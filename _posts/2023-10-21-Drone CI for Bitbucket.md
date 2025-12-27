---
title: Drone CI와 Bitbucket 연동하기
date: 2023-10-21 16:00:00 +0900
categories: [ENGINEERING, CI/CD]
tags: [drone, ci/cd, bitbucket, docker, pipeline]
author: j-ho
img_path: /assets/img/for_post/
description: Docker 기반의 경량 CI 플랫폼인 Drone CI를 Bitbucket과 연동하여 파이프라인을 구성하는 방법을 알아봅니다.
---

Drone CI는 도커(Docker)를 기반으로 [Harness](https://harness.io)에서 개발한 오픈 소스 CI 플랫폼입니다.

모든 구성 요소는 도커 컨테이너(Docker Container)로 되어 있으며 파이프라인 단계 실행도 도커 컨테이너로 수행됩니다.

Go lang으로 작성되어 매우 가볍고 설정 파일도 간단한 YAML 파일로 구성할 수 있어 유지보수, 디버깅이 쉽습니다.

또한 공통적인 파이프라인이 있을 경우 Template을 등록하여 공통적으로 사용할 수도 있습니다.

## Drone 아키텍처

### Drone Server

[Drone Server](https://docs.drone.io/server/overview/)는 저장소에서 변경 사항을 모니터링합니다. 저장소에 저장된 구성 파일(`.drone.yml`)에 따라 Drone Runner에 task를 추가합니다.

### Drone Runner

[Drone Runner](https://docs.drone.io/runner/overview/)는 Drone Server에서 task들을 polling합니다. 후에 지정된 pipeline을 실행합니다.

> Drone은 Server-Runner 구조로 되어 있으며, Server는 작업을 관리하고 Runner는 실제 파이프라인을 실행합니다.
{: .prompt-info }

## Bitbucket 연동 설정

이 글에서는 Drone CI에 Bitbucket을 연동하는 과정을 설명하겠습니다.

우선 연동을 위해선 Bitbucket OAuth를 위한 Key, Secret이 필요합니다.

### BitBucket Workspace Settings 접속

![2023-10-21-image1](2023-10-21-image1.png)
_Bitbucket Workspace Settings_

### OAuth Consumer 생성

**OAuth Consumer → Add Consumer 클릭**

그 후 아래와 같이 정보를 입력합니다.

![2023-10-21-image2](2023-10-21-image2.png)
_OAuth Consumer 설정_

**필수 설정 항목:**
- **Callback URL**: OAuth 인증을 위한 콜백 URL입니다. Drone Server의 `{URL}/login`으로 입력해주시면 됩니다. 언제든 수정 가능하니 우선 `https://example.com/login`으로 입력하셔도 됩니다.
- **URL**: Drone Server의 URL을 입력해주세요.

입력을 완료하신다면 아래와 같이 Key와 Secret Key가 생성됩니다.

![2023-10-21-image3](2023-10-21-image3.png)
_생성된 OAuth Key와 Secret_

> 창을 닫지 마시고 아래의 단계를 이어서 진행해주세요. 생성된 Key와 Secret은 Drone 설정에 필요합니다.
{: .prompt-warning }

## Drone CI 설치

Drone CI 서버를 띄워보겠습니다. 위에서 말씀드렸다시피 Drone CI는 구성 요소가 모두 도커로 되어 있습니다.

따라서 도커 컨테이너로 Drone을 띄우시면 됩니다. 아래는 `docker-compose.yml`입니다.
```yaml
# Docker-compose file
version: '3.1'

services:
  server:
    image: drone/drone:latest
    container_name: drone
    volumes:
      - /var/lib/drone:/data
    environment:
      - DRONE_BITBUCKET_SERVER=https://bitbucket.org
      - DRONE_BITBUCKET_CLIENT_ID={CLIENT_ID}
      - DRONE_BITBUCKET_CLIENT_SECRET={SECRET}
      - DRONE_RPC_SECRET={openssl rand -hex 16} # server와 runner의 RPC_SECRET 동일
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
      - DRONE_RPC_SECRET={openssl rand -hex 16} # server와 runner의 RPC_SECRET 동일
      - DRONE_RUNNER_CAPACITY=2
      - DRONE_RUNNER_NAME=runner
      - DRONE_RUNNER_VOLUMES=/home/centos/drone-runner:/var/lib/drone-runner
    ports:
      - '3000:3000'
    restart: always
```

### Drone Server 환경 변수

[공식 문서: Drone Server Configuration](https://docs.drone.io/server/provider/bitbucket-cloud/)

- **DRONE_BITBUCKET_SERVER**: Drone과 연동될 Bitbucket 서버 URL입니다
- **DRONE_BITBUCKET_CLIENT_ID**: Bitbucket OAuth Key입니다
- **DRONE_BITBUCKET_CLIENT_SECRET**: Bitbucket OAuth Secret Key입니다
- **DRONE_RPC_SECRET**: Drone Server와 Drone Runner가 서로 RPC 통신을 위해 사용될 Secret Key입니다. `openssl rand -hex 16` 명령으로 생성합니다
- **DRONE_SERVER_HOST**: Drone Server의 HOST NAME입니다
- **DRONE_SERVER_PROTO**: Drone Server의 protocol입니다 (예: http, https)

### Drone Runner 환경 변수

[공식 문서: Drone Runner Configuration](https://docs.drone.io/runner/docker/installation/linux/)

- **DRONE_RPC_PROTO**: Drone Server의 protocol입니다
- **DRONE_RPC_HOST**: Drone Server의 HOST NAME입니다
- **DRONE_RPC_SECRET**: Drone Server와 Drone Runner가 서로 RPC 통신을 위해 사용될 Secret Key입니다. `openssl rand -hex 16` 명령으로 생성합니다

> **중요:** Drone Server와 Drone Runner의 `DRONE_RPC_SECRET`은 같아야 합니다.
{: .prompt-danger }

### 실행

작성을 완료하셨다면 아래 명령어를 실행합니다.
```bash
docker-compose -f docker-compose.yml up -d
```

## Drone 접속 및 Repository 활성화

브라우저에서 위의 Drone Server에 접속해보신다면 Bitbucket Repository가 연동된 것을 확인하실 수 있습니다.

![2023-10-21-image4](2023-10-21-image4.png)
_Drone에 연동된 Bitbucket Repository 목록_

이 중 하나의 Repository에 접속해보겠습니다.

![2023-10-21-image5](2023-10-21-image5.png)
_Repository 상세 화면_

### Repository 활성화

Repository를 활성화시켜보겠습니다.

![2023-10-21-image6](2023-10-21-image6.png)
_Repository 활성화 후 설정 화면_

Repository가 활성화되었습니다. 보이는 옵션을 간단하게 설명드리면 아래와 같습니다.

**Repository 설정:**
- **General**: 해당 Repository의 설정
- **Secrets**: pipeline 실행 시 해당 Repository에서만 사용할 환경 변수

**Organization 설정:**
- **Organization → Secret**: 전체 Repository에서 공통으로 사용할 환경 변수
- **Organization → Templates**: pipeline template

> 자세한 옵션은 [Drone 공식 문서](https://docs.drone.io)를 확인해주세요.
{: .prompt-tip }

### Webhook 자동 등록

추가로 Repository를 활성화하면 자동으로 해당 Repository에 `Drone Webhook`이 등록됩니다.

![2023-10-21-image7](2023-10-21-image7.png)
_Bitbucket에 자동 등록된 Drone Webhook_

## 파이프라인 작성

위에서 Repository를 활성화했을 때 나왔던 옵션을 살펴보면 `.drone.yml`이 있습니다. Drone Runner는 이 파일에 설정된대로 파이프라인을 실행합니다.

프로젝트의 root에 `.drone.yml` 파일을 생성합니다.

![2023-10-21-image8](2023-10-21-image8.png)
_프로젝트 루트에 .drone.yml 파일 생성_

### 샘플 파이프라인

샘플 파이프라인을 작성해보겠습니다.
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

위 코드를 작성하고 저장소에 푸시 후 Drone에서 해당 Repository를 확인해보면 파이프라인이 실행되고 있는 것을 확인하실 수 있습니다.

![2023-10-21-image9](2023-10-21-image9.png)
_파이프라인 실행 목록_

![2023-10-21-image10](2023-10-21-image10.png)
_파이프라인 실행 상세 로그_

> 각 step은 독립적인 Docker 컨테이너에서 실행되며, 순차적으로 처리됩니다.
{: .prompt-info }

## 정리

Drone CI와 Bitbucket 연동 과정 요약:

### Drone CI의 주요 특징

| 특징 | 설명 |
|:---|:---|
| **Docker 기반** | 모든 구성 요소가 컨테이너로 실행 |
| **경량** | Go lang으로 작성되어 가볍고 빠름 |
| **간편한 설정** | YAML 파일로 파이프라인 정의 |
| **템플릿 지원** | 공통 파이프라인을 템플릿으로 재사용 |
| **확장성** | 다양한 Runner 지원 (Docker, Kubernetes 등) |

### 연동 절차

**1단계: Bitbucket OAuth 설정**
- Workspace Settings에서 OAuth Consumer 생성
- Callback URL 및 권한 설정
- Client ID와 Secret 발급

**2단계: Drone 설치**
- Docker Compose로 Server와 Runner 배포
- 환경 변수 설정 (RPC_SECRET 동일하게)
- 컨테이너 실행

**3단계: Repository 활성화**
- Drone UI에서 Repository 선택
- 활성화 및 설정
- Webhook 자동 등록 확인

**4단계: 파이프라인 작성**
- `.drone.yml` 파일 생성
- 파이프라인 단계 정의
- 코드 푸시 후 자동 실행 확인

### 아키텍처 구조
```
[Bitbucket]
    ↓ (Webhook)
[Drone Server]
    ↓ (RPC)
[Drone Runner] → Docker Container (Pipeline 실행)
```

### 주요 설정 포인트

**보안:**
- `DRONE_RPC_SECRET`은 Server와 Runner 간 통신 암호화에 사용
- OAuth Secret은 안전하게 보관
- Secrets 기능으로 민감 정보 관리

**확장성:**
- `DRONE_RUNNER_CAPACITY`로 동시 실행 작업 수 조절
- 여러 Runner를 추가하여 부하 분산 가능
- Organization Templates로 공통 파이프라인 관리

**유지보수:**
- YAML 기반 설정으로 버전 관리 용이
- Docker 기반으로 환경 일관성 보장
- 명확한 로그로 디버깅 간편

### 참고 자료

- [Drone 공식 문서](https://docs.drone.io)
- [Bitbucket Cloud Provider](https://docs.drone.io/server/provider/bitbucket-cloud/)
- [Docker Runner Installation](https://docs.drone.io/runner/docker/installation/linux/)

Drone CI와 Bitbucket을 연동하는 방법에 대해서 알아보았습니다.