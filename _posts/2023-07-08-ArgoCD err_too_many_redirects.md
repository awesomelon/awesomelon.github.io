---
title: ArgoCD err_too_many_redirects 해결하기
date: 2023-07-08 22:00:00 +0900
categories: [ENGINEERING, DEVOPS, ArgoCD]
tags: [argocd, kubernetes, ingress, troubleshooting, tls]
author: j-ho
description: ArgoCD 서버 설정 시 발생하는 무한 리다이렉션 문제(err_too_many_redirects)의 원인과 해결 방법을 알아봅니다.
---

ArgoCD 서버를 세팅하고 HTTPS를 연결하여 브라우저에서 접속하려고 보니 `err_too_many_redirects` 이슈가 발생했습니다.

---

## 원인

- Ingress Controller는 TLS를 자체적으로 종료하고 HTTP를 통해 백엔드 서비스와 통신
- argocd-server는 자체적으로 TLS를 종료하고 항상 HTTP 요청을 HTTPS로 리다이렉션

둘이 결합하면서 ArgoCD 서버는 HTTPS로 무한 리다이렉션이 발생합니다.

```
사용자 (HTTPS) → Ingress Controller (TLS 종료) → ArgoCD Server (HTTP → HTTPS 리다이렉트) → 무한 루프
```

---

## 해결 방법

argocd-server deployment 시 `--insecure` 플래그를 추가합니다.

```yaml
containers:
  - command:
      - argocd-server
      - --insecure
```

`--insecure` 플래그는 ArgoCD 서버가 자체 TLS 종료를 비활성화하고, HTTP 요청을 받아들이도록 합니다. 실제 TLS 종료는 Ingress Controller에서 처리됩니다.

```
사용자 (HTTPS) → Ingress Controller (TLS 종료) → ArgoCD Server (HTTP 수락) → 정상 응답
```

---

## 참고 자료

- [GitHub Issue: err_too_many_redirects](https://github.com/argoproj/argo-cd/issues/2953)
- [ArgoCD 공식 문서: Ingress 설정](https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/)
