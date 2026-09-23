---
title: ArgoCD err_too_many_redirects 해결하기
date: 2023-07-08 22:00:00 +0900
categories: [ENGINEERING, DEVOPS, ArgoCD]
tags: [argocd, kubernetes, ingress, troubleshooting, tls]
author: j-ho
description: Argo CD redirect 루프를 요청 경로로 진단하고 TLS 종료 위치에 맞게 Ingress와 서버 설정하기
last_modified_at: 2026-09-12 13:38:07 +0900
---

Argo CD 서버에 HTTPS를 연결한 뒤 브라우저에서 `ERR_TOO_MANY_REDIRECTS`가 발생했습니다. 당시 원인은 **Ingress는 TLS를 종료하고 HTTP로 전달하는데, argocd-server는 그 HTTP 요청을 다시 HTTPS로 보내는 구성**이었습니다.

해결은 TLS를 종료하는 위치와 백엔드 프로토콜을 맞추는 것입니다. `--insecure`를 무조건 붙이는 방법으로 기억하면 다른 구성에서 오히려 문제가 생길 수 있어요.

## 같은 HTTPS 주소로 계속 돌아오는 이유

당시 요청 흐름을 순서대로 보면 다음과 같습니다.

| 단계 | 실제 요청과 응답 |
|:---|:---|
| 1 | 브라우저가 `https://argocd.example.com`에 요청 |
| 2 | Ingress가 TLS를 종료하고 argocd-server에 HTTP로 전달 |
| 3 | TLS를 사용하는 argocd-server가 HTTPS 주소로 redirect |
| 4 | 브라우저가 그 HTTPS 주소를 다시 요청. 2번과 같은 상황 반복 |

브라우저는 이미 HTTPS를 쓰지만 **argocd-server가 받는 연결은 계속 HTTP**라는 점이 핵심입니다. 이 구성에서 내부 TLS를 끄는 방법은 [Argo CD 2.7의 Ingress 문서](https://argo-cd.readthedocs.io/en/release-2.7/operator-manual/ingress/)에도 설명돼 있습니다.

## 변경 전에 redirect를 만드는 위치 확인하기

먼저 실제 응답 헤더를 확인합니다. 아래 도메인은 예시이므로 자신의 주소로 바꿔 실행하세요.

```bash
curl -sS -D - -o /dev/null https://argocd.example.com
```

상태 코드가 3xx라면 `Location`을 봅니다. 필요하면 제한된 횟수만 따라가며 응답을 비교합니다.

```bash
curl -sS -L --max-redirs 5 -D - -o /dev/null https://argocd.example.com
```

같은 HTTPS 주소가 반복된다는 사실은 루프의 증거지만, 이것만으로 Argo CD가 원인이라고 확정할 수는 없습니다. Ingress·앞단 프록시가 별도 redirect를 만들거나 인증 경로가 반복되는 경우도 있기 때문이에요. 다음 세 가지를 함께 확인합니다.

1. Ingress가 외부 TLS를 종료하는지, TLS passthrough인지 확인합니다.
2. Ingress의 upstream 프로토콜과 Service가 가리키는 포트를 확인합니다.
3. argocd-server의 TLS 설정·로그와 Ingress access log를 같은 요청 시점으로 비교합니다.

브라우저의 쿠키를 지우는 것보다 먼저 서버 사이의 요청 프로토콜을 확인하면 원인 후보를 줄일 수 있습니다. 인증 화면 사이를 오가는 루프라면 아래의 TLS 수정과 별도 문제로 봐야 합니다.

## 해결 방법: TLS 종료 위치에 맞춰 선택하기

| 유지하려는 구성 | argocd-server 설정 | 함께 맞출 것 |
|:---|:---|:---|
| Ingress에서 TLS 종료, 내부 HTTP | 서버 TLS 비활성화 | Ingress upstream도 HTTP로 설정 |
| Ingress에서 TLS 종료 후 내부 HTTPS 재연결 | 서버 TLS 유지 | upstream HTTPS, 백엔드 인증서 신뢰 설정 |
| TLS passthrough | 서버 TLS 유지 | Controller의 passthrough 지원·설정, 서버 인증서 |

Controller마다 HTTP·gRPC 처리와 annotation이 다릅니다. 특히 Argo CD의 웹 UI가 열린다고 CLI의 gRPC 연결도 정상이라고 결론 내릴 수는 없어요. 자신이 사용하는 Controller에 맞는 [공식 Ingress 예제](https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/)를 적용해야 합니다.

### 당시 구성: Ingress TLS 종료 + 내부 HTTP

기존 argocd-server 컨테이너 실행 명령에 `--insecure`를 추가했습니다. 아래는 해당 부분만 나타낸 예시이며 Deployment 전체를 대체하는 YAML이 아닙니다. 기존 인수도 유지해야 합니다.

```yaml
containers:
  - name: argocd-server
    command:
      - argocd-server
      - --insecure
```

기본 설치 매니페스트처럼 `argocd-cmd-params-cm`을 읽는 구성이라면 ConfigMap의 `server.insecure`로 설정할 수도 있습니다. 두 방법 중 실제 배포를 관리하는 방식에 맞는 하나를 사용하세요. [공식 ConfigMap 설정](https://argo-cd.readthedocs.io/en/stable/operator-manual/argocd-cmd-params-cm-yaml/)

```bash
kubectl -n argocd patch configmap argocd-cmd-params-cm \
  --type merge \
  -p '{"data":{"server.insecure":"true"}}'

kubectl -n argocd rollout restart deployment argocd-server
kubectl -n argocd rollout status deployment argocd-server
```

예제의 네임스페이스와 리소스명은 기본 설치 기준입니다. ConfigMap 값이 프로세스 시작 때 읽히는 구성에서는 Pod를 다시 시작해야 반영됩니다. Helm이나 GitOps로 설치했다면 실제 values 또는 Git의 매니페스트에도 변경을 반영해야 다음 동기화 때 되돌아가지 않습니다.

`--insecure`는 여기서 **서버 자체 TLS를 끄는 옵션**입니다. 브라우저와 Ingress 사이의 HTTPS는 유지되지만 Ingress와 서버 사이에는 HTTP가 흐릅니다. 내부 통신도 암호화해야 하는 환경이라면 두 번째 또는 세 번째 구성을 선택해야 합니다.

## 정상화는 화면 표시까지 확인하기

적용 뒤에는 rollout 완료를 확인하고 위 `curl` 요청을 다시 실행합니다. 기대하는 결과는 TLS redirect가 무한히 반복되지 않는 것입니다. 첫 응답이 꼭 200이어야 하는 것은 아니며, 로그인 등 의도한 경로로 한 번 이동할 수 있습니다.

그다음 브라우저에서 로그인과 실제 화면 조회를 확인합니다. CLI도 사용하는 환경이면 CLI 연결을 따로 확인하세요. redirect는 사라졌는데 502가 생겼다면 Ingress upstream 프로토콜과 서버 TLS 설정이 엇갈렸는지 먼저 봅니다.

문제가 해결되지 않으면 바꾼 설정을 원래 값으로 되돌리고 다시 배포한 뒤 다른 redirect 발생 지점을 조사해야 합니다. 당시 사례의 교훈은 옵션 하나를 외우는 것보다, **외부 HTTPS 요청이 각 구간에서 어떤 프로토콜로 바뀌는지 추적하는 것**입니다.
