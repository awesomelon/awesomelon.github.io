---
title: Private Nexus Docker Repository 구축하기
date: 2023-11-16 16:00:00 +0900
categories: [ENGINEERING, DEVOPS, Docker]
tags: [nexus, docker, repository, registry, private registry]
author: j-ho
img_path: /assets/img/for_post/
description: Nexus를 활용하여 사내에서 사용할 수 있는 Docker Private Repository를 구축하고 설정하는 전체 과정을 알아봅니다.
---

애플리케이션을 Docker를 이용해 배포하다보면 Docker Build 후 생성된 Docker Image를 관리할 수 있는 Repository가 필요합니다. 이번 시간엔 Nexus를 이용한 사내 Docker Private Repository를 구축해보겠습니다.

![2023-11-16-image1](2023-11-16-image1.png)
_Nexus Repository Manager_

## Nexus 서버 실행

Nexus의 서버를 띄우는 건 Docker Compose 파일로 간단하게 하실 수 있습니다.

> Docker와 Docker Compose의 설치는 필수입니다.
{: .prompt-info }
```yaml
# docker-compose.yml
version: '3.2'

services:
  nexus:
    image: sonatype/nexus3
    volumes:
      - /nexus-data:/nexus-data
    ports:
      - 8081:8081
      - 8082:8082
```

**포트 설명:**
- **8081**: 브라우저에서 접속할 포트 (웹 UI)
- **8082**: Docker Registry API를 이용할 때 필요한 포트

위의 docker-compose 파일이 있는 경로에서 아래 명령어를 실행해줍니다.
```bash
docker-compose up nexus -d
```

![2023-11-16-image2](2023-11-16-image2.png)
_Nexus 컨테이너 실행_

이제 브라우저에서 접속해봅시다. (`http://localhost:8081`)

![2023-11-16-image3](2023-11-16-image3.png)
_Nexus 웹 UI 초기 화면_

## 초기 설정

### 관리자 비밀번호 확인

로그인을 위해서는 초기 비밀번호를 알아야합니다.

![2023-11-16-image4](2023-11-16-image4.png)
_초기 비밀번호 안내_

비밀번호는 위에서 설정한 volume 폴더에서 확인하실 수도 있고, 컨테이너 내부의 `/nexus-data` 폴더에서도 확인하실 수 있습니다.

#### 방법 1: Volume 폴더에서 확인

지정한 Volume 폴더로 이동 후 비밀번호를 확인합니다.

![2023-11-16-image5](2023-11-16-image5.png)
_Volume 폴더 경로_

![2023-11-16-image6](2023-11-16-image6.png)
_admin.password 파일 내용 확인_

#### 방법 2: Container 내부에서 확인

Nexus의 Container ID를 확인합니다.

![2023-11-16-image7](2023-11-16-image7.png)
_실행 중인 컨테이너 확인_

Container 내부에 접속합니다.

![2023-11-16-image8](2023-11-16-image8.png)
_컨테이너 내부 접속_

비밀번호를 확인합니다.

![2023-11-16-image9](2023-11-16-image9.png)
_컨테이너 내부에서 비밀번호 확인_

### 비밀번호 변경

위에서 확인한 비밀번호로 로그인을 하면 새로운 비밀번호를 설정하라는 팝업이 뜹니다.

![2023-11-16-image10](2023-11-16-image10.png)
_새 비밀번호 설정_

계정 설정이 끝이 났습니다. 이제 본격적으로 Docker Repository를 설정해보겠습니다.

## Docker Repository 설정

### Blob Stores 생성

우선 Blob Store를 생성해줍니다. Blob Store는 실제 데이터가 저장될 장소입니다.

저장소는 로컬에서 생성한 이미지가 저장될 **hosted**와 외부에서 가져올 **proxy**가 필요합니다.

#### Hosted Blob Store 생성

먼저 `hosted`를 생성합니다.

![2023-11-16-image11](2023-11-16-image11.png)
_Blob Stores 메뉴_

![2023-11-16-image12](2023-11-16-image12.png)
_Hosted Blob Store 생성_

#### Proxy Blob Store 생성

같은 방식으로 `proxy`를 생성합니다.

![2023-11-16-image13](2023-11-16-image13.png)
_Proxy Blob Store 생성_

### Repositories 생성

**Repository Type:**
- **Hosted**: 기본 Type으로 private Docker image를 관리하는 repository입니다
- **Proxy**: Global Repository처럼 외부 Repository에 대해 Proxy 역할을 합니다

#### Hosted Repository 생성

먼저 `hosted`부터 생성해보겠습니다. 우선 `Create repository` 버튼을 클릭합니다.

![2023-11-16-image14](2023-11-16-image14.png)
_Repository 생성 버튼_

그 후 `docker(hosted)`를 선택합니다.

![2023-11-16-image15](2023-11-16-image15.png)
_Docker Hosted Repository 선택_

아래 표기된 필드를 입력해줍니다.

![2023-11-16-image16](2023-11-16-image16.png)
_Hosted Repository 설정_

> HTTP 포트는 앞서 docker-compose에서 설정한 8082를 사용합니다.
{: .prompt-tip }

#### Proxy Repository 생성

이어서 `docker(proxy)`를 생성해보겠습니다. 아래 필드를 입력해주시면 됩니다.

Remote storage는 Docker Hub의 URL입니다: `https://registry-1.docker.io`

![2023-11-16-image17](2023-11-16-image17.png)
_Proxy Repository 설정_

### Realms 설정

Docker Repository에 접근할 수 있는 인증을 추가합니다. 이는 Docker Bearer Token Realm에서 제공하는 기본적인 인증 권한을 사용해 익명으로 docker pull을 허용합니다.

![2023-11-16-image18](2023-11-16-image18.png)
_Docker Bearer Token Realm 활성화_

> Docker Bearer Token Realm을 활성화하여 Docker 클라이언트가 Nexus와 통신할 수 있도록 합니다.
{: .prompt-info }

### Insecure-registries 설정

위에서 설정한 작업만으로는 docker image를 push하거나 pull할 때 아래와 같은 에러가 발생할 것입니다.

![2023-11-16-image19](2023-11-16-image19.png)
_SSL 인증서 에러_

이는 Docker에 이미지를 push하거나 할 때 필수 조건이 SSL 설정이라서 그렇습니다.

하지만 사내용으로 쓸 때는 외부에서 접근 불가능한 네트워크에 보통 구성하기 때문에 SSL이 필요 없을 수도 있습니다. 그 때 설정할 것이 `insecure-registries` 설정입니다.

설정은 간단합니다. 도커 엔진의 설정파일이라고 할 수 있는 `daemon.json`에 `insecure-registries` 설정을 추가하기만 하면 됩니다.

말 그대로 보안 설정을 `passing`하는 레지스트리를 등록하는 것입니다.
```bash
# 파일이 없다면 생성해줍니다.
vi /etc/docker/daemon.json
```
```json
{
  "insecure-registries": ["{IP Address}:8082"]
}
```

> **주의:** Production 환경에서는 반드시 SSL/TLS 인증서를 설정하여 사용하는 것을 권장합니다.
{: .prompt-warning }

설정 완료 후 도커를 재시작해줍니다.
```bash
service docker restart
```

### 동작 테스트

이제 설정이 완료되었으니 테스트를 해봅시다. 먼저 `docker login`을 해보겠습니다.
```bash
docker login {IP Address}:8082
```

`insecure-registries`를 설정하기 전엔 에러를 뱉어내던 것이 이제 정상적으로 로그인이 됩니다.

![2023-11-16-image20](2023-11-16-image20.png)
_Docker login 성공_

#### Image Pull 테스트

테스트로 docker image를 하나 Docker Hub에서 받아봅니다.
```bash
docker pull busybox
```

![2023-11-16-image21](2023-11-16-image21.png)
_Busybox 이미지 다운로드_

#### Image Push 테스트

받은 이미지를 구축한 Nexus repository에 push합니다.
```bash
docker tag {image ID} {IP Address}:8082/busybox:v1
docker push {IP Address}:8082/busybox:v1
```

Nexus에서 push된 이미지를 확인합니다.

![2023-11-16-image22](2023-11-16-image22.png)
_Nexus에 업로드된 이미지 확인_

## 정리

Nexus Docker Private Repository 구축 과정 요약:

### 구축 단계

| 단계 | 작업 내용 |
|:---:|:---|
| **1** | Docker Compose로 Nexus 서버 실행 |
| **2** | 초기 비밀번호 확인 및 관리자 계정 설정 |
| **3** | Blob Stores 생성 (hosted, proxy) |
| **4** | Repositories 생성 (hosted, proxy) |
| **5** | Realms 설정 (Docker Bearer Token) |
| **6** | Insecure-registries 설정 |
| **7** | Docker login 및 이미지 push/pull 테스트 |

### Repository 유형

**Hosted Repository:**
- 사내에서 빌드한 이미지 저장
- Private Docker Image 관리
- 직접 push/pull 가능

**Proxy Repository:**
- Docker Hub 등 외부 Registry 캐싱
- 네트워크 대역폭 절약
- 이미지 다운로드 속도 향상

### 핵심 설정

**포트 구성:**
```yaml
ports:
  - 8081:8081  # Web UI
  - 8082:8082  # Docker Registry API
```

**Insecure Registry 설정:**
```json
{
  "insecure-registries": ["your-nexus-ip:8082"]
}
```

**이미지 태깅 및 Push:**
```bash
docker tag {image} {nexus-ip}:8082/{image-name}:{tag}
docker push {nexus-ip}:8082/{image-name}:{tag}
```

### 운영 시 고려사항

**보안:**
- Production 환경에서는 SSL/TLS 인증서 필수
- 사용자 권한 관리 (Role-based Access Control)
- 정기적인 백업 (/nexus-data)

**성능:**
- Blob Store 용량 모니터링
- Cleanup Policies 설정 (오래된 이미지 자동 삭제)
- Proxy Repository 캐시 최적화

**유지보수:**
- Nexus 버전 업그레이드 계획
- 로그 모니터링
- 디스크 공간 관리

### 활용 예시

**CI/CD 파이프라인 통합:**
1. Jenkins/Drone에서 이미지 빌드
2. Nexus Private Registry에 Push
3. Kubernetes/Docker에서 이미지 Pull
4. 배포 자동화

**장점:**
- 외부 의존성 감소
- 이미지 버전 관리 용이
- 빌드 속도 향상 (캐싱)
- 내부 네트워크에서 빠른 접근

Private Nexus Docker Repository를 구축해보았습니다. 도움이 되었으면 좋겠습니다.