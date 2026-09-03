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

Portainer는 Server와 Agent 두 가지 요소로 구성됩니다. 클러스터 내의 각 노드에 Agent를 설치하고 Server는 여러 Agent의 연결을 수용하여 하나의 중앙화된 인터페이스에서 여러 클러스터를 관리할 수 있습니다.

![2023-11-24-image1](2023-11-24-image1.png)
_Portainer 아키텍처 구조_

---

## Portainer 설치

Docker Compose로 Server와 Agent를 컨테이너로 띄워요.

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

컨테이너를 시작한 후 브라우저로 접속하면 현재 Portainer Server와 연동된 클러스터들을 볼 수 있어요.

![2023-11-24-image2](2023-11-24-image2.png)
_Portainer 환경 목록_

![2023-11-24-image3](2023-11-24-image3.png)
_Docker 환경 대시보드_

---

## Stack 생성 및 GitOps 설정

Stack이란 다중 컨테이너 애플리케이션의 묶음입니다. docker-compose로 컨테이너를 여러 개 띄웠을 시 그 여러 개를 합쳐서 하나의 Stack이라고 부릅니다.

Add Stack 버튼을 클릭하고 Stack 정보를 입력해요.

![2023-11-24-image5](2023-11-24-image5.png)
_Stack 생성 화면_

**주요 설정**
- **Build Method**: Web editor, Upload, Git Repository 중 선택 (GitOps를 위해 Git Repository 권장)
- **Repository URL**: 변경된 사항이 있는지 감지할 저장소 주소
- **username, personal access token**: 저장소 인증 정보

> Web editor와 upload는 자동배포가 불가능합니다. GitOps를 위해서는 Git Repository 방식을 사용해야 합니다.
{: .prompt-warning }

Portainer는 Polling 방식(일정 시간마다 저장소 체크)과 Webhook 방식(요청을 받으면 즉시 배포)을 지원합니다. Polling은 유료 기능이므로 Webhook 방식을 사용했습니다.

![2023-11-24-image6](2023-11-24-image6.png)
_자동 배포 설정_

---

## CI/CD 파이프라인 동작

Drone CI에서 Docker 빌드가 완료된 후 Portainer Server의 Webhook으로 요청을 보냅니다.

![2023-11-24-image7](2023-11-24-image7.png)
_Drone CI 파이프라인 실행_

요청을 받은 Portainer Server는 해당 Stack에서 변경된 이미지가 있는 컨테이너를 확인하여 새로 띄웁니다.

![2023-11-24-image8](2023-11-24-image8.png)
_Portainer 자동 배포 실행_

---

## 전체 워크플로우

1. 코드 Push (Git)
2. Drone CI 파이프라인 실행
3. Docker 이미지 빌드
4. 이미지 레지스트리에 Push
5. Portainer Webhook 호출
6. Portainer가 새 이미지로 컨테이너 재배포

**Webhook 호출 예시**

```yaml
- name: deploy
  image: curlimages/curl
  commands:
    - curl -X POST https://portainer.example.com/api/webhooks/xxxx
  when:
    branch:
      - main
```

---

## 정리

Portainer는 웹 UI가 직관적이고 Webhook으로 무료 자동 배포가 가능해서 좋았어요. 다만 Polling 자동 배포는 유료이고 Blue-Green이나 Canary 같은 배포 전략은 지원이 제한적입니다.

개인적으로 Jenkins보다 Drone CI의 파이프라인 파일이 훨씬 깔끔해서 마음에 들었어요. 더 고급 기능이 필요하면 ArgoCD나 Flux 같은 도구도 있습니다.
