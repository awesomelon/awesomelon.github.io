---
title: "AI를 이용한 Git Commit 메시지 생성하기"
date: 2024-08-30 14:58:00 +0900
last_modified_at: 2026-09-12 13:38:07 +0900
categories: [ENGINEERING, PLAYGROUND]
tags: [ai, git, claude ai, cli, commit message, 자동화]
author: j-ho
img_path: /assets/img/for_post/
pin: false
description: commit-ai 개발 배경과 실제 소스를 바탕으로 좋은 커밋 메시지, diff 범위, 응답 검증과 안전한 Git 실행을 살펴봅니다.
---

Git을 쓰다 보면 작업보다 커밋 메시지 작성이 더 귀찮게 느껴질 때가 있어요. 결국 `fixed` 같은 메시지를 남기고, 나중에 "무엇을 왜 고쳤지?" 하고 다시 코드를 읽게 되죠. 그래서 **diff를 보고 커밋 메시지 초안을 만드는 CLI, `commit-ai`**를 만들었습니다.

![commit-ai 동작 예시](2024-08-30-example.gif)
_commit-ai의 메시지 생성·선택 과정_

이 글은 2024년 개발 기록에 2026년 9월 소스 확인 내용을 보충한 것입니다. 당시 설명과 현재 구현이 다른 부분은 구분했습니다. 패키지 설치만으로 현재 API와의 호환성까지 보장되는 것은 아닙니다.

## 자동화하고 싶었던 일

원하는 흐름은 단순했습니다. 스테이징한 변경을 읽고, 여러 메시지를 제안하고, 사람이 선택하거나 수정한 뒤 커밋하는 것이었어요. 다국어와 메시지 템플릿, 대화형 편집도 넣었습니다.

하지만 diff가 알려주는 것은 주로 **무엇이 바뀌었는지**입니다. "고객사에서 재현된 문제를 막기 위해서"처럼 코드 밖에 있는 동기는 모델이 알아낼 수 없어요. 그 부분까지 그럴듯하게 채우면 기록의 신뢰도가 오히려 떨어집니다.

가령 다음은 가상의 변경 예시입니다.

```diff
- if (document) {
+ if (document?.status === 'completed') {
    download(document);
  }
```

`fix: 완료된 문서만 다운로드하도록 제한`은 변경에서 읽을 수 있는 설명입니다. 반면 "보안 사고를 해결했다"거나 "고객 오류를 90% 줄였다"는 설명은 별도 근거가 필요해요. AI의 역할은 초안을 만드는 것이고, 커밋의 의도와 검증 결과를 책임지는 사람은 작성자입니다.

## 실제 입력은 working tree가 아니라 staged diff

커밋될 변경만 읽어야 메시지와 커밋이 일치합니다. `git diff`는 기본적으로 작업 디렉터리와 인덱스를 비교하고, `git diff --staged`는 인덱스와 기준 커밋의 차이를 보여줍니다. 같은 파일을 일부만 스테이징한 상황에서 특히 중요한 차이예요. [Git diff 공식 문서](https://git-scm.com/docs/git-diff)

```bash
# 커밋할 변경을 골라 스테이징
git add -p

# 실제 커밋 범위와 내용을 확인
git diff --staged --stat
git diff --staged
```

생성 도중 다른 터미널에서 스테이징을 바꾸면 메시지와 실제 커밋 범위가 어긋날 수 있습니다. CLI를 개선한다면 **메시지 생성에 사용한 diff와 커밋 직전 diff가 같은지** 확인하고, 달라졌을 때 다시 생성하게 하는 편이 좋겠어요.

## 당시 사용법과 현재 확인한 차이

2024년 소개한 버전의 설치 명령은 다음과 같습니다.

```bash
npm install -g @j-ho/commit-ai
commit-ai --help
```

당시에는 Anthropic API 키를 설정하고 Claude 3.5로 메시지를 만들었습니다. 다만 Claude Sonnet 3.5 모델은 2025년 10월 28일 Claude API에서 지원이 종료됐습니다. 오래된 모델 ID를 그대로 쓰면 요청이 실패할 수 있어요. [Anthropic 모델 지원 종료 문서](https://platform.claude.com/docs/en/about-claude/model-deprecations)

2026년 9월 12일 확인한 [README](https://github.com/awesomelon/commitAI/blob/main/README.md)와 [메시지 생성기 소스](https://github.com/awesomelon/commitAI/blob/main/src/GitCommitMessageGenerator.ts)에는 다음 차이도 있었습니다.

| 항목 | 확인한 내용 |
|:---|:---|
| AI 제공자 | README는 Claude 중심이지만 생성기에는 OpenAI·Anthropic 분기가 있음 |
| 기본 제공자 | 생성기 코드의 기본값은 OpenAI |
| 대용량 제외 기준 | 파일의 전체 크기 대신 파일별 diff의 UTF-8 바이트 크기를 계산 |
| 제외된 변경 | 현재 생성기는 해당 diff를 건너뜀. 파일명 요약을 함께 보내는 구현은 아님 |
| 템플릿 | 현재 생성기는 내부 `COMMIT_MESSAGE_TEMPLATE`를 사용. Git의 `commit.template` 자동 반영으로 단정할 수 없음 |

소스의 기능이 npm 최신 배포본이나 CLI 옵션에 그대로 연결돼 있는지는 별도 확인이 필요합니다. 다시 사용한다면 설치 버전, `--help`, 제공자와 모델 설정을 먼저 맞춰야 해요. API 키를 명령행 인자로 직접 쓰는 방식은 셸 기록에 남을 수 있으므로, 도구의 입력·저장 방식을 확인하는 것도 필요합니다.

## 입력을 줄이는 순간 무엇을 잃는가

잠금 파일과 SVG, 소스맵, 큰 diff를 제외하면 입력량은 줄어듭니다. 그러나 잠금 파일 변경이 의존성 업데이트의 핵심일 수도 있고, SVG 수정이 이번 커밋의 전부일 수도 있어요. 필터링은 단순한 성능 최적화가 아니라 **모델이 보게 되는 근거를 바꾸는 결정**입니다.

더 나은 방식은 제외된 파일과 이유를 사용자에게 보여주고, 중요한 변경은 포함 여부를 선택하게 하는 것입니다. 포함된 diff만으로 전체 커밋을 설명하기 어렵다면 자동 생성을 멈추고 직접 작성할 수 있어야 해요.

파일별 100KB 제한은 전체 요청의 토큰 한도를 보장하지 않습니다. 작은 diff가 많이 쌓일 수 있고, 바이트와 토큰은 같은 단위가 아니기 때문입니다. 전체 입력 예산을 별도로 관리하고, 초과 시 변경을 의미 단위로 나누는 선택지를 주는 편이 낫습니다.

또한 staged diff에는 비밀 키나 고객 데이터가 들어갈 수 있습니다. 회사 코드에 사용한다면 외부 API로 보내는 범위를 확인해야 합니다. 확장자 필터를 민감 정보 검사로 간주하면 안 됩니다.

## 응답이 JSON이라고 검증이 끝나는 것은 아니다

당시에는 Markdown JSON 블록, JSON 본문, 번호 목록을 순서대로 파싱하는 방식을 사용했습니다. 형식이 흔들리는 응답을 받아들이기 위한 선택이었어요.

다만 JSON 파싱 성공과 유효한 메시지는 다릅니다. `title`과 `body`가 문자열인지, 제목이 비어 있지 않은지, 허용한 길이와 형식을 지키는지 확인해야 합니다. 형식을 복구할수록 모델의 잘못된 응답을 정상처럼 받아들일 가능성도 생기므로, 실패하면 수동 편집으로 넘어갈 수 있어야 합니다.

Conventional Commits의 기본 형태는 `type(scope): description`입니다. `scope`는 선택 사항이고, `!` 또는 `BREAKING CHANGE:`는 호환성을 깨는 변경을 표시합니다. 제목 50자나 본문 72자 같은 관례는 팀에서 정할 수 있지만 이 명세의 필수 규칙은 아닙니다. [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)

## 모델의 출력은 셸 명령이 아니라 데이터로 전달하기

확인한 생성기에는 메시지를 `execSync()`의 셸 문자열에 넣는 구현이 남아 있습니다. 큰따옴표만 치환하는 것으로 모든 셸 해석을 막을 수는 없어요. 자동 생성된 텍스트를 실행 경계에 넘기는 도구라면 이 부분을 먼저 고쳐야 합니다.

아래는 그 경계를 개선하는 **별도 구현 예시**입니다. 기존 패키지에 반영됐다는 뜻은 아닙니다.

```typescript
import { execFileSync } from 'node:child_process';

function commitMessage(title: string, body: string): void {
  if (!title.trim() || /[\r\n\0]/.test(title) || body.includes('\0')) {
    throw new Error('커밋 메시지 형식이 올바르지 않습니다.');
  }

  // shell을 활성화하지 않고 각 인자를 Git에 직접 전달합니다.
  execFileSync('git', ['commit', '-m', title, '-m', body], {
    stdio: 'inherit',
  });
}
```

Node.js의 `execFile` 계열은 기본적으로 셸을 거치지 않습니다. 이 구분은 파일명으로 diff를 읽는 코드에도 똑같이 적용됩니다. [Node.js child_process 문서](https://nodejs.org/api/child_process.html#child_processexecfilefile-args-options-callback)

처음에는 메시지를 빨리 만드는 것이 목표였지만, 도구를 다시 보면 더 중요한 기준이 보입니다. **커밋될 변경을 정확히 읽는가, 모르는 의도를 지어내지 않는가, 사람이 수정·취소할 수 있는가, 생성된 텍스트를 안전하게 전달하는가.** 후보 문장을 더 멋지게 만드는 일보다 이 경계를 다듬는 것이 다음 개선의 우선순위입니다.
