---
title: Drone CI와 Portainer를 이용한 CI/CD 구축하기
date: 2023-11-24 16:00:00 +0900
categories: [ENGINEERING, DEVOPS, CI/CD]
tags: [portainer, drone, ci/cd, docker, docker swarm, gitops]
author: j-ho
img_path: /assets/img/for_post/
description: Drone CI로 이미지를 빌드하고 Portainer로 자동 배포하는 GitOps 기반 CI/CD 파이프라인을 구축하는 방법을 알아봅니다.
---

> [Drone CI](https://j-ho.dev/posts/Drone-CI-for-Bitbucket/) 글과 연결되니 한번 읽어보시는 것을 추천합니다.
{: .prompt-info }

## Portainer란?

### Accelerate container adoption

[Portainer](https://www.portainer.io)는 다음과 같은 특징을 가진 컨테이너 관리 도구입니다:

- 다양한 환경에서 Kubernetes, Docker, Swarm 등을 쉽게 배포하고 관리할 수 있는 경량화된 관리 도구로서, 웹 UI를 제공합니다
- 실행 중인 컨테이너, 이미지, 볼륨 등을 직관적으로 확인 가능
- CLI로 작업했던 Docker 관련 작업을 손쉽게 사용 가능

### Architecture

[Portainer 아키텍처](https://academy.portainer.io/architecture/#/lessons/LW72Ff_KQ2w4KSKupGE5a3zZ0kUkbn3E)

Portainer는 `Server`와 `Agent` 두 가지 요소로 구성됩니다.

이들은 기존에 구축된 컨테이너 환경에서 가볍게 운영되는 컨테이너로 실행됩니다. **클러스터 내의 각 노드에 Portainer Agent를 설치해야 하며, 이는 Portainer Server 컨테이너에 정보를 전달하도록 설정되어야 합니다.**

`Portainer Server`는 여러 Agent의 연결을 수용할 수 있으며, 이를 통해 하나의 중앙화된 인터페이스에서 여러 클러스터를 관리할 수 있습니다. 이를 위해 Portainer Server 컨테이너는 데이터 지속성이 필요합니다. `Agent`는 상태가 없으며, 데이터는 Server로 전송됩니다.

![2023-11-24-image1](2023-11-24-image1.png)
_Portainer 아키텍처 구조_

> Portainer는 Server-Agent 모델로 중앙화된 관리를 제공하며, 여러 클러스터를 하나의 인터페이스에서 관리할 수 있습니다.
{: .prompt-tip }

## Portainer 설치

간단하게 Docker Compose로 Server와 Agent를 컨테이너로 띄워보겠습니다.
```yaml
version: '3.2'

services:
  agent:
    image: portainer/agent:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /var/lib/docker/volumes:/var/lib/docker/volumes

  portainer:
    image: portainer/portainer-ce:latest
    command: -H tcp://tasks.agent:9001 --tlsskipverify
    ports:
      - '0.0.0.0:9443:9443'
      - '0.0.0.0:9000:9000'
    volumes:
      - portainer_data:/data

volumes:
  portainer_data:
```

### 초기 화면 확인

위의 docker-compose.yml로 컨테이너를 시작한 후 브라우저로 접속해보면 아래와 같은 화면이 뜰 것입니다. 현재 `Portainer Server`와 연동된 클러스터들을 보여주는 화면입니다. primary는 현재 Portainer가 떠있는 Docker를 인식한 것입니다.

![2023-11-24-image2](2023-11-24-image2.png)
_Portainer 환경 목록_

`primary`에 접속해보겠습니다. 현재 Docker 서버의 환경을 간략히 표시해줍니다.

![2023-11-24-image3](2023-11-24-image3.png)
_Docker 환경 대시보드_

## Stack 생성 및 GitOps 설정

### Stack이란?

Stack이란 다중 컨테이너 애플리케이션의 묶음을 의미합니다. docker-compose로 컨테이너를 여러 개 띄웠을 시 그 여러 개를 합쳐서 하나의 Stack이라고 부릅니다.

> Docker Swarm의 Stack과 의미가 일맥상통합니다.
{: .prompt-info }

### Stack 생성

Add Stack 버튼을 클릭합니다.

![2023-11-24-image4](2023-11-24-image4.png)
_Stack 추가 버튼_

그러면 아래와 같이 Stack 정보를 입력하는 화면이 나옵니다.

![2023-11-24-image5](2023-11-24-image5.png)
_Stack 생성 화면_

**주요 설정 항목:**

- **name**: Stack name
- **Build Method**: Stack의 타입입니다
  - Web editor로 직접 docker-compose 파일을 입력 가능
  - Upload로 파일을 업로드 가능
  - **Git Repository**: 자동 배포 가능 (권장)
- **Repository URL**: 변경된 사항이 있는지 감지할 저장소 주소입니다. 변경된 사항이 있을 시 자동으로 배포합니다
- **username, personal access token**: 저장소 인증 정보입니다

> Web editor와 upload는 자동배포가 불가능합니다. GitOps를 위해서는 Git Repository 방식을 사용해야 합니다.
{: .prompt-warning }

### 자동 배포 방식 선택

![2023-11-24-image6](2023-11-24-image6.png)
_자동 배포 설정_

Portainer도 다른 CD 서비스와 마찬가지로 GitOps로 상태를 추적하여 배포합니다. 그 방식은 저장소가 변경되었는지 일정 시간마다 `Polling`하는 방식과 `Webhook`으로 요청을 보내서 바로 배포하는 방식이 있습니다.

**배포 방식 비교:**

| 방식 | 특징 | 제약사항 |
|:---|:---|:---|
| **Webhook** | 즉시 배포, 빠른 반응 | 무료 |
| **Polling** | 주기적 체크 (5분마다) | 유료 기능 |

설정 완료 후 하단에 있는 `Deploy the stack` 버튼을 클릭 시 Stack이 생성됩니다.

> 지정한 경로에 docker-compose.yml이 있어야 생성 가능합니다.
{: .prompt-tip }

## CI/CD 파이프라인 동작 확인

빠른 테스트를 위해 Webhook 방식으로 테스트를 해보았습니다. 아래 이미지는 [Drone CI 페이지](https://j-ho.dev/20/)에서 작업한 Drone CI의 파이프라인 진행 화면입니다.

![2023-11-24-image7](2023-11-24-image7.png)
_Drone CI 파이프라인 실행_

Docker 빌드가 완료된 후 Portainer Server의 Webhook으로 요청을 보냅니다.

### 자동 배포 실행

요청을 받은 Portainer Server는 해당 Stack에서 변경된 이미지가 있는 컨테이너를 확인하여 컨테이너를 새로 띄웁니다.

![2023-11-24-image8](2023-11-24-image8.png)
_Portainer 자동 배포 실행_

## 정리

Drone CI와 Portainer를 이용한 CI/CD 파이프라인 구축 과정:

### 전체 워크플로우
```
1. 코드 Push (Git)
   ↓
2. Drone CI 파이프라인 실행
   ↓
3. Docker 이미지 빌드
   ↓
4. 이미지 레지스트리에 Push
   ↓
5. Portainer Webhook 호출
   ↓
6. Portainer가 새 이미지로 컨테이너 재배포
```

### 주요 구성 요소

| 컴포넌트 | 역할 | 특징 |
|:---|:---|:---|
| **Drone CI** | 빌드 및 테스트 | YAML 기반, 간편한 설정 |
| **Portainer Server** | 배포 관리 | 웹 UI, 중앙 관리 |
| **Portainer Agent** | 노드 모니터링 | 상태 없음, 경량 |
| **Git Repository** | 소스 및 설정 관리 | GitOps 기반 |

### Portainer의 장단점

**장점:**
- 직관적인 웹 UI로 컨테이너 관리 용이
- GitOps 기반 자동 배포 지원
- Webhook을 통한 즉시 배포 (무료)
- 여러 클러스터를 중앙에서 관리
- Docker, Swarm, Kubernetes 모두 지원

**단점:**
- Polling 자동 배포는 유료 기능 (5분마다 체크)
- Enterprise 기능은 유료
- 복잡한 배포 전략(Blue-Green, Canary)은 제한적

### Drone CI vs Jenkins

경험상으론 Jenkins보단 Drone CI가 파이프라인 파일 등을 명확하게 작성할 수 있어서 좋았습니다. (제가 Jenkins를 잘 이용 못 해서 그럴지도...)

**비교:**

| 항목 | Drone CI | Jenkins |
|:---|:---|:---|
| **설정 방식** | YAML 파일 | Groovy/UI |
| **러닝 커브** | 낮음 | 높음 |
| **경량성** | 매우 가벼움 | 무거움 |
| **플러그인** | 제한적 | 매우 풍부 |

### 실무 적용 시 고려사항

**Webhook 설정:**
```yaml
# Drone CI에서 Portainer Webhook 호출 예시
- name: deploy
  image: curlimages/curl
  commands:
    - curl -X POST https://portainer.example.com/api/webhooks/xxxx
  when:
    branch:
      - main
```

**보안:**
- Portainer Webhook URL 보호
- Git Repository 접근 권한 관리
- Docker 이미지 레지스트리 인증

**모니터링:**
- 배포 로그 확인
- 컨테이너 상태 모니터링
- 롤백 계획 수립

### 대안 도구

만약 더 고급 기능이 필요하다면:

- **ArgoCD**: Kubernetes 네이티브 GitOps
- **Flux**: CNCF 프로젝트, GitOps 전문
- **Rancher**: Portainer와 유사하지만 더 많은 기능
- **Kubernetes**: 자체 배포 메커니즘 (Deployment, Rolling Update)

Drone CI와 Portainer를 이용한 CI/CD를 확인해보았습니다. Portainer는 Webhook을 이용한 배포라면 충분히 이용할만 하지만 Polling을 통해 5분마다 자동으로 변경된 것을 체크해 배포해주는 기능은 유료 기능이라서 아쉬웠습니다.