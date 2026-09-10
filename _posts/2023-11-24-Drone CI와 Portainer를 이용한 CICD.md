---
title: Drone CI와 Portainer를 이용한 CI/CD 구축하기
date: 2023-11-24 16:00:00 +0900
categories: [ENGINEERING, DEVOPS, CI/CD]
tags: [portainer, drone, ci/cd, docker, docker swarm, gitops]
author: j-ho
img_path: /assets/img/for_post/
description: Drone CI로 이미지를 빌드하고 Portainer로 배포하는 GitOps 방식 CI/CD 파이프라인을 정리합니다.
---

> [Drone CI](/posts/Drone-CI-for-Bitbucket/) 글과 연결되니 한번 읽어보시는 것을 추천합니다.
{: .prompt-info }

---

## Portainer란?

[Portainer](https://www.portainer.io)는 Kubernetes, Docker, Swarm 등을 쉽게 배포하고 관리할 수 있는 경량화된 관리 도구예요. 웹 UI를 제공하며 실행 중인 컨테이너, 이미지, 볼륨 등을 직관적으로 확인하고 관리할 수 있습니다.

Portainer는 Server와 Agent를 이용해 여러 환경을 중앙에서 관리할 수 있습니다. Docker Swarm에서는 각 노드에 Agent를 배치하는 구성을 사용할 수 있고, 단일 Docker 환경에서는 로컬 소켓으로 직접 연결하는 방식도 가능합니다.

![2023-11-24-image1](2023-11-24-image1.png)
_Portainer 아키텍처 구조_

---

## Portainer 설치

아래 예시는 단일 Docker 호스트에서 Compose로 Server와 Agent를 띄우는 구성입니다. Swarm 클러스터를 관리하려면 Agent의 전역 배포와 overlay 네트워크 등 Swarm용 구성이 별도로 필요해요.

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
    command: -H tcp://agent:9001 --tlsskipverify
    ports:
      - '0.0.0.0:9443:9443'
      - '0.0.0.0:9000:9000'
    volumes:
      - portainer_data:/data

volumes:
  portainer_data:
```

컨테이너를 시작한 후 브라우저로 접속하면 현재 Portainer Server와 연동된 클러스터들을 볼 수 있어요.

![2023-11-24-image2](2023-11-24-image2.png)
_Portainer 환경 목록_

![2023-11-24-image3](2023-11-24-image3.png)
_Docker 환경 대시보드_

---

## Stack 생성 및 GitOps 설정

Portainer에서 Stack은 Compose 파일 등으로 함께 정의하고 배포하는 서비스의 묶음입니다. 단순히 실행 중인 컨테이너 여러 개를 모두 하나의 Stack이라고 부르는 것은 아니에요.

Add Stack 버튼을 클릭하고 Stack 정보를 입력해요.

![2023-11-24-image5](2023-11-24-image5.png)
_Stack 생성 화면_

**주요 설정**
- **Build Method**: Web editor, Upload, Git Repository 중 선택 (GitOps를 위해 Git Repository 권장)
- **Repository URL**: 변경된 사항이 있는지 감지할 저장소 주소
- **username, personal access token**: 저장소 인증 정보

> Git 저장소의 Compose 파일을 기준으로 자동 업데이트하려면 Git Repository 방식을 선택합니다. Web editor·Upload로 만든 Stack의 webhook 기능과 Git 기반 자동 업데이트는 구분해야 하며, 지원 범위는 버전과 에디션에 따라 확인해야 합니다.
{: .prompt-warning }

Portainer의 Git 기반 자동 업데이트에는 Polling 방식(일정 시간마다 저장소 확인)과 Webhook 방식(요청을 받으면 업데이트 확인)이 있습니다. 여기서는 Drone의 빌드 완료 시점에 맞춰 Webhook 방식을 사용했습니다. Polling 자체를 유료 기능이라고 단정해서는 안 되며, 추가 재배포 옵션의 제공 범위는 사용하는 버전과 에디션에서 확인해야 합니다.

![2023-11-24-image6](2023-11-24-image6.png)
_자동 배포 설정_

---

## CI/CD 파이프라인 동작

Drone CI에서 Docker 빌드가 완료된 후 Portainer Server의 Webhook으로 요청을 보냅니다.

![2023-11-24-image7](2023-11-24-image7.png)
_Drone CI 파이프라인 실행_

요청을 받은 Portainer Server는 Git 저장소의 변경을 확인해 Stack을 업데이트합니다. 같은 이미지 태그에 새 이미지만 Push하면 Git 변경이 없어 배포를 건너뛸 수 있어요. 이미지 태그를 갱신한 Compose 파일을 Git에 커밋하거나, 해당 버전에서 제공하는 이미지 다시 받기와 강제 재배포 옵션을 설정해야 합니다.

![2023-11-24-image8](2023-11-24-image8.png)
_Portainer 자동 배포 실행_

---

## 전체 워크플로우

1. 코드 Push (Git)
2. Drone CI 파이프라인 실행
3. Docker 이미지 빌드
4. 이미지 레지스트리에 Push
5. Git의 이미지 태그 갱신 또는 이미지 재조회·강제 재배포 설정 확인
6. Portainer Webhook 호출
7. Portainer가 새 이미지로 컨테이너 재배포

**Webhook 호출 예시**

Portainer 화면에서 복사한 전체 URL을 Drone Secret `portainer_webhook_url`에 등록합니다. Stack과 서비스의 webhook 경로는 다를 수 있으므로 URL을 직접 조합하지 않습니다.

```yaml
- name: deploy
  image: curlimages/curl
  environment:
    PORTAINER_WEBHOOK_URL:
      from_secret: portainer_webhook_url
  commands:
    - curl --fail --show-error -X POST "$PORTAINER_WEBHOOK_URL"
  when:
    branch:
      - main
```

---

## 정리

Portainer는 웹 UI가 직관적이고 Drone의 빌드 완료 후 Webhook으로 배포를 연결할 수 있어 좋았어요. 다만 자동 업데이트의 변경 감지 조건과 사용 버전의 기능 범위를 먼저 확인해야 합니다.

개인적으로 Jenkins보다 Drone CI의 파이프라인 파일이 훨씬 깔끔해서 마음에 들었어요. 더 고급 기능이 필요하면 ArgoCD나 Flux 같은 도구도 있습니다.

## 참고 자료

- [Docker: Compose 네트워크와 서비스 이름](https://docs.docker.com/compose/how-tos/networking/)
- [Portainer: Stack 생성과 GitOps 업데이트](https://docs.portainer.io/user/docker/stacks/add)
- [Portainer: Stack Webhook](https://docs.portainer.io/user/docker/stacks/webhooks)
