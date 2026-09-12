# 블로그 포스팅 내용 평가 및 개선 기록

- 검토일: 2026-09-12
- 원문 기준: `0306ec6b14586104009b78216bac8549f6cb405e`
- 범위: `_posts`의 전체 42편. 원래 파일명과 게시 경로를 유지했다.
- 동일 기준 평균: **7.23/10 → 9.29/10**

## 평가 방법

“12점”은 기대 이상의 완성도를 지향하는 목표로 해석했다. 실제 점수는 아래 다섯 항목을 각각 0–2점으로 평가한 10점 척도다. 원문과 개선본에 같은 기준을 적용했다. 점수는 편집·기술 검토에 따른 판단이며, 독자 조사나 실제 서비스 성과를 측정한 결과가 아니다.

| 항목 | 평가 기준 |
| --- | --- |
| 정확성 | 개념·코드·주장의 정확성, 버전과 적용 범위, 사실과 해석의 구분 |
| 설명 깊이 | 작동 원리, 원인과 증상의 구분, 대안과 한계 |
| 실용성 | 적용 조건, 예제, 검증 방법과 독자의 다음 행동 |
| 구성 | 명확한 도입과 흐름, 제목의 정직성, 중복 없는 설명 |
| 출처 | 주장을 뒷받침하는 일차 자료, 수치·인용의 추적 가능성 |

각 항목에서 0점은 핵심 요건 부재, 1점은 부분 충족, 2점은 해당 글의 목적에 충분한 충족을 뜻한다. 소수점은 충족 정도를 나타낸다. 개인 회고에는 허구의 실험이나 경력을 추가하지 않았으며, 당시 경험과 현재의 일반적 안내를 분리했다.

## 글별 전후 평가

| 글 | 원문 | 개선본 | 핵심 개선 |
| --- | ---: | ---: | --- |
| [캐시가 뭐에요?](../_posts/2022-10-15-cache.md) | 6.9 | 9.4 | 가정임을 표시한 지연 계산 예제와 캐시 후보 비교표 추가 / 네 전략을 읽기 책임·쓰기 시점으로 재구성하고 무효화 경쟁 순서 표 추가 |
| [CI/CD란?](../_posts/2022-10-22-ci-cd.md) | 7.0 | 9.3 | CI·Delivery·Deployment를 같은 기준의 표로 비교 / 프론트엔드 명령 예시와 npm ci·타입 검사·테스트 종료 조건 추가 |
| [구글 검색 너란 녀석...](../_posts/2022-10-29-google-search.md) | 7.0 | 9.4 | 발견·색인·검색 결과 제공을 분리해 재구성 / 초기 PageRank와 현재 공개 순위 시스템을 명확히 구분 |
| [브라우저 주소창에 google.com을 입력한다면?](../_posts/2022-11-12-browser.md) | 7.5 | 9.5 | URL 해석부터 렌더링까지 기본 경로와 생략 조건 재구성 / TCP/TLS·HTTP3 연결 비교, no-cache/no-store와 DNS/HTTP 캐시 구분 |
| [배치 작업 어디까지 해봤니?](../_posts/2022-11-26-batch.md) | 7.2 | 9.4 | 원래 50만 건·버전·시간·CPU 수치를 보존하고 실험 한계를 표기 / 전체 메모리 보관과 미완료 작업량의 원인을 나누어 설명 |
| [NestJS 예외 처리 (Error Exception)](../_posts/2023-01-07-nestjs-exception.md) | 6.3 | 9.3 | 공개 오류 응답 계약과 4xx 메시지·검증 배열·5xx 마스킹 정책 명시 / unknown 기반 catch-all 예제와 중복 응답 방지 처리 추가 |
| [NestJS 로깅 도입하기 (winston)](../_posts/2023-01-14-nestjs-logging.md) | 6.8 | 9.3 | 중앙 Winston 설정·DI 주입·Nest logger 연결로 코드 재구성 / finish/close 중복 방지와 aborted 상태·상태 코드·처리 시간·요청 ID 추가 |
| [LLM (Large Language Model) 및 사용 후기](../_posts/2023-04-08-llm%20사용%20후기.md) | 7.6 | 9.3 | 2023년 기록과 개정 설명을 분리하고 모델 계보를 표로 연결 / 7B×2바이트 메모리 계산으로 기록을 일반 사양으로 해석할 수 없는 이유 설명 |
| [DALL-E 및 사용 후기](../_posts/2023-04-15-DALL-E%20및%20사용%20후기.md) | 7.0 | 9.2 | DALL-E 1과 2의 중간 표현·생성 방식 비교 / CLIP·prior·diffusion의 역할 및 투명 마스크·outpainting·resize 차이를 설명 |
| [LoRA 학습법 (Google Colab)](../_posts/2023-04-16-LoRA%20학습법.md) | 7.5 | 9.2 | 데이터와 캡션 확인을 핵심 단계로 통합 / rank·alpha·학습량을 수식과 조건부 계산으로 구분 |
| [Kafka가 뭐야?](../_posts/2023-05-13-kafka가%20뭐야.md) | 7.8 | 9.5 | 주문 이벤트 예제로 Topic·Partition·Consumer Group을 연결 / 42번 처리/43 commit의 장애 시나리오와 외부 DB 원자성 설명 |
| [Kafka를 설치 및 연동해보자 (with NestJS)](../_posts/2023-05-20-kafka를%20설치%20및%20연동해보자%20(with%20NestJs).md) | 7.4 | 9.2 | 과거 Kafka 2.8 범위를 명시하고 Kafka 4.0 KRaft 전환 근거 제공 / DI 토큰·연결 수명·오류 전파·Controller를 포함하는 일관된 예제로 변경 |
| [ArgoCD err_too_many_redirects 해결하기](../_posts/2023-07-08-ArgoCD%20err_too_many_redirects.md) | 7.4 | 9.3 | curl 헤더와 ingress/backend 로그로 원인을 좁히는 순서 추가 / TLS 종료 위치별 설정 선택 표와 ConfigMap merge patch/rollout 예제 |
| [대용량 엑셀 다운로드 이슈 해결하기](../_posts/2023-08-05-대용량%20엑셀%20다운로드%20이슈.md) | 7.4 | 9.4 | 데이터 수신·워크북·압축·Blob의 메모리 사용 구간과 측정 부재를 명시 / end-to-end 스트리밍과 backpressure, async 작업 상태를 분리해 설명 |
| [국가 간 API 통신 이슈 해결하기](../_posts/2023-10-07-국가%20간%20API%20통신%20이슈.md) | 6.8 | 9.1 | 이미지와 API, 서버 처리와 연결 지연을 분리해 가설을 명확히 함 / curl 누적 시간의 해석과 지역·통신사별 통제 비교 절차 추가 |
| [Jenkins 취약점 이슈 해결하기 (CVE-2023-25765)](../_posts/2023-10-14-Jenkins%20취약점%20이슈.md) | 7.6 | 9.5 | 공격 권한 전제, 본체/플러그인 수정 범위, Jenkins와 NVD 평가 차이를 표로 명시 / 2023년 Java 11/17 기준과 2026년 LTS 2.555.1의 Java 21/25 기준 분리 |
| [Drone CI와 Bitbucket 연동하기](../_posts/2023-10-21-Drone%20CI%20for%20Bitbucket.md) | 7.2 | 9.4 | Server 2/Runner 1과 Compose v2 기준, Bitbucket Cloud 범위 명시 / HTTPS 프록시 전제, loopback 바인딩, Compose 내부 RPC 주소, required env를 갖춘 예시로 교체 |
| [Private Nexus Docker Repository 구축하기](../_posts/2023-11-16-Private%20Nexus%20Docker%20Repository.md) | 7.0 | 9.1 | 검토된 이미지 필수 환경변수, loopback 포트, named volume, 정상 종료 유예 적용 / hosted 필수/proxy 선택을 분리하고 Realm과 권한의 차이를 명시 |
| [무작위 로그인 시도 공격 대응하기](../_posts/2023-11-20-무작위%20로그인%20시도.md) | 7.4 | 9.3 | 키 인증·출발지 제한·Fail2ban·포트 변경의 목적과 한계를 비교 / 복구 경로→허용 추가→새 접속 확인→기존 공개 규칙 제거 순서로 재구성 |
| [Drone CI와 Portainer를 이용한 CI/CD 구축하기](../_posts/2023-11-24-Drone%20CI와%20Portainer를%20이용한%20CICD.md) | 7.1 | 9.3 | 단일 Docker host에는 socket 직접 연결로 단순화하고 loopback HTTPS 관리 포트만 공개 / GitOps updates와 BE Stack Webhook을 구분하고 2023 화면/2026 안내를 분리 |
| [Terraform으로 AWS 인프라 구축하기](../_posts/2023-11-26-Terraform으로%20AWS%20Infra%20구축하기.md) | 7.1 | 8.9 | 기존 인프라와 새 리소스 범위, 단일 EC2 한계, 인증서·서브넷 접근 경로를 명시 / SSO profile·계정 확인, 버전 범위와 lockfile 관리, terraform.tfvars 예시 추가 |
| [이미지에서 색상 추출하기](../_posts/2024-07-22-이미지에서%20색상%20추출하기.md) | 7.2 | 8.9 | 팔레트 후보 생성과 대표색 선택 기준을 분리하고 투명도·색 공간의 정책을 설명 / 8비트 RGBA 샘플링의 입력 검증과 투명 픽셀 제외 예제를 추가하고 실제 실행으로 확인 |
| [AI를 이용한 Git Commit 메시지 생성하기](../_posts/2024-08-30-AI를%20이용한%20Git%20Commit%20메시지%20생성하기.md) | 6.3 | 9.3 | GitHub README와 생성기 코드를 직접 확인해 당시 기능과 현재 구현 차이를 표로 정정 / Claude Sonnet 3.5 지원 종료일과 설치 버전·API 호환성의 범위를 명시 |
| [기능 분할 설계 (Feature-Sliced Design, FSD)](../_posts/2024-09-14-기능분할설계(FSD).md) | 7.0 | 9.4 | 레이어·슬라이스·세그먼트를 서로 다른 질문으로 설명하고 현재 processes 상태 명확화 / 같은 레이어 import 위반과 상위 조합 지점·슬라이스 합치기 대안을 구체화 |
| [스크롤은 건드리지마!!](../_posts/2024-12-10-스크롤은%20건드리지마!!.md) | 6.2 | 9.4 | 기본 관성·CSS 앵커 이동·입력 가로채기·스크롤 연동 장식을 표로 구분 / 반복 주장을 입력-결과 지연과 대체 구현의 검증 책임으로 통합 |
| [DLLM: 기존 LLM과의 차이점과 새로운 가능성](../_posts/2025-03-06-LLM%20기존%20LLM과의%20차이점과%20새로운%20가능성.md) | 6.4 | 9.4 | 설명 범위를 LLaDA 마스크 확산으로 고정하고 이산 토큰과 연속 노이즈 차이를 설명 / GPT 학습 병렬성·BERT 목표·LLaDA 생성 절차를 분리 |
| [브레드크럼(Breadcrumbs): 웹에서 필수 도구인가, 재평가 대상인가?](../_posts/2025-03-27-브레드크럼(Breadcrumbs).md) | 7.1 | 9.5 | 위치·방문 이력·필터의 역할을 나누고 검색 목록 복원을 별도 문제로 설명 / 깊이 숫자 대신 실제 상위 목적지와 과제로 도입 판단 |
| [Chrome은 이미지 요청 우선순위를 어떻게 결정할까요?](../_posts/2025-04-14-Chrome은%20이미지%20요청%20우선순위를%20어떻게%20결정할까요.md) | 7.6 | 9.4 | 발견 지연·우선순위·다운로드·렌더 지연을 분리하고 LCP 구간별 개입 표 추가 / 크기 휴리스틱을 악용하지 않고 올바른 width·height를 유지하도록 설명 |
| [JPEG가 여전히 널리 쓰이는 이유: 압축보다 큰 호환성](../_posts/2025-07-01-왜%20JPEG가%20여전히%20웹을%20지배하는가.md) | 7.3 | 9.1 | 제목을 널리 쓰이는 이유로 조정하고 압축과 교환 호환성의 구분을 중심 논지로 재구성 / 색차 서브샘플링·DCT·양자화·엔트로피의 역할과 품질 숫자의 비동등성 설명 |
| [AI는 인간을 덜 합리적이라고 가정할까? 게임 실험과 자의식 해석의 한계](../_posts/2025-11-24-AI는%20당신을%20비합리적이라고%20생각합니다.md) | 7.1 | 9.2 | 주장형 제목을 질문형으로 바꾸고 관측·저자의 정의·대안 설명·실험 밖 주장을 표로 구분 / 4200 호출과 28개 모델, 21개 선택 집단의 요약값을 구분 |
| [AI는 버블인가, 혁명인가? 기술·사업·가격을 나눠 보자](../_posts/2025-11-25-AI는%20버블인가,%20혁명인가.md) | 6.3 | 9.0 | 2025년 11월 자료 기준을 명시하고 세 가지 다른 판단과 증거를 표로 정리 / 검증 어려운 직접 인용을 없애고 Alphabet 공식 실적 자료에 근거한 CapEx와 운영비 부담으로 논지 보강 |
| [AI의 미래와 우리가 던져야 할 질문들](../_posts/2025-11-28-AI의%20미래와%20우리가%20던져야%20할%20질문들.md) | 6.2 | 9.0 | 직접 발언록 대신 대담을 출발점으로 한 해설임을 명시하고 검증된 공식 사례 중심으로 재구성 / 접근성·통제권·이탈 가능성 및 사실·추론·가치 권고를 구분하는 표 추가 |
| [Chain-of-Visual-Thought (CoVT) 기술 분석](../_posts/2025-12-01-Chain-of-Visual-Thought%20(CoVT)%20기술%20분석.md) | 7.2 | 9.2 | 기존 VLM의 시각 입력과 텍스트 중심 중간 추론을 구분 / 시각 토큰 정의 및 SAM8·Depth4·Edge4·DINO4 표 추가 |
| [애플의 LLM 하이퍼파라미터 전이 연구: Complete(d) Parameterisation](../_posts/2026-01-03-apple-computed%20Parameterisation.md) | 7.6 | 9.3 | Figure1 원본 숫자 2.31/1.32와 50M→7.2B 비교의 손실·토큰 기준 재확인 / 배치 증가 시 η·λ·ε·1-β·업데이트 횟수 전체 표 및 β1=.9→.6 검산 예시 추가 |
| [Claude Code 제작자 Boris Cherny의 13가지 사용 팁](../_posts/2026-01-04-claude-code-tips.md) | 7.0 | 9.0 | 문제→첫 개입→평가 기준 표와 완료까지의 비용 중심 논지 추가 / 13개 주제와 기존 6개 스크린샷을 보존하면서 독립 작업 경계·지침 삭제 기준·작은 변경의 예외 제시 |
| [코딩 에이전트가 코드를 빨리 써도, 제품은 저절로 좋아지지 않는다](../_posts/2026-05-07-코딩%20에이전트가%20코드를%20빨리%20써도,%20제품은%20저절로%20좋아지지%20않는다.md) | 7.6 | 9.4 | 원문 요약을 줄이고 제품 가치에 집중해 280줄에서 118줄로 편집 / 가상 10일 작업의 구현·리뷰·배포 대기를 분리하고 전체 개선 10% 계산 |
| [AI 시대의 좋은 개발자는 코드를 더 많이 만들지 않는다](../_posts/2026-05-12-AI%20시대의%20좋은%20개발자는%20코드를%20더%20많이%20만들지%20않는다.md) | 8.4 | 9.3 | 노동시장·도입 통계 등 유지비와 직접 연결되지 않는 단락 제거 / 사전 공개 논문과 관찰 연구의 한계를 유지하고 최신 METR 설계 문제 확인 |
| [AI 에이전트를 많이 돌리면 정말 생산성이 올라갈까](../_posts/2026-05-29-AI%20에이전트를%20많이%20돌리면%20정말%20생산성이%20올라갈까.md) | 8.1 | 9.2 | 파일·공통 API 계약·가설 조사·독립 리뷰별 병렬화 기준 표 추가 / 별도 worktree가 의미상 충돌을 해결하지 않는다는 한계 명시 |
| [macOS에서 만든 한글 파일명이 검색되지 않는 이유](../_posts/2026-07-03-macOS에서%20만든%20한글%20파일명이%20검색되지%20않는%20이유.md) | 8.3 | 9.5 | APFS 보존과 정규화 무시 비교를 Apple 문서의 버전 조건과 연결 / NFC/NFD 코드 포인트를 출력하는 JavaScript 최소 예제 추가 및 실행 검증 |
| [에이전트 코드베이스에서 리팩터링이 돈이 되는 이유](../_posts/2026-08-03-에이전트%20코드베이스에서%20리팩터링이%20돈이%20되는%20이유.md) | 8.2 | 9.5 | 원문 줄 수·추정 입력/출력·소요 시간을 전후 표로 압축 / 83%는 추정 입력량 감소이며 청구 비용이나 실행 시간 개선이 아님을 선명하게 구분 |
| [AI로 만들기 쉬워진 시대, 차별화를 만드는 안목](../_posts/2026-08-06-AI가%20모든%20것을%20만들%20수%20있는%20시대,%20진짜%20차별화는%20취향이다.md) | 6.9 | 9.2 | 안목을 사전 판단 기준과 사후 수정 조건으로 정의 / 기술·유통·운영과 안목을 함께 보고 해자 주장에 경계 설정 |
| [웹에서 HEVC with Alpha 영상을 사용할 때 고려해야 할 것들](../_posts/2026-09-04-웹에서%20HEVC%20with%20Alpha%20영상을%20사용할%20때%20고려해야%20할%20것들.md) | 8.8 | 9.5 | Apple·S3·CloudFront·WHATWG 기술 주장에 본문 근거 연결 / Range와 적응형 비트레이트 차이 및 헤더 크기의 8MiB 단위 명시 |

## 검증 범위

- 프로덕션 Jekyll 전체 빌드 성공. 중복 출력 경고 해소.
- HTML-Proofer 내부 링크·이미지·스크립트·앵커 검사 통과. 외부 링크 자동 일괄 검사는 제외했으며, 핵심 인용은 본문 검토에서 자료를 열어 확인했다.
- 42편 모두 본문 변경, 발행일·파일명·기존 42개 URL 보존, 수정일 표시와 렌더링 결과 확인.
- Kafka/NestJS 예제 6개 파일: KafkaJS 2.2.4, NestJS 11.1.6, TypeScript 5.9.3에서 strict 타입 검사 통과. 브로커 통합 테스트는 미실시.
- 배치 경계값·실패 시 커서 종료, RGBA 예제, NFC/NFD 예제 실행 검증. 셸·YAML·코드 펜스 및 git diff 검사 통과.
- CoVT·Apple 연구 글과 Drone/Portainer·Terraform 절차를 작성 담당 외 검토자가 추가 검토. ALB 가용 영역 전제 보완.
- 부수 변경: 작성일/수정일 분리 표시, 같은 경로를 덮어쓰던 태그 대소문자 통일, 매니페스트 중복 출력과 아이콘 경로 수정.
- 배포는 저장소의 기존 GitHub Actions → GitHub Pages 경로를 사용한다. 이 기록의 점수는 배포 여부와 독립적이며, 실제 배포 상태는 해당 커밋의 Actions 결과에서 확인할 수 있다.

문서에 담긴 외부 인프라·유료 API·실제 기기 실험은 이 검토에서 모두 재현한 것이 아니다. 역사적 서비스 상태와 저자의 실제 측정값은 원문에 존재하는 기록 범위에서 보존했다. 아래 글별 한계에 추가 확인이 필요한 부분을 기록했다.

## 글별 근거와 남은 한계

### 캐시가 뭐에요?

- 파일: `_posts/2022-10-15-cache.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.7, 1.3, 1.2, 1.5, 1.2] → [1.9, 1.9, 1.9, 1.9, 1.8]
- 원문 검토: 캐시 전략 소개에 비해 읽기·쓰기 축의 구분과 선택 기준이 부족함
- 원문 검토: TTL·DB 갱신 후 무효화에도 남는 경쟁 조건의 구체적 사례가 없음
- 원문 검토: 적중률 외 운영 지표와 메모리 축출 정책을 설명하지 않음
- 개선: 가정임을 표시한 지연 계산 예제와 캐시 후보 비교표 추가
- 개선: 네 전략을 읽기 책임·쓰기 시점으로 재구성하고 무효화 경쟁 순서 표 추가
- 개선: TTL과 eviction, 요청 합치기의 범위, 장애 시 원본 부하를 구분
- 남은 한계: 실제 서비스 적중률·지연 측정 데이터 없음
- 남은 한계: 분산 무효화나 요청 합치기의 실행 구현은 범위 밖
- 확인한 자료: [자료 1](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside), [자료 2](https://redis.io/docs/latest/develop/reference/eviction/)

### CI/CD란?

- 파일: `_posts/2022-10-22-ci-cd.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.8, 1.2, 1.1, 1.5, 1.4] → [1.9, 1.8, 1.9, 1.9, 1.8]
- 원문 검토: 정의와 장점에 집중해 실제 팀이 적용할 검증·복구 기준이 부족함
- 원문 검토: PR 성공과 실제 통합 브랜치의 성공 차이를 설명하지 않음
- 원문 검토: 빌드 이후 배포 산출물·환경·사용자 경로의 검증이 빠짐
- 개선: CI·Delivery·Deployment를 같은 기준의 표로 비교
- 개선: 프론트엔드 명령 예시와 npm ci·타입 검사·테스트 종료 조건 추가
- 개선: 구축형 제품의 배포 일정, 산출물 추적·배포 후 확인·복구 기준 제시
- 남은 한계: CI 공급자별 실행 가능한 workflow 파일은 포함하지 않음
- 남은 한계: 특정 팀의 전달·복구 시간 개선을 측정한 사례는 없음
- 확인한 자료: [자료 1](https://martinfowler.com/articles/continuousIntegration.html), [자료 2](https://martinfowler.com/bliki/ContinuousDelivery.html), [자료 3](https://docs.npmjs.com/cli/v11/commands/npm-ci/)

### 구글 검색 너란 녀석...

- 파일: `_posts/2022-10-29-google-search.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.7, 1.2, 1.2, 1.4, 1.5] → [1.9, 1.8, 1.9, 1.9, 1.9]
- 원문 검토: 크롤링과 PageRank 사이에 독립적인 색인 생성 설명이 부족함
- 원문 검토: SEO 항목이 일반론에 머물러 검색 미노출 원인을 구분하기 어려움
- 원문 검토: robots.txt·noindex·canonical의 관계와 한계가 빠짐
- 개선: 발견·색인·검색 결과 제공을 분리해 재구성
- 개선: 초기 PageRank와 현재 공개 순위 시스템을 명확히 구분
- 개선: 개발 블로그 개선표와 Search Console 점검 순서, 인과 해석의 한계 추가
- 남은 한계: 검색 순위의 비공개 가중치는 평가하지 않음
- 남은 한계: 블로그 Search Console의 실제 데이터에 접근하거나 성과를 측정하지 않음
- 확인한 자료: [자료 1](https://developers.google.com/search/docs/fundamentals/how-search-works), [자료 2](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), [자료 3](https://developers.google.com/search/docs/appearance/ranking-systems-guide), [자료 4](https://research.google/pubs/the-anatomy-of-a-large-scale-hypertextual-web-search-engine/), [자료 5](https://developers.google.com/search/docs/appearance/page-experience), [자료 6](https://developers.google.com/search/docs/crawling-indexing/robots/intro)

### 브라우저 주소창에 google.com을 입력한다면?

- 파일: `_posts/2022-11-12-browser.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.8, 1.4, 1.2, 1.6, 1.5] → [1.9, 1.9, 1.9, 1.9, 1.9]
- 원문 검토: 주소 해석과 HTTPS 이동 가정이 생략됨
- 원문 검토: 캐시·연결 재사용 예외가 개별 설명에 흩어져 실제 경로를 이해하기 어려움
- 원문 검토: 브라우저 단계와 성능 문제 관찰 항목의 연결이 없음
- 개선: URL 해석부터 렌더링까지 기본 경로와 생략 조건 재구성
- 개선: TCP/TLS·HTTP3 연결 비교, no-cache/no-store와 DNS/HTTP 캐시 구분
- 개선: DevTools Timing 관찰표와 TTFB 해석·Disable cache의 한계 추가
- 남은 한계: Google 서비스 내부 구현이나 특정 브라우저의 모든 최적화를 재현한 설명은 아님
- 남은 한계: 실제 네트워크 캡처·지연 측정은 수행하지 않음
- 확인한 자료: [자료 1](https://www.rfc-editor.org/rfc/rfc1034), [자료 2](https://www.rfc-editor.org/rfc/rfc9114.html), [자료 3](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching), [자료 4](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work), [자료 5](https://developer.chrome.com/docs/devtools/network/reference)

### 배치 작업 어디까지 해봤니?

- 파일: `_posts/2022-11-26-batch.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.5, 1.6, 1.3, 1.4, 1.4] → [1.9, 1.9, 1.8, 1.9, 1.9]
- 원문 검토: 과거 CPU 관찰값만으로 안정성을 단정하는 표현이 남음
- 원문 검토: 최종 선택 기준이 빠른 분할 처리와 느린 스트림이라는 단순 대비에 머무름
- 원문 검토: 잔여 배치 수정은 있으나 전체 읽기·쓰기·재시도 계약이 부족함
- 원문 검토: 인덱스·측정 조건·부분 실패·동시 데이터 변경의 한계가 충분히 드러나지 않음
- 개선: 원래 50만 건·버전·시간·CPU 수치를 보존하고 실험 한계를 표기
- 개선: 전체 메모리 보관과 미완료 작업량의 원인을 나누어 설명
- 개선: 커서와 bounded bulkWrite를 조합한 텍스트 예제, 잔여 flush·finally close 추가
- 개선: 경계 건수 0/1/1000/1001와 중간 실패를 모델 스텁으로 실행 검증
- 개선: 매칭 수·수정 수·멱등성·체크포인트·대상 시점의 차이를 설명
- 남은 한계: 2022년 원시 측정 환경과 반복 실험은 재현하지 않음
- 남은 한계: 코드 검증은 모델 스텁의 제어 흐름이며 실제 MongoDB 통합·성능 검증은 아님
- 남은 한계: 재개 가능한 작업 저장소 전체 구현은 포함하지 않음
- 확인한 자료: [자료 1](https://nodejs.org/download/release/v14.19.0/docs/api/cli.html#cli_max_old_space_size_size_in_megabytes), [자료 2](https://www.mongodb.com/docs/manual/reference/method/db.collection.bulkWrite/), [자료 3](https://www.mongodb.com/docs/manual/reference/limits/), [자료 4](https://www.mongodb.com/docs/manual/reference/method/cursor.skip/), [자료 5](https://mongoosejs.com/docs/6.x/docs/api/querycursor.html), [자료 6](https://mongoosejs.com/docs/6.x/docs/api.html#model_Model-bulkWrite)

### NestJS 예외 처리 (Error Exception)

- 파일: `_posts/2023-01-07-nestjs-exception.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.7, 1.1, 1.3, 1.4, 0.8] → [1.9, 1.9, 1.7, 1.9, 1.9]
- 원문 검토: HttpException 전용 예제여서 알 수 없는 오류와 응답 계약이 달라짐
- 원문 검토: 5xx 상세 메시지 공개 정책과 로그 책임이 빠짐
- 원문 검토: 전역 등록·필터 우선순위·이미 시작된 응답의 경계가 부족함
- 개선: 공개 오류 응답 계약과 4xx 메시지·검증 배열·5xx 마스킹 정책 명시
- 개선: unknown 기반 catch-all 예제와 중복 응답 방지 처리 추가
- 개선: APP_FILTER 등록과 route/controller/global 처리 우선순위 설명
- 개선: HTTP 요청 밖의 비동기 작업·스트리밍 경계를 명시하고 기대 동작 표 추가
- 남은 한계: NestJS/Express 의존성이 없어 애플리케이션 컴파일·통합 실행은 수행하지 않음
- 남은 한계: 예제는 Express JSON API이며 GraphQL·Fastify·큐 작업용 구현은 아님
- 남은 한계: 프로젝트별 업무 오류 코드·민감 로그 마스킹 정책은 설계 대상
- 확인한 자료: [자료 1](https://docs.nestjs.com/exception-filters), [자료 2](https://github.com/nestjs/nest/blob/master/packages/common/exceptions/http.exception.ts), [자료 3](https://docs.nestjs.com/faq/request-lifecycle)

### NestJS 로깅 도입하기 (winston)

- 파일: `_posts/2023-01-14-nestjs-logging.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.6, 1.2, 1.4, 1.4, 1.2] → [1.9, 1.9, 1.7, 1.9, 1.9]
- 원문 검토: 요청 시작 URL만 기록해 완료 상태·응답 시간·중단을 구분할 수 없음
- 원문 검토: 직접 만든 로거와 Nest 시스템 로거의 연결·주입 책임이 불명확함
- 원문 검토: 날짜 회전 한계를 지적하지만 메모리·파일 보관 구성의 실제 대안이 부족함
- 개선: 중앙 Winston 설정·DI 주입·Nest logger 연결로 코드 재구성
- 개선: finish/close 중복 방지와 aborted 상태·상태 코드·처리 시간·요청 ID 추가
- 개선: route pattern과 필드 허용 목록으로 민감 값 무분별 기록 방지
- 개선: moment 제거, 크기·파일 개수 회전 설정과 날짜 회전 차이 설명
- 개선: 예상 JSON 예시는 실제 측정값이 아님을 명시
- 남은 한계: NestJS/Express/Winston 의존성이 없어 컴파일·파일 회전 통합 검증은 수행하지 않음
- 남은 한계: 컨트롤러에 등록된 경로만 미들웨어 대상이며 전체 미등록 URL까지 기록하는 구성은 아님
- 남은 한계: 요청 ID의 전 계층·분산 추적 전파는 별도 구현 필요
- 확인한 자료: [자료 1](https://docs.nestjs.com/middleware), [자료 2](https://nodejs.org/api/http.html#event-finish), [자료 3](https://github.com/winstonjs/winston), [자료 4](https://github.com/gremo/nest-winston), [자료 5](https://docs.nestjs.com/techniques/logger), [자료 6](https://github.com/winstonjs/winston-daily-rotate-file)

### LLM (Large Language Model) 및 사용 후기

- 파일: `_posts/2023-04-08-llm 사용 후기.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.8, 1.3, 1.3, 1.6, 1.6] → [1.9, 1.8, 1.8, 1.9, 1.9]
- 원문 검토: 개인 후기에서 제품 적합성 결론으로 넘어가는 평가 기준이 부족
- 원문 검토: GPU 메모리 기록의 불확실성은 밝혔지만 실제 파라미터 저장량과의 관계 설명 부족
- 원문 검토: 모델 계보·벤치마크·사용 경험의 비교 단위가 혼재
- 개선: 2023년 기록과 개정 설명을 분리하고 모델 계보를 표로 연결
- 개선: 7B×2바이트 메모리 계산으로 기록을 일반 사양으로 해석할 수 없는 이유 설명
- 개선: 업무 정확도·지연·반복 안정성·운영 부담을 동일 과제에서 평가하는 기준 추가
- 남은 한계: 당시 프롬프트·양자화·실행 도구 옵션이 없어 정량 재현 불가
- 남은 한계: 새로운 모델 실험을 수행하지 않았고 최신 모델 비교를 다루지 않음
- 확인한 자료: [자료 1](https://arxiv.org/abs/1706.03762), [자료 2](https://arxiv.org/abs/2302.13971), [자료 3](https://crfm.stanford.edu/2023/03/13/alpaca.html), [자료 4](https://lmsys.org/blog/2023-03-30-vicuna/), [자료 5](https://openai.com/index/chatgpt/), [자료 6](https://openai.com/index/introducing-chatgpt-and-whisper-apis/)

### DALL-E 및 사용 후기

- 파일: `_posts/2023-04-15-DALL-E 및 사용 후기.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.6, 1.3, 1.2, 1.5, 1.4] → [1.9, 1.8, 1.8, 1.8, 1.9]
- 원문 검토: API 기능 수가 적어 제품 도입이 시기상조라는 결론이 과도함
- 원문 검토: CLIP을 이해 모델로 설명해 생성 모델과 역할 구분이 약함
- 원문 검토: 편집과 resize의 목적·제품 검증 기준 부족
- 개선: DALL-E 1과 2의 중간 표현·생성 방식 비교
- 개선: CLIP·prior·diffusion의 역할 및 투명 마스크·outpainting·resize 차이를 설명
- 개선: 제품의 실패 비용과 검수 흐름을 기준으로 당시 결론 범위를 조정
- 남은 한계: 2023년 결과의 통제 실험·성공률 기록 없음
- 남은 한계: 현재 API 실행 가이드가 아닌 역사적 사용 후기
- 확인한 자료: [자료 1](https://arxiv.org/abs/2102.12092), [자료 2](https://arxiv.org/abs/2103.00020), [자료 3](https://arxiv.org/abs/2204.06125), [자료 4](https://developers.openai.com/api/reference/resources/images), [자료 5](https://openai.com/index/dall-e-2/)

### LoRA 학습법 (Google Colab)

- 파일: `_posts/2023-04-16-LoRA 학습법.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.7, 1.2, 1.5, 1.6, 1.5] → [1.9, 1.9, 1.8, 1.8, 1.8]
- 원문 검토: 일반적인 반복 실험 권고만 있어 결과의 원인 분리 방법 부족
- 원문 검토: rank·alpha·steps의 상호작용을 독자가 판단하기 어려움
- 원문 검토: 자동 캡션 품질·모델 계열 호환성·평가 조건이 부족
- 개선: 데이터와 캡션 확인을 핵심 단계로 통합
- 개선: rank·alpha·학습량을 수식과 조건부 계산으로 구분
- 개선: epoch·seed·LoRA 강도를 통제한 결과 비교 및 증상별 가설 표 추가
- 남은 한계: 연결 노트북을 실제 Colab에서 재실행하지 않음
- 남은 한계: 당시 기본 모델·GPU·전체 설정이 없어 30분 기록 재현 불가
- 확인한 자료: [자료 1](https://arxiv.org/abs/2106.09685), [자료 2](https://colab.research.google.com/github/hollowstrawberry/kohya-colab/blob/main/Dataset_Maker.ipynb), [자료 3](https://github.com/hollowstrawberry/kohya-colab), [자료 4](https://huggingface.co/docs/diffusers/en/training/lora), [자료 5](https://huggingface.co/docs/diffusers/v0.14.0/en/training/lora), [자료 6](https://j-ho.s3.ap-northeast-2.amazonaws.com/ionic6_images.zip)

### Kafka가 뭐야?

- 파일: `_posts/2023-05-13-kafka가 뭐야.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.9, 1.4, 1.3, 1.6, 1.6] → [1.9, 1.9, 1.9, 1.9, 1.9]
- 원문 검토: 구성요소가 나열돼 있어 순서·병렬성·업무 실패를 연결하기 어려움
- 원문 검토: 중복 발생 지점과 멱등 처리의 원자성 조건이 부족
- 원문 검토: 보관 만료·compaction·acks의 경계와 Kafka 4.0 변화가 없음
- 개선: 주문 이벤트 예제로 Topic·Partition·Consumer Group을 연결
- 개선: 42번 처리/43 commit의 장애 시나리오와 외부 DB 원자성 설명
- 개선: 확장 한계·retention·ISR·exactly-once의 적용 범위를 구분하고 공식 자료 연결
- 남은 한계: 일반적인 Consumer Group의 입문 범위로 최신 share group 등 고급 프로토콜은 다루지 않음
- 남은 한계: 운영 부하·장애 실험 결과를 포함하지 않음
- 확인한 자료: [자료 1](https://kafka.apache.org/34/configuration/producer-configs/#acks), [자료 2](https://kafka.apache.org/34/configuration/topic-level-configs/), [자료 3](https://kafka.apache.org/34/design/design/#load-balancing), [자료 4](https://kafka.apache.org/34/design/design/#message-delivery-semantics), [자료 5](https://kafka.apache.org/34/getting-started/introduction/), [자료 6](https://kafka.apache.org/34/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html), [자료 7](https://kafka.apache.org/40/getting-started/upgrade/), [자료 8](https://kafka.js.org/docs/consuming#manual-committing)

### Kafka를 설치 및 연동해보자 (with NestJS)

- 파일: `_posts/2023-05-20-kafka를 설치 및 연동해보자 (with NestJs).md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.7, 1.3, 1.4, 1.5, 1.5] → [1.9, 1.8, 1.9, 1.8, 1.8]
- 원문 검토: 전체 실행 경로에서 Controller·main 구성과 실제 검증 단계가 빠져 있음
- 원문 검토: 설정 주입·자동 Topic 생성·부분 연결 실패 설명 부족
- 원문 검토: 과거 브로커 설치와 신규 Kafka 차이 및 offset 재시작 검증이 약함
- 개선: 과거 Kafka 2.8 범위를 명시하고 Kafka 4.0 KRaft 전환 근거 제공
- 개선: DI 토큰·연결 수명·오류 전파·Controller를 포함하는 일관된 예제로 변경
- 개선: CLI 통신→HTTP 발행→Consumer 로그→그룹 offset→재시작 확인을 연결
- 개선: 게시 본문의 TypeScript 코드 6개를 별도 프로젝트로 추출해 KafkaJS 2.2.4·NestJS 11.1.6·TypeScript 5.9.3에서 strict, skipLibCheck=false, noEmit 타입 검사 통과
- 남은 한계: Kafka 2.8/NestJS 실제 통합 환경을 띄워 실행하지 않음
- 남은 한계: 단일 Topic/handler와 단일 Broker 학습 예제로 운영 내구성·재시도 체계는 포함하지 않음
- 확인한 자료: [자료 1](https://docs.nestjs.com/controllers#status-code), [자료 2](https://docs.nestjs.com/fundamentals/custom-providers), [자료 3](https://docs.nestjs.com/fundamentals/lifecycle-events), [자료 4](https://kafka.apache.org/28/configuration/broker-configs/), [자료 5](https://kafka.apache.org/28/getting-started/quickstart/), [자료 6](https://kafka.apache.org/40/getting-started/upgrade/), [자료 7](https://kafka.js.org/docs/consuming), [자료 8](https://kafka.js.org/docs/producing)

### ArgoCD err_too_many_redirects 해결하기

- 파일: `_posts/2023-07-08-ArgoCD err_too_many_redirects.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.9, 1.1, 1.3, 1.5, 1.6] → [1.9, 1.8, 1.9, 1.9, 1.8]
- 원문 검토: 정확한 당시 원인은 있으나 다른 redirect 원인과 구별하는 진단이 부족
- 원문 검토: 단편 YAML 이후 반영·검증·되돌리기 절차 없음
- 원문 검토: TLS termination·re-encryption·passthrough의 선택 경계 설명 부족
- 개선: curl 헤더와 ingress/backend 로그로 원인을 좁히는 순서 추가
- 개선: TLS 종료 위치별 설정 선택 표와 ConfigMap merge patch/rollout 예제
- 개선: GitOps 원본 반영·내부 HTTP 의미·UI/CLI 검증·502 후속 진단 설명
- 남은 한계: 실제 사용자 클러스터에서 장애 재현하지 않음
- 남은 한계: Controller별 완전한 배포 YAML 대신 공식 문서와 선택 기준 제공
- 확인한 자료: [자료 1](https://argo-cd.readthedocs.io/en/release-2.7/operator-manual/ingress/), [자료 2](https://argo-cd.readthedocs.io/en/stable/operator-manual/argocd-cmd-params-cm-yaml/), [자료 3](https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/)

### 대용량 엑셀 다운로드 이슈 해결하기

- 파일: `_posts/2023-08-05-대용량 엑셀 다운로드 이슈.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.8, 1.3, 1.4, 1.5, 1.4] → [1.9, 1.9, 1.9, 1.9, 1.8]
- 원문 검토: OOM 해소와 대기 UX 개선의 원인이 충분히 분리되지 않음
- 원문 검토: 사용자 10명 미만이라는 규모 설명만으로 운영 조건을 제한
- 원문 검토: 비동기 접수 이후 실패·재시작·중복·정합성·다운로드 경로 설명 부족
- 개선: 데이터 수신·워크북·압축·Blob의 메모리 사용 구간과 측정 부재를 명시
- 개선: end-to-end 스트리밍과 backpressure, async 작업 상태를 분리해 설명
- 개선: 실제 HTTP 200 기록을 보존하고 202 예시·작업 소유권·정합성·검증 항목 추가
- 남은 한계: 당시 메모리 프로파일과 처리 시간 수치가 없어 개선율 제시 불가
- 남은 한계: 특정 DB나 XLSX 라이브러리 구현을 실제 재현한 글은 아님
- 확인한 자료: [자료 1](https://d2.naver.com/helloworld/9423440), [자료 2](https://github.com/exceljs/exceljs#streaming-xlsx), [자료 3](https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/structure-of-a-spreadsheetml-document), [자료 4](https://nodejs.org/api/stream.html), [자료 5](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.3)

### 국가 간 API 통신 이슈 해결하기

- 파일: `_posts/2023-10-07-국가 간 API 통신 이슈.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.7, 1.1, 1.2, 1.6, 1.2] → [1.9, 1.7, 1.8, 1.9, 1.8]
- 원문 검토: 거리 비교의 한계는 설명했지만 실제 지연 구간을 검증하는 절차가 없었음
- 원문 검토: 지역 진입점 선택과 CCN의 사설 upstream 조건이 생략됨
- 원문 검토: 전후 경로 도식에서 낮은 지연을 확정적으로 표현하면서 수치 근거는 없음
- 개선: 이미지와 API, 서버 처리와 연결 지연을 분리해 가설을 명확히 함
- 개선: curl 누적 시간의 해석과 지역·통신사별 통제 비교 절차 추가
- 개선: VPC 라우트·사설 upstream·프록시 실패 전환·쓰기 요청 재시도 조건 추가
- 개선: 새 측정 절차는 보완안임을 밝히고 당시 수치를 생성하지 않음
- 남은 한계: 당시 지역·통신사별 전후 latency·오류율 원자료가 없어 개선률과 원인을 정량 확정할 수 없음
- 남은 한계: 현장의 CCN·DNS 설정 자체는 재실행하지 않음
- 확인한 자료: [자료 1](https://www.tencentcloud.com/product/ccn), [자료 2](https://www.tencentcloud.com/document/product/215/47911), [자료 3](https://curl.se/docs/manpage.html#-w), [자료 4](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Connection_management_in_HTTP_1.x), [자료 5](https://www.rfc-editor.org/rfc/rfc9113.html)

### Jenkins 취약점 이슈 해결하기 (CVE-2023-25765)

- 파일: `_posts/2023-10-14-Jenkins 취약점 이슈.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.8, 1.1, 1.3, 1.6, 1.8] → [2, 1.8, 1.8, 1.9, 2]
- 원문 검토: 2023년 Java 11 설치·yum 업데이트 예시가 현재 실행 경로로 오독될 수 있음
- 원문 검토: 2.93.1 이상만 강조해 해당 CVE의 최초 수정과 현재 설치 권장 버전 구분이 약함
- 원문 검토: 알람 패키지와 실제 로딩된 플러그인 대조 및 회귀 검증이 추상적
- 개선: 공격 권한 전제, 본체/플러그인 수정 범위, Jenkins와 NVD 평가 차이를 표로 명시
- 개선: 2023년 Java 11/17 기준과 2026년 LTS 2.555.1의 Java 21/25 기준 분리
- 개선: 오래된 설치 명령을 제거하고 실행 Java 확인·백업·템플릿 회귀·CWPP 재검사 절차 추가
- 개선: 취약점 탐지와 실제 침해 여부의 증거를 구분하고 sandbox 우회식 복구를 방지
- 남은 한계: 실제 CWPP 재검사 결과와 Jenkins 실행 환경에는 접근하지 않았음
- 남은 한계: 기존 기록 이상의 침해 여부나 패치 효과를 주장하지 않음
- 확인한 자료: [자료 1](https://www.jenkins.io/security/advisory/2023-02-15/#SECURITY-2939), [자료 2](https://nvd.nist.gov/vuln/detail/CVE-2023-25765), [자료 3](https://plugins.jenkins.io/email-ext/), [자료 4](https://www.jenkins.io/doc/book/platform-information/support-policy-java/), [자료 5](https://www.jenkins.io/doc/upgrade-guide/2.361/)

### Drone CI와 Bitbucket 연동하기

- 파일: `_posts/2023-10-21-Drone CI for Bitbucket.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.6, 1.1, 1.3, 1.6, 1.6] → [1.9, 1.8, 1.9, 1.9, 1.9]
- 원문 검토: latest와 외부 HTTP/HTTPS 포트 구성이 운영 전제를 충분히 고정하지 못함
- 원문 검토: 외부 OAuth 주소와 Runner RPC 주소가 뒤섞여 있음
- 원문 검토: Runner 관리 포트 노출과 사용자 등록 범위 및 socket 권한 설명이 부족
- 원문 검토: 실패 지점별 진단과 push/PR 배포 조건 검증이 없음
- 개선: Server 2/Runner 1과 Compose v2 기준, Bitbucket Cloud 범위 명시
- 개선: HTTPS 프록시 전제, loopback 바인딩, Compose 내부 RPC 주소, required env를 갖춘 예시로 교체
- 개선: 등록 허용 목록, secret Git 제외·무출력 config 검사, Docker socket 권한 설명 추가
- 개선: OAuth/webhook/Pending/clone 실패 진단표 및 branch와 event 동시 제한 안내 추가
- 남은 한계: 실제 Bitbucket OAuth 및 webhook, Runner를 배포해 검증하지 않았음
- 남은 한계: 예시는 공식 계열 태그이며 운영에는 검토한 정확한 태그 또는 digest를 선택해야 함
- 남은 한계: 리버스 프록시는 전제로 명시했으며 설치 설정 전체는 포함하지 않음
- 확인한 자료: [자료 1](https://docs.drone.io/server/provider/bitbucket-cloud/), [자료 2](https://docs.drone.io/runner/docker/installation/linux/), [자료 3](https://docs.drone.io/server/reference/drone-user-filter/), [자료 4](https://docs.drone.io/pipeline/docker/syntax/trigger/), [자료 5](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/), [자료 6](https://docs.docker.com/engine/security/), [자료 7](https://www.alpinelinux.org/releases/)

### Private Nexus Docker Repository 구축하기

- 파일: `_posts/2023-11-16-Private Nexus Docker Repository.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.6, 1.1, 1.3, 1.6, 1.4] → [1.9, 1.8, 1.8, 1.8, 1.8]
- 원문 검토: 이미지 버전 미지정과 HTTP 노출을 그대로 따라 하기 쉬움
- 원문 검토: named volume·종료 시간·초기 비밀번호 명령이 부족
- 원문 검토: 관리자와 CI/pull 계정 권한 분리가 추상적
- 원문 검토: 로컬 레이어와 Registry 검증 차이, digest 검증, 실패 진단이 없음
- 개선: 검토된 이미지 필수 환경변수, loopback 포트, named volume, 정상 종료 유예 적용
- 개선: hosted 필수/proxy 선택을 분리하고 Realm과 권한의 차이를 명시
- 개선: Linux loopback HTTP 실습과 운영 TLS 경로·daemon config 검증을 구분
- 개선: tag 제거 후 pull과 digest 비교, pull 전용 계정 검증, 백업·cleanup 보존 조건 추가
- 남은 한계: Nexus와 Registry를 실제 기동해 push/pull하지 않았음
- 남은 한계: 사용할 Nexus 버전·권한 상세·TLS 프록시는 현장에 맞춰 지정해야 함
- 남은 한계: 기존 스크린샷은 2023년 UI이며 현행 화면과 다를 수 있음
- 확인한 자료: [자료 1](https://github.com/sonatype/docker-nexus3), [자료 2](https://help.sonatype.com/en/docker-authentication.html), [자료 3](https://help.sonatype.com/en/docker-repository-reverse-proxy-strategies.html), [자료 4](https://docs.docker.com/reference/cli/dockerd/#insecure-registries), [자료 5](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file)

### 무작위 로그인 시도 공격 대응하기

- 파일: `_posts/2023-11-20-무작위 로그인 시도.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.7, 1.3, 1.2, 1.6, 1.6] → [1.9, 1.8, 1.8, 1.9, 1.9]
- 원문 검토: 맥락 없이 iptables append 규칙을 복사하면 무효 또는 운영자 잠금 위험이 있음
- 원문 검토: 실패 로그 집계에 고정 필드 awk와 Failed password만 사용
- 원문 검토: sshd Include/Match 및 기존 세션과 새 연결의 차이 설명 부족
- 원문 검토: Fail2ban 설치·로그 backend·실행 검증이 완결되지 않음
- 개선: 키 인증·출발지 제한·Fail2ban·포트 변경의 목적과 한계를 비교
- 개선: 복구 경로→허용 추가→새 접속 확인→기존 공개 규칙 제거 순서로 재구성
- 개선: NAT 출발지·복수 보안 그룹·IPv6·TCP Wrappers 차이 반영
- 개선: sshd -t/-T와 조건부 설정·MFA 주의점, journal 기반 Fail2ban 정책과 검증 추가
- 개선: 인증 실패·성공 로그인·침해 여부를 구분하고 미확인 공격 주체를 단정하지 않음
- 남은 한계: 서버의 실제 sshd·방화벽·Fail2ban 설정이나 침해 로그를 검사한 것은 아님
- 남은 한계: 클라우드/배포판마다 서비스명·로그·방화벽 도구가 다르므로 본문에서 범위를 구분함
- 확인한 자료: [자료 1](https://man.openbsd.org/sshd_config), [자료 2](https://man.openbsd.org/sshd), [자료 3](https://www.openssh.org/txt/release-6.7), [자료 4](https://manpages.debian.org/testing/fail2ban/jail.conf.5.en.html)

### Drone CI와 Portainer를 이용한 CI/CD 구축하기

- 파일: `_posts/2023-11-24-Drone CI와 Portainer를 이용한 CICD.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.6, 1.2, 1.3, 1.5, 1.5] → [1.9, 1.9, 1.8, 1.8, 1.9]
- 원문 검토: latest Server/Agent와 HTTP 관리 포트 노출 예시
- 원문 검토: 일반 Stack Webhook의 현재 BE 제한을 구체적으로 밝히지 않음
- 원문 검토: 이미지 push·Git 변경·webhook·배포 성공의 경계가 추상적
- 원문 검토: branch만 지정한 배포 단계 및 상태 검증·롤백·배포 경합 설명 부족
- 개선: 단일 Docker host에는 socket 직접 연결로 단순화하고 loopback HTTPS 관리 포트만 공개
- 개선: GitOps updates와 BE Stack Webhook을 구분하고 2023 화면/2026 안내를 분리
- 개선: 소스 커밋·image digest·배포 설정 커밋·실행 이미지를 추적하는 보완안 추가
- 개선: curl 버전·timeout·secret trace 중단과 push/branch/success 조건 명시
- 개선: 웹훅 수신과 서비스 정상의 구분, 이전 이미지 복구·DB 제한·직렬 배포를 설명
- 남은 한계: 현재 사용자의 Portainer 버전·에디션 및 webhook을 직접 실행해 확인하지 않았음
- 남은 한계: 예시 webhook step은 이미지 빌드·push·배포 설정 커밋 뒤에 붙이는 조각이며 전체 파이프라인을 새로 구현한 것은 아님
- 남은 한계: 단일 호스트 예시로 무중단·고가용성은 보장하지 않음
- 확인한 자료: [자료 1](https://docs.portainer.io/start/install-ce/server/docker/linux), [자료 2](https://docs.portainer.io/user/docker/stacks/add), [자료 3](https://docs.portainer.io/user/docker/stacks/webhooks), [자료 4](https://docs.portainer.io/faqs/troubleshooting/stacks-deployments-and-updates/how-do-automatic-updates-for-stacks-applications-work), [자료 5](https://docs.drone.io/pipeline/docker/syntax/conditions/), [자료 6](https://github.com/curl/curl-container/releases/tag/8.22.0)

### Terraform으로 AWS 인프라 구축하기

- 파일: `_posts/2023-11-26-Terraform으로 AWS Infra 구축하기.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.6, 1.3, 1.2, 1.5, 1.5] → [1.8, 1.8, 1.8, 1.7, 1.8]
- 원문 검토: 전체 설정 전에 plan/apply를 안내하고 실제 변수 입력 예시가 없음
- 원문 검토: 접근 키 직접 export 위주이며 계정·역할 확인 절차가 없음
- 원문 검토: 고정 listener priority와 인스턴스 ID 기반 Target Group 이름으로 불필요한 결합
- 원문 검토: 인증서·앱 health endpoint·state 잠금·검증 범위가 충분하지 않음
- 개선: 기존 인프라와 새 리소스 범위, 단일 EC2 한계, 인증서·서브넷 접근 경로를 명시
- 개선: SSO profile·계정 확인, 버전 범위와 lockfile 관리, terraform.tfvars 예시 추가
- 개선: 전체 파일 작성 후 저장된 plan 검토·apply하도록 순서를 수정
- 개선: listener priority 변수 검증, Target Group name_prefix·health check·교체 lifecycle 보완
- 개선: 2023 DynamoDB 잠금과 2026 S3 lockfile/deprecation을 구분하고 state 보호·서비스 검증을 보강
- 개선: 독립 검토를 거쳐 EC2 서브넷의 AZ가 기존 ALB에서 활성화되어야 한다는 전제를 추가
- 남은 한계: Terraform CLI와 AWS 자격 증명이 없어 validate/plan/apply 실제 실행은 하지 않았음
- 남은 한계: 기존 외부 예제 저장소는 수정하지 않았으며 본문과 다를 수 있음을 명시
- 남은 한계: 앱 설치·VPC·ALB·인증서·state 저장소 생성은 사전 조건이며 이 글의 생성 범위 밖
- 확인한 자료: [자료 1](https://developer.hashicorp.com/terraform/install), [자료 2](https://developer.hashicorp.com/terraform/language/providers/requirements), [자료 3](https://developer.hashicorp.com/terraform/cli/commands/plan), [자료 4](https://developer.hashicorp.com/terraform/cli/commands/init), [자료 5](https://developer.hashicorp.com/terraform/language/backend/s3), [자료 6](https://developer.hashicorp.com/terraform/language/manage-sensitive-data), [자료 7](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html), [자료 8](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-update-security-groups.html), [자료 9](https://github.com/tfutils/tfenv), [자료 10](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/check-target-health.html)

### 이미지에서 색상 추출하기

- 파일: `_posts/2024-07-22-이미지에서 색상 추출하기.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.7, 1.5, 1.3, 1.5, 1.2] → [1.8, 1.9, 1.8, 1.8, 1.6]
- 원문 검토: 대표색의 의미가 면적 우세색인지 UI 강조색인지 명확하지 않음
- 원문 검토: 브라우저 전용 ImageData를 어댑터 공통 계약으로 사용해 환경 독립성 설명이 불완전함
- 원문 검토: 샘플링·K-means 재현성 설명은 있으나 투명도, 빈 입력, 작은 강조색 검증이 빠짐
- 개선: 팔레트 후보 생성과 대표색 선택 기준을 분리하고 투명도·색 공간의 정책을 설명
- 개선: 8비트 RGBA 샘플링의 입력 검증과 투명 픽셀 제외 예제를 추가하고 실제 실행으로 확인
- 개선: K-means 목적함수와 CIEDE2000을 구분하고 재현성 및 품질 검증 입력을 제시
- 남은 한계: Image Colors 저장소 내용을 확인하지 못했으므로 기존 개발 경험 외의 구현 세부사항은 독립 설계 예시로 한정
- 남은 한계: 실제 이미지 데이터셋의 성능·팔레트 품질 벤치마크는 수행하지 않음
- 확인한 자료: [자료 1](https://html.spec.whatwg.org/multipage/canvas.html#security-with-canvas-elements), [자료 2](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html), [자료 3](https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/), [자료 4](https://github.com/awesomelon/image-colors)

### AI를 이용한 Git Commit 메시지 생성하기

- 파일: `_posts/2024-08-30-AI를 이용한 Git Commit 메시지 생성하기.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.1, 1.2, 1.3, 1.6, 1.1] → [1.9, 1.9, 1.8, 1.8, 1.9]
- 원문 검토: Claude 3.5 사용법과 향후 OpenAI 지원 계획이 현재 생성기 코드와 일치하지 않음
- 원문 검토: 큰 파일은 파일명만 전송한다는 설명이 현재 코드의 diff 제외 동작과 다름
- 원문 검토: Git commit.template 자동 반영 설명이 현재 생성기의 내부 템플릿 사용과 다름
- 원문 검토: AI 출력이 셸 문자열로 실행되는 실제 구현 위험 및 staged diff의 일관성 설명이 빠짐
- 개선: GitHub README와 생성기 코드를 직접 확인해 당시 기능과 현재 구현 차이를 표로 정정
- 개선: Claude Sonnet 3.5 지원 종료일과 설치 버전·API 호환성의 범위를 명시
- 개선: 외부 API 전송 범위와 필터링에 따른 증거 누락을 설명
- 개선: 실제 변경에서 읽을 수 있는 커밋 설명과 지어낸 동기를 구분하고 셸 없는 execFileSync 예제 추가
- 남은 한계: 별도 commitAI 저장소의 코드는 수정하지 않았고 npm 배포본과 API 연동을 실행 검증하지 않음
- 남은 한계: 당시 회고를 보존했으며 모든 과거 릴리스의 실제 기능은 추적하지 않음
- 확인한 자료: [자료 1](https://git-scm.com/docs/git-diff), [자료 2](https://platform.claude.com/docs/en/about-claude/model-deprecations), [자료 3](https://github.com/awesomelon/commitAI/blob/main/README.md), [자료 4](https://github.com/awesomelon/commitAI/blob/main/src/GitCommitMessageGenerator.ts), [자료 5](https://www.conventionalcommits.org/en/v1.0.0/), [자료 6](https://nodejs.org/api/child_process.html#child_processexecfilefile-args-options-callback)

### 기능 분할 설계 (Feature-Sliced Design, FSD)

- 파일: `_posts/2024-09-14-기능분할설계(FSD).md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.6, 1.2, 1.3, 1.6, 1.3] → [1.9, 1.9, 1.9, 1.9, 1.8]
- 원문 검토: 레이어와 장점을 나열하지만 실제 기능 간 의존 충돌을 어디에서 해결할지 예제가 부족함
- 원문 검토: 엔티티 간 명시적 교차 참조 예외와 Public API의 순환 의존 위험 설명이 빠짐
- 원문 검토: 폴더 구조만 보고 도입 여부를 판단하기 쉬우며 변경 비용 검증 기준이 추상적임
- 개선: 레이어·슬라이스·세그먼트를 서로 다른 질문으로 설명하고 현재 processes 상태 명확화
- 개선: 같은 레이어 import 위반과 상위 조합 지점·슬라이스 합치기 대안을 구체화
- 개선: 공개 경계와 내부 상대 경로, @x 예외를 설명하고 필요 레이어만 있는 구조 제시
- 개선: 실제 변경 문제별 작은 개입과 확인 기준으로 도입 판단을 연결
- 남은 한계: 프로젝트별 책임 경계는 팀과 제품 맥락에 따라 달라지며 구조 예시는 유일한 정답이 아님
- 남은 한계: 실제 FSD 예제 저장소의 빌드나 정적 경계 검사까지 수행하지 않음
- 확인한 자료: [자료 1](https://feature-sliced.design/docs/reference/slices-segments), [자료 2](https://feature-sliced.design/docs/reference/layers), [자료 3](https://feature-sliced.design/docs/reference/layers#entity-relationships), [자료 4](https://feature-sliced.design/docs/reference/public-api), [자료 5](https://feature-sliced.design/docs/guides/migration/from-custom), [자료 6](https://github.com/awesomelon/fsd-todo)

### 스크롤은 건드리지마!!

- 파일: `_posts/2024-12-10-스크롤은 건드리지마!!.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.6, 1.1, 1.1, 1.1, 1.3] → [1.9, 1.8, 1.9, 1.9, 1.9]
- 원문 검토: 10개 이유 중 사용자 통제·지연·효율 저하 주장이 반복됨
- 원문 검토: 스크롤 효과의 종류를 구분했지만 결론은 연출 전체를 단정적으로 비판함
- 원문 검토: 접근성·성능 문제의 구체적 재현 과제와 WCAG 등급이 빠짐
- 개선: 기본 관성·CSS 앵커 이동·입력 가로채기·스크롤 연동 장식을 표로 구분
- 개선: 반복 주장을 입력-결과 지연과 대체 구현의 검증 책임으로 통합
- 개선: WCAG 2.3.3 AAA와 키보드 기준 A를 구분하고 접근성 위반 단정 제거
- 개선: 기본 앵커·reduced-motion·scroll-margin 예제와 실제 작업별 회귀 점검 추가
- 남은 한계: 특정 플러그인의 성능이나 보조 기술 조합을 측정한 비교 실험은 아님
- 남은 한계: 검증 표는 주요 회귀 확인용이며 전체 접근성 적합성 판정을 대체하지 않음
- 확인한 자료: [자료 1](https://dontfuckwithscroll.com/), [자료 2](https://www.w3.org/TR/css-overflow-3/#smooth-scrolling), [자료 3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html), [자료 4](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html), [자료 5](https://www.w3.org/TR/css-scroll-snap-1/#scroll-margin)

### DLLM: 기존 LLM과의 차이점과 새로운 가능성

- 파일: `_posts/2025-03-06-LLM 기존 LLM과의 차이점과 새로운 가능성.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.6, 1.1, 1.0, 1.5, 1.2] → [1.9, 1.9, 1.8, 1.9, 1.9]
- 원문 검토: DLLM 전체의 정의와 LLaDA 같은 마스크 확산 구현이 혼재됨
- 원문 검토: 기존 모델과 차이의 반복 설명에 비해 생성 비용과 사용자 체감 지연 비교가 부족함
- 원문 검토: 2025년의 초기 연구 단계 설명을 현재 상태처럼 유지함
- 개선: 설명 범위를 LLaDA 마스크 확산으로 고정하고 이산 토큰과 연속 노이즈 차이를 설명
- 개선: GPT 학습 병렬성·BERT 목표·LLaDA 생성 절차를 분리
- 개선: 512개 위치와 32단계 가상 예제로 단순 속도 배율 계산의 오류를 설명
- 개선: 논문이 뒷받침하는 성과 범위와 상용 API 사례를 구분하고 작업별 평가 기준 제시
- 남은 한계: 모델을 직접 실행하거나 같은 하드웨어·품질로 성능 비교하지 않음
- 남은 한계: Mercury 사례는 공급사의 제품 발표 확인이며 독립적인 성능 검증이 아님
- 확인한 자료: [자료 1](https://ml-gsai.github.io/LLaDA-demo/), [자료 2](https://arxiv.org/abs/2005.14165), [자료 3](https://arxiv.org/abs/1810.04805), [자료 4](https://arxiv.org/html/2502.09992v1), [자료 5](https://arxiv.org/abs/2502.09992), [자료 6](https://www.inceptionlabs.ai/blog/introducing-mercury-2)

### 브레드크럼(Breadcrumbs): 웹에서 필수 도구인가, 재평가 대상인가?

- 파일: `_posts/2025-03-27-브레드크럼(Breadcrumbs).md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.6, 1.3, 1.4, 1.5, 1.3] → [1.9, 1.9, 1.9, 1.9, 1.9]
- 원문 검토: 생존·사망 논쟁과 장단점이 반복돼 실제 도입 결정으로 연결이 약함
- 원문 검토: 경로 깊이 3단계 기준과 ARIA 표준 표현이 과도하게 규범적으로 읽힐 여지가 있음
- 원문 검토: 2025년 Google 모바일 검색 결과 표시 변경이 누락됨
- 개선: 위치·방문 이력·필터의 역할을 나누고 검색 목록 복원을 별도 문제로 설명
- 개선: 깊이 숫자 대신 실제 상위 목적지와 과제로 도입 판단
- 개선: 현재 페이지 링크 여부에 따른 aria-current 규칙과 장식 분리 예제 제공
- 개선: Google 모바일 표시 변경 및 JSON-LD와 접근성 HTML의 차이 반영
- 개선: 클릭률 단독 판단을 피하고 위치 이해·상위 탐색 과제로 검증하도록 개선
- 남은 한계: 사용자 조사·전환 실험 결과가 아닌 설계 판단과 검증 제안
- 남은 한계: 다중 분류에서 대표 경로를 선택하는 구체 정책은 서비스별로 정해야 함
- 확인한 자료: [자료 1](https://webdesignerdepot.com/breadcrumbs-are-dead-in-web-design/), [자료 2](https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/), [자료 3](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb), [자료 4](https://developers.google.com/search/blog/2025/01/simplifying-breadcrumbs)

### Chrome은 이미지 요청 우선순위를 어떻게 결정할까요?

- 파일: `_posts/2025-04-14-Chrome은 이미지 요청 우선순위를 어떻게 결정할까요.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.7, 1.3, 1.5, 1.6, 1.5] → [1.9, 1.9, 1.9, 1.8, 1.9]
- 원문 검토: 규칙과 속성 중심으로 설명해 LCP가 늦는 실제 구간별 판단이 부족함
- 원문 검토: high·low 적용을 일괄 처방처럼 읽을 수 있고 반응형 preload 중복 가능성 설명이 빠짐
- 원문 검토: 스크린샷의 과거 관찰과 현재 모든 Chrome 구현을 구분하는 안내가 부족함
- 개선: 발견 지연·우선순위·다운로드·렌더 지연을 분리하고 LCP 구간별 개입 표 추가
- 개선: 크기 휴리스틱을 악용하지 않고 올바른 width·height를 유지하도록 설명
- 개선: 초기 HTML 핵심 이미지·늦게 발견되는 배경·덜 중요한 이미지의 적용을 분리
- 개선: lazy loading·preload·fetchpriority 차이와 반응형 리소스 불일치를 설명
- 개선: 동일 조건의 우선순위와 실제 LCP·경쟁 리소스를 함께 검증하도록 개선
- 남은 한계: 보존한 스크린샷은 과거 관찰 자료이며 2026년 Chrome 버전별 재측정 결과는 아님
- 남은 한계: 실제 사이트 LCP 개선량은 측정하지 않았고 휴리스틱의 구체 동작은 버전에 따라 바뀔 수 있음
- 확인한 자료: [자료 1](https://www.debugbear.com/blog/chrome-image-request-prioritization), [자료 2](https://web.dev/articles/fetch-priority), [자료 3](https://developer.chrome.com/docs/devtools/network/reference#timing-explanation), [자료 4](https://chromium.googlesource.com/chromium/src/%2B/5fd6239cc261e95c614a255b9367f8dc8e7b5354/third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc), [자료 5](https://web.dev/articles/optimize-cls#images_without_dimensions), [자료 6](https://web.dev/articles/optimize-lcp), [자료 7](https://web.dev/articles/optimize-lcp#optimize_when_the_resource_is_discovered), [자료 8](https://web.dev/articles/preload-responsive-images), [자료 9](https://web.dev/articles/fetch-priority#resource_priority)

### JPEG가 여전히 널리 쓰이는 이유: 압축보다 큰 호환성

- 파일: `_posts/2025-07-01-왜 JPEG가 여전히 웹을 지배하는가.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.6, 1.5, 1.2, 1.5, 1.5] → [1.9, 1.8, 1.9, 1.8, 1.7]
- 원문 검토: 웹을 지배한다는 제목에 해당하는 사용량 통계가 없고 현재 포맷 선택으로 연결되는 기준이 약함
- 원문 검토: GIF 발음·특허 분쟁 세부가 중심 논지와 분리돼 독자의 실무 판단을 방해함
- 원문 검토: JPEG가 무료였다는 마지막 일반화가 앞선 특허 분쟁 설명과 긴장 관계
- 개선: 제목을 널리 쓰이는 이유로 조정하고 압축과 교환 호환성의 구분을 중심 논지로 재구성
- 개선: 색차 서브샘플링·DCT·양자화·엔트로피의 역할과 품질 숫자의 비동등성 설명
- 개선: 사진·UI 캡처·투명 배경·다운로드별 선택 표와 picture 예제, 대표 이미지 비교 절차 추가
- 개선: 원래 3개 이미지 유지 및 출처와 자체 측정 여부 명시
- 남은 한계: 이미지 포맷별 실제 압축률과 기기 표시 시간을 직접 측정하지 않았음
- 남은 한계: 역사 기사의 기존 이미지 예시를 유지했으며 표시용 파일을 원 실험 파일로 간주하지 않음
- 확인한 자료: [자료 1](https://www.w3.org/Graphics/GIF/spec-gif89a.txt), [자료 2](https://spectrum.ieee.org/jpeg-image-format-history), [자료 3](https://www.w3.org/Graphics/JPEG/itu-t81.pdf), [자료 4](https://jpeg.org/jpeg/), [자료 5](https://www.libpng.org/pub/png/pnghist.html), [자료 6](https://developers.google.com/speed/webp/faq), [자료 7](https://html.spec.whatwg.org/multipage/embedded-content.html#the-picture-element)

### AI는 인간을 덜 합리적이라고 가정할까? 게임 실험과 자의식 해석의 한계

- 파일: `_posts/2025-11-24-AI는 당신을 비합리적이라고 생각합니다.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.7, 1.2, 1.2, 1.6, 1.4] → [1.9, 1.9, 1.8, 1.8, 1.8]
- 원문 검토: 기능적 자의식의 창발이라는 소제목이 본문의 신중한 해석보다 강하게 결론을 제시함
- 원문 검토: 21개 모델을 먼저 분류한 뒤 집단 패턴을 요약하는 선택 효과와 두 AI 조건 중앙값 0의 의미를 충분히 설명하지 않음
- 원문 검토: 업무 적용이 막연한 인간 결정권 우려에 머물고 반증 가능한 검증 조건이 부족함
- 개선: 주장형 제목을 질문형으로 바꾸고 관측·저자의 정의·대안 설명·실험 밖 주장을 표로 구분
- 개선: 4200 호출과 28개 모델, 21개 선택 집단의 요약값을 구분
- 개선: 낮은 선택값이 실제 승률과 같지 않음을 설명하고 실제 이력·전문성·표현 변경·실제 대결의 후속 실험 제안
- 개선: 독자 업무에 연결되는 작성자 권위 단서 평가 예시를 검증할 가설로 명시
- 남은 한계: 논문 v1의 재분석·독립 반복 실험을 수행하지 않았음
- 남은 한계: 학습 데이터나 모델 내부 상태를 확인할 수 없으므로 원인에 관한 결론은 보류함
- 확인한 자료: [자료 1](https://arxiv.org/html/2511.00926v1), [자료 2](https://arxiv.org/html/2511.00926v1#S3.T3), [자료 3](https://arxiv.org/abs/2511.00926)

### AI는 버블인가, 혁명인가? 기술·사업·가격을 나눠 보자

- 파일: `_posts/2025-11-25-AI는 버블인가, 혁명인가.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.3, 1.0, 1.0, 1.6, 1.4] → [1.9, 1.8, 1.8, 1.8, 1.7]
- 원문 검토: 기업 CEO 전망을 순서대로 요약하지만 기술 가치·사업 수익성·투자 가격을 구분하는 논지가 약함
- 원문 검토: 인터뷰 한국어 직접 인용과 일자리 전망을 원문 맥락까지 독립 확인하기 어려움
- 원문 검토: CapEx·미래 투자·투자 회수의 관계와 단위 효율·총 에너지 사용량 구분이 부족함
- 개선: 2025년 11월 자료 기준을 명시하고 세 가지 다른 판단과 증거를 표로 정리
- 개선: 검증 어려운 직접 인용을 없애고 Alphabet 공식 실적 자료에 근거한 CapEx와 운영비 부담으로 논지 보강
- 개선: 단계별 사업 원가·반복 사용·설비 이용 등 추적할 신호 및 업무 단위 생산성 설명
- 개선: 냉각 에너지와 총 전력, AlphaFold 예측과 개별 생성형 AI 투자 타당성을 분리
- 남은 한계: 현재 시장 밸류에이션이나 기업별 수익성 모델을 계산한 투자 분석은 아님
- 남은 한계: BBC 인터뷰 영상 자체의 전체 발언을 재전사하지 않아 직접 인용을 제외하고 당시 자료 기반 해설로 구성
- 확인한 자료: [자료 1](https://www.youtube.com/watch?v=BYx63PKKPvg), [자료 2](https://abc.xyz/investor/events/event-details/2025/2025-Q3-Earnings-Call-2025-4OI4Bac_Q9/default.aspx), [자료 3](https://deepmind.google/blog/deepmind-ai-reduces-google-data-centre-cooling-bill-by-40/), [자료 4](https://deepmind.google/blog/alphafold-reveals-the-structure-of-the-protein-universe/)

### AI의 미래와 우리가 던져야 할 질문들

- 파일: `_posts/2025-11-28-AI의 미래와 우리가 던져야 할 질문들.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.2, 1.1, 1.1, 1.6, 1.2] → [1.8, 1.8, 1.9, 1.8, 1.7]
- 원문 검토: 대담 화자의 구체적 발언을 재검증하기 어려우며 광범위한 권력·윤리 질문이 결론 없이 반복됨
- 원문 검토: 모델 정책 공개와 실제 행동의 일치, 접근성과 통제권의 구분이 약함
- 원문 검토: 출처 확인·사실성·신원 확인이 한 문제처럼 연결됨
- 개선: 직접 발언록 대신 대담을 출발점으로 한 해설임을 명시하고 검증된 공식 사례 중심으로 재구성
- 개선: 접근성·통제권·이탈 가능성 및 사실·추론·가치 권고를 구분하는 표 추가
- 개선: OpenAI의 2025년 GPT-4o 동조 문제 회고를 평가 목표의 한계와 연결
- 개선: C2PA를 근거로 사실성·출처·신원을 분리하고 선택권·검증·이탈의 구체적인 제품 조건 제시
- 남은 한계: 대담 전체 전사문과 화자별 정확한 발언은 재확인하지 않아 세부 인용을 제거했음
- 남은 한계: 거버넌스 평가 방법은 제안이며 제품 사용자 연구로 검증한 결과는 아님
- 확인한 자료: [자료 1](https://prod-cf.tuckercarlson.com/tucker-show-sam-altman), [자료 2](https://openai.com/index/introducing-the-model-spec/), [자료 3](https://openai.com/index/sycophancy-in-gpt-4o/), [자료 4](https://spec.c2pa.org/specifications/specifications/2.2/explainer/Explainer.html)

### Chain-of-Visual-Thought (CoVT) 기술 분석

- 파일: `_posts/2025-12-01-Chain-of-Visual-Thought (CoVT) 기술 분석.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.4, 1.5, 1.2, 1.7, 1.4] → [1.9, 1.9, 1.8, 1.8, 1.8]
- 원문 검토: 기존 VLM이 반드시 이미지 전체를 텍스트로 바꾼다는 식의 언어 병목 설명
- 원문 검토: 텍스트와 시각 토큰을 자유롭게 교차하는 추론이 구현된 것처럼 읽히는 표현
- 원문 검토: 외부 전문가 불필요를 근거로 전반적인 추론 효율이 좋다고 단정
- 원문 검토: 시각 신호 4유형과 대표 설정 20개 벡터, 세 유형과 네 유형 결과의 비단조성이 생략됨
- 개선: 기존 VLM의 시각 입력과 텍스트 중심 중간 추론을 구분
- 개선: 시각 토큰 정의 및 SAM8·Depth4·Edge4·DINO4 표 추가
- 개선: 표2 수치와 %p 계산을 원문 대조하고 CV 전체와 하위 과제 중복 및 3유형80.0/4유형79.8 비교 설명
- 개선: Appendix C의 완전 교차 추론 미구현, Appendix B.3의 기반 모델 대비 시간 오버헤드 명시
- 개선: 시각화와 인과 설명을 구분하고 실제 제품 실패 사례의 검증 절차 제시
- 남은 한계: 논문 모델을 실행하거나 자체 데이터셋에서 재현하지 않았음
- 남은 한계: 자연 이미지 벤치마크 결과를 문서 OCR·UI 이해로 전이할 수 있는지는 확인되지 않음
- 확인한 자료: [자료 1](https://arxiv.org/html/2511.19418v1), [자료 2](https://arxiv.org/html/2511.19418v1#S3.SS1), [자료 3](https://arxiv.org/html/2511.19418v1#S3.SS3), [자료 4](https://arxiv.org/html/2511.19418v1#S3.SS4), [자료 5](https://arxiv.org/html/2511.19418v1#A2.SS3), [자료 6](https://arxiv.org/html/2511.19418v1#S3.T2), [자료 7](https://arxiv.org/html/2511.19418v1#A3), [자료 8](https://github.com/facebookresearch/segment-anything), [자료 9](https://depth-anything-v2.github.io/), [자료 10](https://github.com/hellozhuo/pidinet), [자료 11](https://github.com/facebookresearch/dinov2)

### 애플의 LLM 하이퍼파라미터 전이 연구: Complete(d) Parameterisation

- 파일: `_posts/2026-01-03-apple-computed Parameterisation.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.7, 1.5, 1.3, 1.6, 1.5] → [1.9, 1.9, 1.9, 1.8, 1.8]
- 원문 검토: 작은 모델 탐색의 실제 6730 GPU-hours 비용과 적용 손익분기점이 생략됨
- 원문 검토: 학습 기간과 배치의 변화 방향 구분 및 AdamW 모멘텀 보수 계산이 독자에게 추상적임
- 원문 검토: PyTorch AdamW와 AdamLH의 감쇠 관례 및 큰 배율에서 유효 범위를 벗어나는 위험이 생략됨
- 개선: Figure1 원본 숫자 2.31/1.32와 50M→7.2B 비교의 손실·토큰 기준 재확인
- 개선: 배치 증가 시 η·λ·ε·1-β·업데이트 횟수 전체 표 및 β1=.9→.6 검산 예시 추가
- 개선: 감쇠 구현 관례와 전이 가정·유효 범위, 배치와 학습 기간 방향의 차이 설명
- 개선: Appendix D.3 탐색 비용을 명시하고 전이 재사용에 따른 비용 회수 판단 추가
- 개선: 기존 Figure1/3/6 이미지 직접 확인 및 캡션 유지·개선, computed 태그 수정
- 남은 한계: 독립 학습 재현을 수행하지 않았으며 GPU 전체 비용 절감율을 추정하지 않음
- 남은 한계: 다른 모델 구조·데이터·미세조정 조건으로의 일반화는 추가 실험 필요
- 확인한 자료: [자료 1](https://arxiv.org/pdf/2512.22382v1), [자료 2](https://arxiv.org/html/2512.22382v1), [자료 3](https://arxiv.org/html/2512.22382v1#A4.SS3), [자료 4](https://arxiv.org/abs/2512.22382)

### Claude Code 제작자 Boris Cherny의 13가지 사용 팁

- 파일: `_posts/2026-01-04-claude-code-tips.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.4, 1.3, 1.5, 1.5, 1.3] → [1.8, 1.8, 1.9, 1.8, 1.7]
- 원문 검토: 13개 팁마다 일반적인 조언이 반복되고 어떤 문제에 어떤 도구를 쓸지 판단 기준이 약함
- 원문 검토: 훅 실패를 || true로 무시하도록 권장해 자동화 고장을 숨길 가능성
- 원문 검토: 과거 slash commands와 현재 skills 체계, 과거 모델 선호와 현재 추천이 혼재할 여지
- 원문 검토: 테스트·린트는 이름만으로 무해하지 않으며 병렬 세션 충돌·Stop hook 재진입 조건이 부족함
- 개선: 문제→첫 개입→평가 기준 표와 완료까지의 비용 중심 논지 추가
- 개선: 13개 주제와 기존 6개 스크린샷을 보존하면서 독립 작업 경계·지침 삭제 기준·작은 변경의 예외 제시
- 개선: 공식 문서로 skills 통합·teleport 요구·dontAsk·Stop hook 의미 검증
- 개선: 무조건적인 || true 권장 삭제 및 수정 이후 훅의 한계와 실패 가시성 명시
- 개선: 저장 실패 시 입력 유지라는 구체적 완료 조건 예시와 통합 시간·재작업·결함 평가 제시
- 남은 한계: Boris X 원문을 도구로 재열람하지 못해 기존 글의 13개 주제만 유지하고 직접 인용·성과 배수는 제외
- 남은 한계: Claude Code CLI를 직접 실행해 설정을 통합 검증하지 않았으며 현재 문서와 당시 화면이 다를 수 있음
- 확인한 자료: [자료 1](https://x.com/bcherny/status/2007179832300581177), [자료 2](https://code.claude.com/docs/en/best-practices), [자료 3](https://code.claude.com/docs/en/claude-code-on-the-web#from-web-to-terminal), [자료 4](https://code.claude.com/docs/en/best-practices#write-an-effective-claudemd), [자료 5](https://code.claude.com/docs/en/best-practices#explore-first-then-plan-then-code), [자료 6](https://code.claude.com/docs/en/skills), [자료 7](https://code.claude.com/docs/en/sub-agents), [자료 8](https://code.claude.com/docs/en/hooks), [자료 9](https://code.claude.com/docs/en/permissions), [자료 10](https://code.claude.com/docs/en/best-practices#connect-mcp-servers), [자료 11](https://code.claude.com/docs/en/hooks#stop), [자료 12](https://code.claude.com/docs/en/best-practices#give-claude-a-way-to-verify-its-work), [자료 13](https://code.claude.com/docs/en/claude-code-on-the-web), [자료 14](https://code.claude.com/docs/en/github-actions)

### 코딩 에이전트가 코드를 빨리 써도, 제품은 저절로 좋아지지 않는다

- 파일: `_posts/2026-05-07-코딩 에이전트가 코드를 빨리 써도, 제품은 저절로 좋아지지 않는다.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.6, 1.6, 1.4, 1.4, 1.6] → [1.9, 1.9, 1.9, 1.9, 1.8]
- 원문 검토: 병목은 판단이라는 주장을 팀 조건과 구분하지 않고 반복
- 원문 검토: 경쟁 제품 격차와 시니어/주니어 격차를 생산성 판단으로 확장할 여지
- 원문 검토: 문서화·좋은 판단에 대한 결론이 반복되고 사용자 성과를 확인할 구체적 방법이 부족
- 개선: 원문 요약을 줄이고 제품 가치에 집중해 280줄에서 118줄로 편집
- 개선: 가상 10일 작업의 구현·리뷰·배포 대기를 분리하고 전체 개선 10% 계산
- 개선: 가상 문서 검색 요청의 대안 원인과 개입을 비교
- 개선: 구현·전달·품질·제품 지표 및 교란 요인, 의사결정 기록 예시 추가
- 남은 한계: 에세이의 관점과 제안이며 실제 사용자 개선 실험은 미실시
- 남은 한계: 새로 추가한 사례와 숫자는 가상임을 본문에 표시
- 확인한 자료: [자료 1](https://www.thetypicalset.com/blog/thoughts-on-coding-agents), [자료 2](https://ethanding.substack.com/p/claude-code-is-not-making-your-product)

### AI 시대의 좋은 개발자는 코드를 더 많이 만들지 않는다

- 파일: `_posts/2026-05-12-AI 시대의 좋은 개발자는 코드를 더 많이 만들지 않는다.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.8, 1.8, 1.6, 1.4, 1.8] → [1.9, 1.9, 1.9, 1.7, 1.9]
- 원문 검토: 장기 유지보수 주제에서 고용 전망·연령별 고용·AI 설문으로 논점 분산
- 원문 검토: 도구 사용 방식을 결과의 유일한 원인처럼 표현
- 원문 검토: AI 리뷰의 독립성과 모든 변경에 동일 검증을 요구하는 비용이 불분명
- 개선: 노동시장·도입 통계 등 유지비와 직접 연결되지 않는 단락 제거
- 개선: 사전 공개 논문과 관찰 연구의 한계를 유지하고 최신 METR 설계 문제 확인
- 개선: AI 리뷰의 공유 전제 위험과 위험 수준에 비례한 검증 명시
- 개선: 유지비 비교 절차와 계약·회귀·변경 범위·이후 수정 비용의 증거 표 추가
- 개선: 코드 줄 수 최소화와 유지비 최소화를 명시적으로 구분
- 남은 한계: 문헌의 작업·도구·시점이 서로 달라 효과를 하나로 합산할 수 없음
- 남은 한계: 장기 유지비와 학습에 대한 본인 실증 데이터 없음
- 확인한 자료: [자료 1](https://www.jamesshore.com/v2/blog/2026/you-need-ai-that-reduces-your-maintenance-costs), [자료 2](https://www.seangoedecke.com/software-engineering-may-no-longer-be-a-lifetime-career/), [자료 3](https://arxiv.org/html/2603.28592v2), [자료 4](https://github.blog/news-insights/research/does-github-copilot-improve-code-quality-heres-what-the-data-says/), [자료 5](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/), [자료 6](https://metr.org/blog/2026-02-24-uplift-update/)

### AI 에이전트를 많이 돌리면 정말 생산성이 올라갈까

- 파일: `_posts/2026-05-29-AI 에이전트를 많이 돌리면 정말 생산성이 올라갈까.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.7, 1.6, 1.5, 1.7, 1.6] → [1.9, 1.9, 1.9, 1.8, 1.7]
- 원문 검토: 병렬화를 테스트·문서 같은 작업 종류로 분류해 실제 의존성 간과 가능
- 원문 검토: 동시 실행 수를 늘릴지 줄일지 판단할 관찰 기준 부재
- 원문 검토: 주의력 관련 원칙 반복
- 개선: 파일·공통 API 계약·가설 조사·독립 리뷰별 병렬화 기준 표 추가
- 개선: 별도 worktree가 의미상 충돌을 해결하지 않는다는 한계 명시
- 개선: 리뷰 대기 수·대기 시간·통합량·재수정 비용으로 동시 실행 수 조정
- 개선: 하루 8개 생성/3개 통합 가상 예시와 병목 해소용 위임의 예외 설명
- 남은 한계: 일인 검토자 중심의 운영 관점으로 팀별 최적 동시 작업 수를 실증하지 않음
- 남은 한계: 대기열 숫자는 원리를 설명하기 위한 가상 예시
- 확인한 자료: [자료 1](https://addyosmani.com/blog/orchestration-tax/)

### macOS에서 만든 한글 파일명이 검색되지 않는 이유

- 파일: `_posts/2026-07-03-macOS에서 만든 한글 파일명이 검색되지 않는 이유.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.6, 1.7, 1.6, 1.6, 1.8] → [2.0, 1.9, 1.9, 1.8, 1.9]
- 원문 검토: 입력 보정만으로 새 데이터 문제를 막았다는 결론이 저장 경쟁 조건 한계와 충돌
- 원문 검토: password 제외 외 모든 text를 정규화하면 식별자 변형 위험
- 원문 검토: 실행 가능한 코드 포인트 재현과 요청 경계 예시 부족
- 원문 검토: 기존 데이터 정규화·인덱스·식별자 충돌 처리 구체성 부족
- 개선: APFS 보존과 정규화 무시 비교를 Apple 문서의 버전 조건과 연결
- 개선: NFC/NFD 코드 포인트를 출력하는 JavaScript 최소 예제 추가 및 실행 검증
- 개선: 표시 이름만 정규화하고 storageKey를 보존하는 요청 생성 예제 추가
- 개선: 실제 경험과 권장 보완 방향을 구분하고 결론의 과도한 해결 표현 수정
- 개선: IME·즉시 저장·기존 데이터·중복 이름·원문 보존 검증 표 추가
- 개선: NFKC·초성 검색·인덱스와 마이그레이션을 분리
- 남은 한계: 원 서비스 DB와 브라우저에서 통합 회귀 검증은 하지 못함
- 남은 한계: 요청 생성 TypeScript 예제는 설명용이며 사용자 프로젝트 적용 결과를 주장하지 않음
- 확인한 자료: [자료 1](https://www.unicode.org/reports/tr15/), [자료 2](https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/APFS_Guide/FAQ/FAQ.html), [자료 3](https://tc39.es/ecma262/multipage/text-processing.html#sec-string.prototype.normalize), [자료 4](https://www.postgresql.org/docs/current/collation.html#COLLATION-NONDETERMINISTIC)

### 에이전트 코드베이스에서 리팩터링이 돈이 되는 이유

- 파일: `_posts/2026-08-03-에이전트 코드베이스에서 리팩터링이 돈이 되는 이유.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.8, 1.6, 1.4, 1.6, 1.8] → [1.9, 1.9, 1.9, 1.9, 1.9]
- 원문 검토: 단일 대표 작업 결과에 비해 경제적·설계상 결론이 넓음
- 원문 검토: 입력 토큰 절감과 작업 시간 증가를 투자 결정으로 연결하는 방법 부족
- 원문 검토: 원문 요약이 길고 독자가 적용할 실험 절차가 부족
- 개선: 원문 줄 수·추정 입력/출력·소요 시간을 전후 표로 압축
- 개선: 83%는 추정 입력량 감소이며 청구 비용이나 실행 시간 개선이 아님을 선명하게 구분
- 개선: 같은 단위의 총비용·반복 횟수 손익분기 모델과 가상 계산 추가
- 개선: 여러 유형의 대표 변경, 동일 완료 조건, 격리 체크아웃, 반복 편차를 포함한 검증 계획
- 개선: 리팩터링 후보별 최소 개입과 중단 신호 표 추가
- 남은 한계: 원 실험은 자체 보고 문자 기반 근사치이고 반복 통계·정확한 리팩터링 비용 없음
- 남은 한계: 새 비용 모델과 실험 계획은 제안이며 실제 ROI 실측 아님
- 확인한 자료: [자료 1](https://martinfowler.com/articles/exploring-gen-ai/refactoring-economic-benefit.html)

### AI로 만들기 쉬워진 시대, 차별화를 만드는 안목

- 파일: `_posts/2026-08-06-AI가 모든 것을 만들 수 있는 시대, 진짜 차별화는 취향이다.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.4, 1.3, 1.2, 1.6, 1.4] → [1.9, 1.8, 1.9, 1.8, 1.8]
- 원문 검토: 안목·느낌은 복제 불가라는 주장과 신뢰를 빨리 얻는 것이 경쟁 지표라는 단정
- 원문 검토: 안목을 결과적으로 맞은 판단으로 정의해 사후 해석·취향과 구분이 어려움
- 원문 검토: 실제 제품 선택과 검증 방법 없이 추상 주장 반복
- 개선: 안목을 사전 판단 기준과 사후 수정 조건으로 정의
- 개선: 기술·유통·운영과 안목을 함께 보고 해자 주장에 경계 설정
- 개선: 가상 문서 요약 기능의 간결함·출처·자동 반영·통제 비용 비교 표
- 개선: 신뢰 인상과 실제 정확성 및 검증 가능성을 구분
- 개선: 2019 인간-AI 상호작용 연구 연결 및 팀 학습 절차 추가
- 남은 한계: 안목과 성장의 인과효과를 검증한 연구가 아닌 개인 해석
- 남은 한계: 문서 요약 설계 비교는 실제 제품 측정이 아닌 가상 사례
- 확인한 자료: [자료 1](https://www.thevccorner.com/p/why-taste-is-the-new-moat), [자료 2](https://www.paulgraham.com/taste.html), [자료 3](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/)

### 웹에서 HEVC with Alpha 영상을 사용할 때 고려해야 할 것들

- 파일: `_posts/2026-09-04-웹에서 HEVC with Alpha 영상을 사용할 때 고려해야 할 것들.md`
- 세부 점수(정확성·깊이·실용성·구성·출처): [1.8, 1.8, 1.7, 1.7, 1.8] → [1.9, 2.0, 1.9, 1.8, 1.9]
- 원문 검토: 용량/디코딩 구분은 좋지만 실제 파일 선택을 위한 통제 비교 계획 부재
- 원문 검토: 가상 메모리 숫자가 실측처럼 읽힐 수 있음
- 원문 검토: Range 부분 전달과 적응형 화질, MB/MiB 헤더 예제 구분 부족
- 원문 검토: 동시 재생 감소 효과를 구체적 측정 없이 지나치게 크게 예상
- 개선: Apple·S3·CloudFront·WHATWG 기술 주장에 본문 근거 연결
- 개선: Range와 적응형 비트레이트 차이 및 헤더 크기의 8MiB 단위 명시
- 개선: 메모리 숫자를 가상 예시로 표시하고 단순 증가로 누수 확정 방지
- 개선: 동일 파일 크기/해상도/동시 재생/캐시/지원 환경 비교표와 측정 계획 추가
- 개선: CSS 표시 크기·DPR 기반 낮은 해상도 후보와 실제 기기 검증 한계 설명
- 개선: 동시 재생 감소의 우월성 단정을 비교할 가설로 수정
- 남은 한계: 실제 원본 3개 영상·대상 기기에서 재생/화질/메모리 측정 불가
- 남은 한계: 브라우저/OS 지원표는 실제 대상 파일의 Alpha 재생 보장과 다름
- 남은 한계: 기존 실제 경험은 보존했으며 신규 성능 수치나 측정 성공을 만들지 않음
- 확인한 자료: [자료 1](https://developer.apple.com/videos/play/wwdc2019/506/), [자료 2](https://developer.chrome.com/blog/alpha-transparency-in-chrome-video), [자료 3](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/RangeGETs.html), [자료 4](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html), [자료 5](https://html.spec.whatwg.org/multipage/media.html#media-elements)
