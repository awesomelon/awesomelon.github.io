---
title: Drone CI와 Bitbucket 연동하기
date: 2023-10-21 16:00:00 +0900
categories: [ENGINEERING, CI/CD]
tags: [drone, ci/cd, bitbucket, docker, pipeline]
author: j-ho
img_path: /assets/img/for_post/
description: Docker 기반 CI 플랫폼 Drone CI를 Bitbucket과 연동해 파이프라인을 구성한 과정을 정리합니다.
---

Drone CI는 Harness에서 제공하는 CI 플랫폼으로, Go로 작성되어 있고 YAML 파일로 파이프라인을 구성할 수 있습니다. 이 글에서는 Server와 Docker Runner를 컨테이너로 배포하고 각 파이프라인 단계도 컨테이너에서 실행합니다. Drone에는 Exec·SSH 등 다른 Runner도 있으므로 모든 파이프라인이 Docker에서 실행되는 것은 아니에요.

---

## Drone 아키텍처

**Drone Server**는 저장소에서 변경 사항을 모니터링하고 구성 파일(`.drone.yml`)에 따라 Drone Runner에 task를 추가합니다.

**Drone Runner**는 Drone Server에서 task들을 polling하고 지정된 pipeline을 실행합니다.

---

## Bitbucket 연동 설정

연동을 위해 Bitbucket OAuth Key와 Secret이 필요해요.

### BitBucket Workspace Settings 접속

![2023-10-21-image1](2023-10-21-image1.png)
_Bitbucket Workspace Settings_

### OAuth Consumer 생성

OAuth Consumer → Add Consumer 클릭 후 정보를 입력해요.

![2023-10-21-image2](2023-10-21-image2.png)
_OAuth Consumer 설정_

- **Callback URL**: Drone Server의 `{URL}/login`
- **URL**: Drone Server의 URL

![2023-10-21-image3](2023-10-21-image3.png)
_생성된 OAuth Key와 Secret_

---

## Drone CI 설치

아래는 `docker-compose.yml` 예시입니다. `{...}`는 실제 값으로 바꿔야 하는 자리표시자입니다. `openssl rand -hex 16`을 한 번 실행해 만든 값을 Server와 Runner의 `DRONE_RPC_SECRET`에 동일하게 넣어주세요.

```yaml
version: '3.1'

services:
  server:
    image: drone/drone:latest
    container_name: drone
    volumes:
      - /var/lib/drone:/data
    environment:
      - DRONE_BITBUCKET_CLIENT_ID={CLIENT_ID}
      - DRONE_BITBUCKET_CLIENT_SECRET={SECRET}
      - DRONE_RPC_SECRET={SHARED_SECRET}
      - DRONE_SERVER_HOST={DRONE_SERVER_HOST}
      - DRONE_SERVER_PROTO={DRONE_SERVER_PROTO}
    ports:
      - '12080:80'
      - '12443:443'
    restart: always

  runner:
    image: drone/drone-runner-docker:latest
    container_name: runner
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - DRONE_RPC_PROTO={DRONE_SERVER_PROTO}
      - DRONE_RPC_HOST={DRONE_SERVER_HOST}
      - DRONE_RPC_SECRET={SHARED_SECRET}
      - DRONE_RUNNER_CAPACITY=2
      - DRONE_RUNNER_NAME=runner
    ports:
      - '3000:3000'
    restart: always
```

> Drone Server와 Drone Runner의 `DRONE_RPC_SECRET`은 같아야 합니다.
{: .prompt-danger }

`DRONE_SERVER_HOST`에는 스킴을 제외한 외부 호스트명과 필요한 포트를 넣습니다. 위 포트 매핑으로 HTTP에 직접 접속한다면 `{호스트}:12080`과 `DRONE_SERVER_PROTO=http`를 사용합니다. HTTPS를 사용하려면 인증서 또는 앞단 프록시의 TLS 설정도 필요하며, `12443:443` 매핑만으로 HTTPS가 활성화되지는 않습니다. Runner에서도 설정한 주소에 접속할 수 있어야 해요.

```bash
docker-compose -f docker-compose.yml up -d
```

---

## Repository 활성화

브라우저에서 Drone Server에 접속하면 Bitbucket Repository가 연동된 것을 확인할 수 있습니다.

![2023-10-21-image4](2023-10-21-image4.png)
_Drone에 연동된 Bitbucket Repository 목록_

Repository를 활성화하면 자동으로 해당 Repository에 Drone Webhook이 등록됩니다.

![2023-10-21-image7](2023-10-21-image7.png)
_Bitbucket에 자동 등록된 Drone Webhook_

---

## 파이프라인 작성

프로젝트의 root에 `.drone.yml` 파일을 생성합니다.

```yaml
---
kind: pipeline
type: docker
name: deployments

steps:
  - name: step1
    image: alpine
    commands:
      - echo "Hello World"

  - name: step2
    image: alpine
    commands:
      - echo "Hello World2"
```

코드를 푸시하면 파이프라인이 실행돼요.

![2023-10-21-image9](2023-10-21-image9.png)
_파이프라인 실행 목록_

![2023-10-21-image10](2023-10-21-image10.png)
_파이프라인 실행 상세 로그_

---

## 정리

**연동 절차:**
1. Bitbucket OAuth Consumer 생성
2. Docker Compose로 Server와 Runner 배포
3. Repository 활성화 (Webhook 자동 등록)
4. `.drone.yml` 작성 후 푸시

**참고 자료:**
- [Drone 공식 문서](https://docs.drone.io)
- [Bitbucket Cloud Provider](https://docs.drone.io/server/provider/bitbucket-cloud/)
- [Drone Docker Runner 설치](https://docs.drone.io/runner/docker/installation/linux/)
