---
title: Private Nexus Docker Repository 구축하기
last_modified_at: 2026-09-12 13:38:07 +0900
date: 2023-11-16 16:00:00 +0900
categories: [ENGINEERING, DEVOPS, Docker]
tags: [nexus, docker, repository, registry, private registry]
author: j-ho
img_path: /assets/img/for_post/
description: Nexus로 사내 Docker Private Repository를 구축하고 설정한 과정을 정리합니다.
---

Docker로 애플리케이션을 배포하다 보면 빌드한 이미지를 보관할 저장소가 필요하다. 이 글에서는 Nexus로 사내 전용 Docker 이미지 저장소를 구축하는 과정을 정리한다.

![2023-11-16-image1](2023-11-16-image1.png)
_Nexus Repository Manager_

---

## Nexus 서버 실행

아래는 Linux Docker Engine과 Compose v2에서 **외부에 공개하지 않고 Registry 동작을 확인하는 최소 실습**이다. 2023년 화면은 보존하고, 예시는 로컬 바인딩과 영속 볼륨을 사용하도록 보완했다. 원격 CI/CD에 연결할 때는 뒤에서 설명하는 TLS와 권한을 먼저 준비한다.

`.env`의 `NEXUS_IMAGE`에는 [공식 이미지](https://github.com/sonatype/docker-nexus3)의 버전 태그 또는 digest를 검토한 뒤 넣는다. 예를 들어 `NEXUS_IMAGE=sonatype/nexus3:<선택한-버전>`에서 꺾쇠 부분은 실제 게시된 태그로 바꾼다.

사용할 버전의 시스템 요구사항과 업그레이드 경로도 확인해야 한다. `latest`는 실행 시점마다 달라져 예전 DB에 새 버전이 예고 없이 연결될 수 있다.

`compose.yaml`:

```yaml
services:
  nexus:
    image: ${NEXUS_IMAGE:?Set a reviewed Nexus image tag or digest}
    volumes:
      - nexus_data:/nexus-data
    ports:
      - '127.0.0.1:8081:8081'
      - '127.0.0.1:8082:8082'
    restart: unless-stopped
    stop_grace_period: 120s

volumes:
  nexus_data:
```

- **8081**: 브라우저에서 접속할 포트 (웹 UI)
- **8082**: Docker Registry API를 이용할 때 필요한 포트

이 예시는 named volume을 사용한다. 기존처럼 호스트 디렉터리를 bind mount한다면 디렉터리를 미리 만들고 Nexus 프로세스(공식 이미지의 UID 200)가 쓸 수 있게 해야 한다. 설정·DB·이미지가 들어 있는 볼륨이므로 `docker compose down -v`로 지우지 않도록 주의한다.

```bash
docker compose config --quiet
docker compose up -d nexus
docker compose logs --tail=100 nexus
```

![2023-11-16-image3](2023-11-16-image3.png)
_Nexus 웹 UI 초기 화면_

---

## 초기 설정

로그에서 초기화 완료를 확인한 뒤 `http://localhost:8081`로 접속한다. 초기 관리자 비밀번호는 컨테이너 안의 파일에서 확인할 수 있다. 이 명령 출력과 비밀번호가 담긴 화면은 외부에 공유하지 않는다.

```bash
docker compose exec nexus cat /nexus-data/admin.password
```

![2023-11-16-image6](2023-11-16-image6.png)
_admin.password 파일 내용 확인_

로그인 후 새로운 비밀번호를 설정한다. 초기 관리자 계정은 설정에 사용하고, CI에서 push할 계정과 배포 서버에서 pull할 계정은 별도로 만든다. Realm 활성화와 계정에 repository 권한을 부여하는 작업은 별개다.

---

## Docker Repository 설정

### Blob Stores 생성

Blob Store는 실제 데이터를 저장하는 장소다. 여기서는 저장소 용도를 구분하기 위해 `hosted`, `proxy`라는 이름으로 만든다. 이 이름은 Blob Store 유형이 아니라 다음 단계에서 만들 Repository 용도를 나타낸다.

![2023-11-16-image12](2023-11-16-image12.png)
_Hosted Blob Store 생성_

### Repositories 생성

**Repository Type:**
- **Hosted**: private Docker image를 관리하는 repository
- **Proxy**: Docker Hub와 같은 외부 Repository 요청을 중계하고 이미지를 캐시하는 repository

docker(hosted)를 선택하고 HTTP 포트는 8082로 설정한다.

![2023-11-16-image16](2023-11-16-image16.png)
_Hosted Repository 설정_

Docker Hub 다운로드를 캐시하려면 선택적으로 docker(proxy)를 생성한다. Remote storage는 `https://registry-1.docker.io`다. hosted 저장소의 push/pull만 확인할 때는 proxy가 필요하지 않다.

![2023-11-16-image17](2023-11-16-image17.png)
_Proxy Repository 설정_

위 8082 포트는 hosted Repository 전용이다. proxy Repository도 Docker 클라이언트에서 이용하려면 별도 connector 포트를 설정해 공개하거나, hosted와 proxy를 묶은 group Repository의 connector로 접속해야 한다.

### Realms 설정

Docker Bearer Token Realm을 활성화해 Docker 클라이언트가 Nexus와 통신할 수 있도록 한다.

![2023-11-16-image18](2023-11-16-image18.png)
_Docker Bearer Token Realm 활성화_

### HTTP 실습과 원격 운영 구분

위 예시에서 Registry는 `127.0.0.1:8082`에만 열려 있다. Docker Engine은 loopback 주소를 기본적으로 insecure registry로 취급하므로, 같은 호스트에서는 `localhost:8082`로 진행할 수 있다.

다른 호스트의 HTTP Registry를 사용한다면 **이미지를 받거나 보내는 Docker daemon**에 해당 `host:port`를 명시해야 한다. 브라우저나 Nexus 컨테이너 안에서 설정하는 항목이 아니다. [Docker daemon의 insecure registry 설명](https://docs.docker.com/reference/cli/dockerd/#insecure-registries)

공유 서버의 `/etc/docker/daemon.json`을 예시 JSON으로 통째로 덮어쓰지 않는다. 필요한 키를 기존 설정과 병합하고 JSON 구문과 daemon 옵션을 검사한 뒤, 실행 중인 컨테이너에 미칠 영향을 고려해 재시작한다.

```bash
# Linux의 기본 설정 경로를 사용하는 경우
sudo dockerd --validate --config-file=/etc/docker/daemon.json
```

운영에서는 Registry 전용 도메인과 신뢰할 수 있는 TLS 인증서를 준비하고, 리버스 프록시 또는 Nexus HTTPS connector를 통해 제공한다. UI 포트 8081과 Registry connector 포트 8082를 혼동하지 않도록 한다. private CA를 사용한다면 Docker daemon이 그 CA를 신뢰하도록 설정하며 TLS 검증을 꺼서 해결하지 않는다. [Sonatype의 reverse proxy 구성 방식](https://help.sonatype.com/en/docker-repository-reverse-proxy-strategies.html)

원격에 공개할 때는 프록시 upstream과 방화벽도 조정해야 한다. 예시의 loopback 바인딩은 다른 호스트에서 직접 연결할 수 없도록 의도한 설정이다.

---

## 동작 테스트

같은 Docker 호스트에서 실행한다. push 권한이 있는 전용 사용자를 준비한 뒤, 명령이 묻는 비밀번호를 입력한다. `docker login` 주소에는 스킴이나 `/repository/...` 경로를 넣지 않는다.

{% raw %}
```bash
docker login localhost:8082 --username ci-publisher
docker pull alpine:3.24
docker tag alpine:3.24 localhost:8082/demo/alpine:v1
docker push localhost:8082/demo/alpine:v1

# 로컬 태그를 제거한 뒤 Registry에서 다시 받아 경로를 확인
docker image rm localhost:8082/demo/alpine:v1
docker pull localhost:8082/demo/alpine:v1
docker image inspect localhost:8082/demo/alpine:v1 --format '{{json .RepoDigests}}'
```
{% endraw %}

push 결과의 digest와 다시 pull한 digest를 비교한다. 로컬 레이어가 남아 있으면 다운로드를 재사용할 수 있으므로 완전히 새 클라이언트에서도 pull을 확인하면 더 명확하다. 배포용 pull 전용 계정으로는 pull이 성공하고 push가 거절되는지도 점검한다.

![2023-11-16-image22](2023-11-16-image22.png)
_Nexus에 업로드된 이미지 확인_

---

## 실패 지점을 나눠 확인하기

| 증상 | 확인할 내용 |
| --- | --- |
| UI도 열리지 않음 | Nexus 초기화 로그, 메모리, 볼륨 권한 |
| `/v2/`가 404 또는 HTML 반환 | UI 포트로 보냈는지, hosted connector·프록시 경로 |
| HTTPS 요청에 HTTP 응답 오류 | 실제 TLS 구성과 daemon의 HTTP 실습 설정 불일치 |
| login 성공, push 실패 | hosted 주소인지, 해당 repository의 쓰기 권한인지 |
| 재배포 후 데이터가 사라짐 | 이전과 같은 영속 볼륨을 연결했는지 |

인증이 필요한 `/v2/` 요청의 `401`과 인증 challenge는 정상 흐름의 일부일 수 있다. 상태 코드 하나만 보고 서버가 고장 났다고 판단하지 않고, login부터 이어지는 전체 흐름을 확인한다.

## 정리

**구축 단계**
1. Docker Compose로 Nexus 서버 실행
2. 초기 비밀번호 확인 및 관리자 계정 설정
3. hosted Repository와 저장용 Blob Store 생성
4. 필요한 경우에만 proxy·group 추가
5. Docker Bearer Token Realm과 계정별 권한 설정
6. 로컬 HTTP 실습 또는 원격 TLS 구성
7. digest와 권한을 포함한 push/pull 검증

실제 운영에서는 DB와 Blob Store를 일관된 시점으로 복원할 수 있도록 사용하는 버전의 백업 절차를 따른다. 볼륨이 있다고 해서 백업까지 보장되지는 않는다.

Cleanup Policy를 적용하기 전에는 배포 중이거나 롤백에 필요한 이미지가 삭제되지 않도록 보존 기준을 정하고, 실제 용량 회수에 필요한 작업도 해당 버전 문서에서 확인한다.

이렇게 구축한 Private Registry는 CI/CD 파이프라인에서 Jenkins나 Drone으로 빌드한 이미지를 Push하고, 배포할 때 Pull하는 용도로 사용할 수 있다.

## 참고 자료

- [Sonatype: Nexus 공식 Docker 이미지](https://github.com/sonatype/docker-nexus3)
- [Sonatype: Repository Connector 설정](https://help.sonatype.com/en/configurable-repository-fields.html)
- [Sonatype: Docker Repository 그룹](https://help.sonatype.com/en/grouping-docker-repositories.html)

- [Sonatype: Docker 인증과 Realm](https://help.sonatype.com/en/docker-authentication.html)
- [Docker: daemon 설정 검증](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file)
