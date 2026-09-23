---
title: Drone CI와 Portainer를 이용한 CI/CD 구축하기
last_modified_at: 2026-09-12 13:38:07 +0900
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

빌드한 이미지와 실제 서비스가 실행 중인 이미지가 다르면 CI가 초록색이어도 배포는 성공한 것이 아닙니다. 이 글에서는 Drone의 이미지 빌드·push와 Portainer의 Stack 업데이트를 연결하고, 그 사이에서 변경을 놓치지 않는 방법을 정리합니다.

> 화면은 2023년 구축 당시의 기록입니다. 설치·예시는 2026년 문서를 참고해 보완했습니다. Docker Standalone 기준이며, Swarm의 무중단 업데이트 설정이나 Kubernetes 배포를 그대로 설명하는 예시는 아닙니다.
{: .prompt-info }

## Portainer란?

[Portainer](https://www.portainer.io)는 Kubernetes, Docker, Swarm 등을 쉽게 배포하고 관리할 수 있는 경량화된 관리 도구예요. 웹 UI를 제공하며 실행 중인 컨테이너, 이미지, 볼륨 등을 직관적으로 확인하고 관리할 수 있습니다.

Portainer는 Server와 Agent를 이용해 여러 환경을 중앙에서 관리할 수 있습니다. Docker Swarm에서는 각 노드에 Agent를 배치하는 구성을 사용할 수 있고, 단일 Docker 환경에서는 로컬 소켓으로 직접 연결하는 방식도 가능합니다.

![2023-11-24-image1](2023-11-24-image1.png)
_Portainer 아키텍처 구조_

---

## Portainer 설치

한 대의 Linux Docker 호스트를 관리할 때는 Server가 로컬 Docker socket에 직접 연결하는 구성이 가장 단순합니다. 아래는 [Portainer CE 설치 문서](https://docs.portainer.io/start/install-ce/server/docker/linux)를 바탕으로 한 `compose.yaml`입니다. 여러 호스트를 관리할 때 Agent를 추가하고, Swarm에서는 별도의 전역 Agent 배포 구성을 사용합니다.

```yaml
services:
  portainer:
    image: ${PORTAINER_IMAGE:?Set a reviewed Portainer image tag or digest}
    ports:
      - '127.0.0.1:9443:9443'
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    restart: unless-stopped

volumes:
  portainer_data:
```

`.env`에 `PORTAINER_IMAGE=portainer/portainer-ce:lts`를 설정하면 공식 문서의 LTS 계열 이미지로 시작할 수 있습니다. `lts`도 이동하는 태그이므로 운영 전에는 검토한 정확한 버전 또는 digest로 고정합니다.

```bash
docker compose config --quiet
docker compose up -d
docker compose ps
docker compose logs --tail=100 portainer
```

같은 호스트에서 `https://localhost:9443`으로 접속합니다. 원격 관리 시에는 관리망의 TLS 프록시나 SSH 터널을 사용하고, 초기 관리자 설정을 완료합니다. 현재 버전에서 setup token을 요구하면 설치 문서의 초기 설정 절차를 따릅니다.

기본 9443 인증서는 자체 서명 인증서이므로, CI의 webhook 호출에 사용하려면 신뢰 가능한 인증서 또는 private CA 신뢰 구성이 필요합니다. `curl -k`로 검증을 건너뛰는 방법을 배포 예시에 넣지는 않습니다. 레거시 HTTP 9000과 Edge Agent용 8000은 이 구성에 필요하지 않아 공개하지 않았어요.

Portainer와 Runner는 Docker 제어 권한을 갖습니다. 관리 UI와 webhook의 접근 경로를 필요한 운영자·CI로 제한하고, Agent를 추가한다면 Server와 호환되는 버전 및 접근 제한도 함께 구성해야 합니다.

컨테이너를 시작한 후 브라우저로 접속하면 Portainer와 연결된 환경들을 볼 수 있어요. 단일 Docker 호스트도 하나의 Environment이며, 모두 클러스터인 것은 아닙니다.

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
- **Repository reference / Compose path**: 배포할 브랜치와 저장소 루트 기준 Compose 파일 경로
- **저장소 인증**: 사용하는 Git provider와 Portainer 버전에 맞는 읽기 권한의 인증 정보

> Git 저장소의 Compose 파일을 기준으로 자동 업데이트하려면 Git Repository 방식을 선택합니다. 2026년 확인한 문서에서 일반적인 **Stack Webhook**은 Business Edition 기능으로 안내합니다. 이를 Git Repository의 **GitOps updates**와 같은 기능으로 보고 CE에서 모든 webhook을 쓸 수 있다고 가정하지 않습니다. 설치 버전·에디션의 GitOps 설정 화면에서 사용 가능한 방식을 확인합니다.
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

## 무엇을 배포할지 Git에 남기기

같은 `latest` 태그에 새 이미지를 덮어쓰는 방식은 구현하기 편하지만, Git만 보고 실제 배포 내용을 복원하기 어렵습니다. 보완안으로 이미지에 커밋 SHA 태그를 붙이고, push가 완료된 뒤 배포용 Compose의 `image`를 그 태그 또는 digest로 바꾸는 방식을 권합니다.

| 단계 | 남겨야 할 결과 |
| --- | --- |
| 애플리케이션 빌드·검증 | 소스 커밋과 테스트 결과 |
| Registry push | 이미지 digest, 성공 여부 |
| 배포 설정 갱신 | 그 이미지를 가리키는 Compose 커밋 |
| Portainer 업데이트 요청 | 확인할 배포 설정 커밋 |
| 실제 서비스 검증 | 실행 이미지와 응답·상태 검사 결과 |

이렇게 하면 webhook은 “어떤 이미지인지 모르는 최신 상태를 가져오라”가 아니라 “Git에 기록한 상태를 확인하라”는 신호가 됩니다. 단, 커밋 SHA로 이름 붙인 태그도 덮어쓸 수 있으므로 레지스트리의 불변 태그 정책 또는 digest가 필요합니다.

이 순서는 배포용 설정을 CI가 갱신하도록 **추가 구현해야 하는 보완안**입니다. 아래 webhook 단계만 복사하면 이미지 push와 Git 커밋까지 자동으로 생기는 것은 아니에요. 애플리케이션과 배포 설정을 같은 저장소에 두면 CI의 설정 커밋이 다시 빌드를 촉발하지 않도록 트리거를 구분합니다.

[Portainer의 변경 감지 설명](https://docs.portainer.io/faqs/troubleshooting/stacks-deployments-and-updates/how-do-automatic-updates-for-stacks-applications-work)에 따르면 기본 경로는 Git 커밋을 비교합니다. 같은 태그를 꼭 유지해야 한다면 사용 버전에서 re-pull과 force redeployment를 지원하는지, 각각 어떤 조건에서 동작하는지 따로 확인합니다.

## 전체 워크플로우

1. 코드 Push (Git)
2. Drone CI 파이프라인 실행
3. Docker 이미지 빌드
4. 이미지 레지스트리에 Push
5. push에 성공한 이미지의 태그·digest로 Git의 배포 설정 갱신
6. Portainer Webhook 호출
7. Portainer가 새 이미지로 컨테이너 재배포
8. 실행 이미지와 서비스 응답을 확인해 배포 완료 판정

**Webhook 호출 예시**

Portainer의 **선택한 Stack에 대한 GitOps 설정**에서 복사한 전체 URL을 Drone Secret `portainer_webhook_url`에 등록합니다. Stack·서비스·GitOps webhook을 섞어 URL을 직접 조합하지 않습니다. URL 자체가 실행 권한을 갖는 비밀로 취급되어야 하므로 코드와 로그에 노출하지 않습니다.

다음은 이미지 push와 배포 설정 커밋이 **이미 성공한 파이프라인의 마지막 step**에 추가할 조각입니다. curl 컨테이너 버전은 보완 시점의 [공식 릴리스](https://github.com/curl/curl-container/releases/tag/8.22.0)를 명시했습니다.

```yaml
- name: deploy
  image: curlimages/curl:8.22.0
  environment:
    PORTAINER_WEBHOOK_URL:
      from_secret: portainer_webhook_url
  commands:
    - set +x
    - curl --fail --silent --show-error --connect-timeout 10 --max-time 60 -X POST "$PORTAINER_WEBHOOK_URL"
  when:
    branch:
      - main
    event:
      - push
    status:
      - success
```

---

## webhook 성공과 배포 성공 구분하기

HTTP 성공 응답은 요청을 받았다는 신호일 뿐, 새 컨테이너가 정상 서비스를 제공한다는 보장은 아닙니다. Registry 접근 실패, 잘못된 Compose 경로, 애플리케이션 기동 실패가 그 뒤에 발생할 수 있어요.

배포 후에는 Portainer에서 Stack의 이벤트와 컨테이너 상태를 확인하고, 실행 이미지가 의도한 digest인지 비교합니다. 서비스의 읽기 전용 상태 확인 URL과 대표 사용자 요청도 점검해요. Docker의 `running` 상태만으로 애플리케이션 준비가 끝났다고 판단하지 않습니다.

실패하면 이전 배포 설정 커밋이 가리키는 이미지로 되돌린 뒤 같은 검증을 수행합니다. 이때 이전 이미지가 Registry에 남아 있어야 하며, DB 스키마를 변경한 배포는 코드 롤백만으로 복구되지 않을 수 있습니다. 두 빌드가 동시에 끝날 때 오래된 빌드의 배포가 나중에 덮어쓰지 않도록 환경별 배포를 직렬화하는 것도 필요해요.

현재 예시는 단일 호스트이므로 무중단이나 고가용성을 보장하지 않습니다. **CI 성공 → 업데이트 요청 성공 → 서비스 정상**의 세 결과를 구분해 관찰할 수 있을 때 자동 배포를 운영할 수 있습니다.

## 정리

Portainer는 웹 UI가 직관적이고 Drone의 빌드 완료 후 Webhook으로 배포를 연결할 수 있어 좋았어요. 다만 자동 업데이트의 변경 감지 조건과 사용 버전의 기능 범위를 먼저 확인해야 합니다.

개인적으로 Jenkins보다 Drone CI의 파이프라인 파일이 훨씬 깔끔해서 마음에 들었어요. Kubernetes에서 지속적인 상태 조정이 필요하다면 Argo CD나 Flux를 별도로 검토할 수 있지만, 이 단일 Docker 환경의 구성에 바로 바꿔 끼우는 도구는 아닙니다.

## 참고 자료

- [Docker: Compose 네트워크와 서비스 이름](https://docs.docker.com/compose/how-tos/networking/)
- [Portainer: Stack 생성과 GitOps 업데이트](https://docs.portainer.io/user/docker/stacks/add)
- [Portainer: Stack Webhook](https://docs.portainer.io/user/docker/stacks/webhooks)

- [Portainer: CE의 Docker 설치](https://docs.portainer.io/start/install-ce/server/docker/linux)
- [Portainer: 자동 업데이트의 변경 감지](https://docs.portainer.io/faqs/troubleshooting/stacks-deployments-and-updates/how-do-automatic-updates-for-stacks-applications-work)
- [Drone: branch·event·status 조건](https://docs.drone.io/pipeline/docker/syntax/conditions/)
