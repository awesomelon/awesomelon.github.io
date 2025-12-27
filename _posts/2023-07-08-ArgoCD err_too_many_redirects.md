---
title: ArgoCD err_too_many_redirects 해결하기
date: 2023-07-08 22:00:00 +0900
categories: [ENGINEERING, DEVOPS, ArgoCD]
tags: [argocd, kubernetes, ingress, troubleshooting, tls]
author: j-ho
description: ArgoCD 서버 설정 시 발생하는 무한 리다이렉션 문제(err_too_many_redirects)의 원인과 해결 방법을 알아봅니다.
---

하루는 ArgoCD 서버를 세팅하던 때였습니다. ArgoCD 서버를 무사히 띄운 후 HTTPS를 연결하여 브라우저에서 HTTPS로 접속하려고 보니 `err_too_many_redirects` 이슈가 발생하였습니다.

## err_too_many_redirects 넌 뭐야?

원인을 파악하니 아래와 같은 이슈가 있었습니다.

**문제의 핵심:**
- `Ingress Controller`는 TLS를 자체적으로 종료하고 HTTP를 통해 백엔드 서비스와 통신
- `argocd-server`는 자체적으로 TLS를 종료하고 항상 HTTP 요청을 HTTPS로 리다이렉션

둘이 결합하면서 ArgoCD 서버는 HTTPS로 무한 리다이렉션이 발생하는 것이었습니다.

> 이 문제는 TLS 종료 지점이 중복되어 발생합니다. Ingress에서 이미 HTTPS를 처리했는데, ArgoCD 서버가 다시 HTTPS로 리다이렉트하려고 시도하면서 무한 루프가 발생합니다.
{: .prompt-warning }

## 해결 방법

argocd-server deployment 시 `--insecure` 플래그를 추가하는 것으로 간단하게 해결할 수 있습니다.
```yaml
containers:
  - command:
      - argocd-server
      - --insecure
```

> `--insecure` 플래그는 ArgoCD 서버가 자체 TLS 종료를 비활성화하고, HTTP 요청을 받아들이도록 합니다. 실제 TLS 종료는 Ingress Controller에서 처리됩니다.
{: .prompt-tip }

## 정리

**문제 발생 시나리오:**
```
사용자 (HTTPS) → Ingress Controller (TLS 종료) → ArgoCD Server (HTTP → HTTPS 리다이렉트) → 무한 루프
```

**해결 후 시나리오:**
```
사용자 (HTTPS) → Ingress Controller (TLS 종료) → ArgoCD Server (HTTP 수락) → 정상 응답
```

**핵심 포인트:**
- Ingress Controller가 TLS 종료를 담당하는 경우, ArgoCD 서버는 `--insecure` 모드로 실행
- 이를 통해 TLS 종료 지점을 하나로 통일
- 백엔드는 HTTP로 통신하되, 외부에는 HTTPS로 제공

### 추가 설정 옵션

ArgoCD Ingress 설정 시 고려할 수 있는 다른 옵션들:

**Option 1**: 단일 Ingress 객체 사용
- ArgoCD UI와 gRPC를 하나의 호스트로 통합

**Option 2**: 여러 Ingress 객체 사용 (권장)
- UI와 gRPC를 별도 호스트로 분리
- 더 나은 보안과 유연성 제공

## 참고 자료

- [GitHub Issue: err_too_many_redirects](https://github.com/argoproj/argo-cd/issues/2953)
- [ArgoCD 공식 문서: Ingress 설정](https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/#option-2-multiple-ingress-objects-and-hosts)