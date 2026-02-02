---
title: Private Nexus Docker Repository 구축하기
date: 2023-11-16 16:00:00 +0900
categories: [ENGINEERING, DEVOPS, Docker]
tags: [nexus, docker, repository, registry, private registry]
author: j-ho
img_path: /assets/img/for_post/
description: Nexus를 활용하여 사내에서 사용할 수 있는 Docker Private Repository를 구축하고 설정하는 전체 과정을 알아봅니다.
---

애플리케이션을 Docker를 이용해 배포하다보면 Docker Build 후 생성된 Docker Image를 관리할 수 있는 Repository가 필요해요. Nexus를 이용한 사내 Docker Private Repository를 구축해보겠습니다.

![2023-11-16-image1](2023-11-16-image1.png)
_Nexus Repository Manager_

---

## Nexus 서버 실행

Docker Compose로 간단하게 서버를 띄워요.

```yaml
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

- **8081**: 브라우저에서 접속할 포트 (웹 UI)
- **8082**: Docker Registry API를 이용할 때 필요한 포트

```bash
docker-compose up nexus -d
```

![2023-11-16-image3](2023-11-16-image3.png)
_Nexus 웹 UI 초기 화면_

---

## 초기 설정

초기 비밀번호는 volume 폴더에서 확인하거나 컨테이너 내부의 `/nexus-data/admin.password`에서 확인할 수 있습니다.

![2023-11-16-image6](2023-11-16-image6.png)
_admin.password 파일 내용 확인_

로그인 후 새로운 비밀번호를 설정합니다.

---

## Docker Repository 설정

### Blob Stores 생성

Blob Store는 실제 데이터가 저장될 장소입니다. 로컬에서 생성한 이미지가 저장될 hosted와 외부에서 가져올 proxy를 생성합니다.

![2023-11-16-image12](2023-11-16-image12.png)
_Hosted Blob Store 생성_

### Repositories 생성

**Repository Type:**
- **Hosted**: private Docker image를 관리하는 repository
- **Proxy**: Docker Hub와 같은 외부 Repository에 대해 Proxy 역할

docker(hosted)를 선택하고 HTTP 포트는 8082를 설정합니다.

![2023-11-16-image16](2023-11-16-image16.png)
_Hosted Repository 설정_

docker(proxy)를 생성할 때 Remote storage는 Docker Hub의 URL입니다: `https://registry-1.docker.io`

![2023-11-16-image17](2023-11-16-image17.png)
_Proxy Repository 설정_

### Realms 설정

Docker Bearer Token Realm을 활성화하여 Docker 클라이언트가 Nexus와 통신할 수 있도록 해요.

![2023-11-16-image18](2023-11-16-image18.png)
_Docker Bearer Token Realm 활성화_

### Insecure-registries 설정

사내용으로 SSL이 필요 없는 경우 `insecure-registries` 설정을 추가합니다.

```bash
vi /etc/docker/daemon.json
```

```json
{
  "insecure-registries": ["{IP Address}:8082"]
}
```

> Production 환경에서는 반드시 SSL/TLS 인증서를 설정하여 사용하는 것을 권장합니다.
{: .prompt-warning }

Docker를 재시작해요.

```bash
service docker restart
```

---

## 동작 테스트

```bash
# 로그인
docker login {IP Address}:8082

# 이미지 다운로드
docker pull busybox

# 태그 및 Push
docker tag {image ID} {IP Address}:8082/busybox:v1
docker push {IP Address}:8082/busybox:v1
```

![2023-11-16-image22](2023-11-16-image22.png)
_Nexus에 업로드된 이미지 확인_

---

## 정리

**구축 단계**
1. Docker Compose로 Nexus 서버 실행
2. 초기 비밀번호 확인 및 관리자 계정 설정
3. Blob Stores 생성 (hosted, proxy)
4. Repositories 생성 (hosted, proxy)
5. Realms 설정 (Docker Bearer Token)
6. Insecure-registries 설정
7. Docker login 및 이미지 push/pull 테스트

**운영 시 고려사항**
- Production 환경에서는 SSL/TLS 인증서 필수
- 사용자 권한 관리 (Role-based Access Control)
- 정기적인 백업 (/nexus-data)
- Blob Store 용량 모니터링
- Cleanup Policies 설정 (오래된 이미지 자동 삭제)

**활용:**
CI/CD 파이프라인에서 Jenkins/Drone으로 이미지를 빌드하고, Nexus Private Registry에 Push한 뒤, Kubernetes/Docker에서 이미지를 Pull하여 배포를 자동화할 수 있습니다.
