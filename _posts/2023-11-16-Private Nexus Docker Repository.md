---
title: Private Nexus Docker Repository 구축하기
date: 2023-11-16 16:00:00 +0900
categories: [ENGINEERING, DEVOPS, Docker]
tags: [nexus, docker, repository, registry, private registry]
author: j-ho
img_path: /assets/img/for_post/
description: Nexus로 사내 Docker Private Repository를 구축하고 설정한 과정을 정리합니다.
---

애플리케이션을 Docker를 이용해 배포하다 보면 Docker Build 후 생성된 Docker Image를 관리할 수 있는 Repository가 필요해요. Nexus를 이용한 사내 Docker Private Repository를 구축해보겠습니다.

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

호스트의 `/nexus-data` 디렉터리는 미리 만들고 Nexus 프로세스(공식 이미지의 UID 200)가 쓸 수 있는 권한을 부여해야 합니다. 그렇지 않으면 데이터 디렉터리 권한 오류로 시작하지 못할 수 있어요.

```bash
docker-compose up -d nexus
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

Blob Store는 실제 데이터가 저장될 장소입니다. 여기서는 저장소 용도를 구분하기 위해 `hosted`, `proxy`라는 이름으로 만듭니다. 이 이름은 Blob Store의 유형이 아니라 다음 단계에서 만들 Repository의 용도를 나타내요.

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

위의 8082 포트는 hosted Repository 전용입니다. proxy Repository도 Docker 클라이언트에서 이용하려면 별도 connector 포트를 설정해 공개하거나, hosted와 proxy를 묶은 group Repository의 connector로 접속해야 합니다.

### Realms 설정

Docker Bearer Token Realm을 활성화하여 Docker 클라이언트가 Nexus와 통신할 수 있도록 해요.

![2023-11-16-image18](2023-11-16-image18.png)
_Docker Bearer Token Realm 활성화_

### Insecure-registries 설정

TLS를 설정하지 않은 HTTP Registry로 테스트할 때는 Docker 클라이언트 측에 `insecure-registries` 설정을 추가합니다. 사내용이라는 이유만으로 암호화가 불필요한 것은 아니에요.

```bash
vi /etc/docker/daemon.json
```

```json
{
  "insecure-registries": ["{IP Address}:8082"]
}
```

> Production 환경에서는 SSL/TLS 인증서를 설정해 사용하는 게 좋습니다.
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

# Nexus hosted Repository에서 다운로드
docker pull {IP Address}:8082/busybox:v1
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

실제 운영할 때는 SSL/TLS 인증서 적용, 사용자 권한 관리, `/nexus-data` 백업, Blob Store 용량 모니터링 정도는 챙겨야 합니다. Cleanup Policies로 오래된 이미지를 자동 삭제하는 설정도 해두면 좋아요.

이렇게 구축한 Private Registry는 CI/CD 파이프라인에서 Jenkins나 Drone으로 빌드한 이미지를 Push하고 배포 시 Pull하는 용도로 사용할 수 있습니다.

## 참고 자료

- [Sonatype: Nexus 공식 Docker 이미지](https://github.com/sonatype/docker-nexus3)
- [Sonatype: Repository Connector 설정](https://help.sonatype.com/en/configurable-repository-fields.html)
- [Sonatype: Docker Repository 그룹](https://help.sonatype.com/en/grouping-docker-repositories.html)
