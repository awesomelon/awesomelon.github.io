---
title: Drone CI와 Bitbucket 연동하기
last_modified_at: 2026-09-12 13:38:07 +0900
date: 2023-10-21 16:00:00 +0900
categories: [ENGINEERING, CI/CD]
tags: [drone, ci/cd, bitbucket, docker, pipeline]
author: j-ho
img_path: /assets/img/for_post/
description: Docker 기반 CI 플랫폼 Drone CI를 Bitbucket과 연동해 파이프라인을 구성한 과정을 정리합니다.
---

Drone CI는 Harness에서 제공하는 CI 플랫폼으로, Go로 작성되어 있고 YAML 파일로 파이프라인을 구성할 수 있습니다. 이 글에서는 Server와 Docker Runner를 컨테이너로 배포하고 각 파이프라인 단계도 컨테이너에서 실행합니다. Drone에는 Exec·SSH 등 다른 Runner도 있으므로 모든 파이프라인이 Docker에서 실행되는 것은 아니에요.

---

> 아래 화면은 2023년 연동 당시의 기록입니다. 설치 예시는 Drone Server 2 계열, Docker Runner 1 계열, Docker Compose v2 명령을 기준으로 정리했습니다. Bitbucket Cloud용 설정이며 Bitbucket Data Center/Server에는 별도 provider 설정이 필요합니다.
{: .prompt-info }

## Drone 아키텍처

**Drone Server**는 Bitbucket의 webhook을 받아 파이프라인을 등록하고, 저장소의 `.drone.yml`을 바탕으로 실행할 작업을 관리합니다. Bitbucket에서 Drone으로 들어오는 webhook과 Runner가 Server에서 작업을 가져오는 통신은 방향이 다릅니다.

**Drone Runner**는 Drone Server에서 task들을 polling하고 지정된 pipeline을 실행합니다.

---

## Bitbucket 연동 설정

연동을 위해 Bitbucket OAuth Consumer의 Key와 Secret이 필요해요. 먼저 `https://drone.example.com`처럼 고정된 외부 주소와 TLS 인증서를 준비합니다. Bitbucket Cloud가 webhook을 보낼 수 있어야 하므로 VPN 안에서 브라우저로 열리는 것만으로는 충분하지 않습니다. [Drone의 Bitbucket Cloud 설정](https://docs.drone.io/server/provider/bitbucket-cloud/)

OAuth Consumer의 저장소 조회·webhook 등록 권한은 공식 provider 안내에 맞춰 설정하고, Drone에 허용할 사용자·조직 범위도 함께 정합니다. 이미지를 빌드할 수 있는 CI 서버를 누구나 사용할 수 있는 상태로 열어두지 않도록 해야 해요.

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

아래 구성은 **같은 Linux 호스트의 HTTPS 리버스 프록시가 `127.0.0.1:12080`으로 전달하는 환경**을 가정합니다. 프록시는 이 파일에 포함되어 있지 않습니다. 외부에는 `https://drone.example.com`, Server와 Runner 사이에는 Compose 내부 서비스명 `server:80`을 사용해요.

`compose.yaml`:

```yaml
services:
  server:
    image: ${DRONE_SERVER_IMAGE:?Set DRONE_SERVER_IMAGE}
    volumes:
      - drone_data:/data
    environment:
      DRONE_BITBUCKET_CLIENT_ID: ${DRONE_BITBUCKET_CLIENT_ID:?Set client ID}
      DRONE_BITBUCKET_CLIENT_SECRET: ${DRONE_BITBUCKET_CLIENT_SECRET:?Set client secret}
      DRONE_RPC_SECRET: ${DRONE_RPC_SECRET:?Set shared secret}
      DRONE_SERVER_HOST: ${DRONE_SERVER_HOST:?Set external hostname}
      DRONE_SERVER_PROTO: https
      DRONE_USER_FILTER: ${DRONE_USER_FILTER:?Set allowed Bitbucket accounts}
    ports:
      - '127.0.0.1:12080:80'
    restart: unless-stopped

  runner:
    image: ${DRONE_RUNNER_IMAGE:?Set DRONE_RUNNER_IMAGE}
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      DRONE_RPC_PROTO: http
      DRONE_RPC_HOST: server:80
      DRONE_RPC_SECRET: ${DRONE_RPC_SECRET:?Set shared secret}
      DRONE_RUNNER_CAPACITY: '2'
      DRONE_RUNNER_NAME: runner
    restart: unless-stopped

volumes:
  drone_data:
```

같은 디렉터리의 `.env`에는 다음 값을 넣습니다. `REPLACE_...` 값은 실제 값으로 바꿔야 하며, 공유 비밀은 `openssl rand -hex 32`를 한 번 실행해 생성합니다. Server와 Runner는 같은 변수를 참조하므로 서로 다른 비밀을 넣을 실수를 줄일 수 있어요.

```dotenv
DRONE_SERVER_IMAGE=drone/drone:2
DRONE_RUNNER_IMAGE=drone/drone-runner-docker:1
DRONE_SERVER_HOST=drone.example.com
DRONE_USER_FILTER=REPLACE_WITH_ALLOWED_BITBUCKET_ACCOUNT
DRONE_BITBUCKET_CLIENT_ID=REPLACE_WITH_OAUTH_KEY
DRONE_BITBUCKET_CLIENT_SECRET=REPLACE_WITH_OAUTH_SECRET
DRONE_RPC_SECRET=REPLACE_WITH_GENERATED_SECRET
```

`DRONE_USER_FILTER`에는 허용할 Bitbucket 계정을 쉼표로 구분해 넣고 허용되지 않은 계정의 등록이 거절되는지 확인합니다. [등록 허용 목록 설정](https://docs.drone.io/server/reference/drone-user-filter/)

`:2`와 `:1`은 공식 설치 문서에서 제시하는 계열 태그이며 고정 버전은 아닙니다. 연결 검증 후 운영 설정에는 검토한 정확한 태그 또는 digest를 기록합니다. `.env`는 Git에서 제외하고 접근 권한을 제한합니다. `docker compose config`는 해석된 secret까지 출력할 수 있으므로 여기서는 출력 없는 `--quiet` 검사를 사용합니다.

```bash
chmod 600 .env
docker compose config --quiet
docker compose up -d
docker compose ps
docker compose logs --tail=100 runner
```

Runner 로그에 Server 연결 성공이 나타나는지 확인합니다. `DRONE_SERVER_HOST`에는 `https://`나 `/login` 경로를 넣지 않습니다. OAuth callback에는 반대로 스킴을 포함한 `https://drone.example.com/login` 전체 주소가 필요해요.

리버스 프록시도 컨테이너라면 그 컨테이너에서 `127.0.0.1`은 Drone 호스트가 아닙니다. 공통 Docker 네트워크의 `server:80`으로 전달하는 등 네트워크 구성을 맞춰야 합니다. Runner를 다른 호스트로 옮길 때도 내부 서비스명이 사라지므로 RPC 주소와 TLS 설정을 함께 변경합니다.

> Docker socket을 마운트한 Runner는 호스트 Docker를 제어합니다. CI 전용 호스트를 사용하고 신뢰하지 않는 파이프라인에 호스트 볼륨·privileged 실행을 허용하지 않습니다. Runner 관리용 포트 3000은 일반 파이프라인 실행에 필요하지 않아 외부에 공개하지 않았습니다. [Docker Engine 보안](https://docs.docker.com/engine/security/)
{: .prompt-warning }

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

프로젝트의 root에 `.drone.yml` 파일을 생성합니다. 아래는 배포가 아니라 저장소 이벤트와 Runner 연결을 확인하는 최소 파이프라인입니다. 예시 Alpine 계열은 2026년 보완 시점의 값이며, 실제 프로젝트에서는 빌드 도구에 맞는 이미지를 사용합니다.

```yaml
---
kind: pipeline
type: docker
name: connection-check

steps:
  - name: step1
    image: alpine:3.24
    commands:
      - echo "Hello World"

  - name: step2
    image: alpine:3.24
    commands:
      - echo "Hello World2"
```

코드를 푸시하면 파이프라인이 실행돼요.

![2023-10-21-image9](2023-10-21-image9.png)
_파이프라인 실행 목록_

![2023-10-21-image10](2023-10-21-image10.png)
_파이프라인 실행 상세 로그_

---

## 화면은 뜨는데 빌드가 안 된다면

| 증상 | 먼저 확인할 경계 |
| --- | --- |
| OAuth 로그인 실패 | 외부 스킴·호스트·`/login` callback 일치 여부 |
| 저장소가 보이지 않음 | 로그인한 Bitbucket 계정과 OAuth의 저장소 권한 |
| push 후 실행 항목이 생기지 않음 | Bitbucket webhook 전달 결과, Drone 외부 접근, 저장소 활성화 |
| 실행 항목이 Pending에 머무름 | Runner 로그의 RPC 연결, 공유 비밀, Runner 용량·조건 |
| 작업은 시작되지만 clone·pull 실패 | Runner의 Git·이미지 레지스트리 접근과 인증 |

운영 파이프라인을 추가할 때는 빌드 성공만 확인하지 않고, 의도적으로 실패하는 작업 뒤의 배포 단계가 실행되지 않는지도 확인합니다. 배포 secret은 필요한 저장소에만 등록하고 PR의 비신뢰 코드에 노출하지 않아요. 배포 조건은 `main` 같은 branch와 `push` 같은 event를 함께 제한해야 PR 대상 브랜치만 보고 배포되는 일을 피할 수 있습니다. [Drone trigger 규칙](https://docs.drone.io/pipeline/docker/syntax/trigger/)

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

- [Docker: Compose 변수 보간과 필수 값](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/)
- [Alpine: 지원 릴리스 계열](https://www.alpinelinux.org/releases/)
