---
title: ArgoCD err_too_many_redirects 해결하기
date: 2023-07-08 22:00:00 +0900
categories: [ENGINEERING, DEVOPS, ArgoCD]
tags: [argocd, kubernetes, ingress, troubleshooting, tls]
author: j-ho
description: ArgoCD에서 err_too_many_redirects가 발생했을 때 해결 방법
---

ArgoCD 서버를 세팅하고 HTTPS를 연결하여 브라우저에서 접속하려니 `err_too_many_redirects` 이슈가 발생했어요.

---

## 원인

- 당시 구성에서는 Ingress Controller가 TLS 연결을 종료하고 HTTP로 백엔드 서비스와 통신
- 기본 TLS 설정의 argocd-server는 전달받은 HTTP 요청을 HTTPS로 리다이렉션

브라우저가 리다이렉션된 HTTPS 주소로 다시 요청해도 Ingress가 HTTP로 전달하므로 같은 리다이렉션이 반복됩니다.

```
사용자 (HTTPS) → Ingress Controller (TLS 종료) → ArgoCD Server (HTTP → HTTPS 리다이렉트) → 무한 루프
```

---

## 해결 방법

Ingress에서 TLS를 종료하고 백엔드에 HTTP로 전달하는 구성을 유지한다면, 기존 argocd-server Deployment의 컨테이너 실행 명령에 `--insecure` 플래그를 추가합니다. 아래는 해당 부분만 발췌한 예시예요.

```yaml
containers:
  - command:
      - argocd-server
      - --insecure
```

`--insecure` 플래그는 ArgoCD 서버의 자체 TLS 종료를 비활성화하고 HTTP 요청을 받아들이게 해요. 실제 TLS 종료는 Ingress Controller에서 처리돼요.

```
사용자 (HTTPS) → Ingress Controller (TLS 종료) → ArgoCD Server (HTTP 수락) → 정상 응답
```

---

## 참고 자료

- [GitHub Issue: err_too_many_redirects](https://github.com/argoproj/argo-cd/issues/2953)
- [ArgoCD 공식 문서: Ingress 설정](https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/)
- [ArgoCD 2.7 문서: Ingress 설정](https://argo-cd.readthedocs.io/en/release-2.7/operator-manual/ingress/)
