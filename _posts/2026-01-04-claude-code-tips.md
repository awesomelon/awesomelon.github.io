---
title: "Claude Code 제작자 Boris Cherny의 13가지 사용 팁"
date: 2026-01-04 10:00:00 +0900
categories: [ENGINEERING, PLAYGROUND]
tags: [claude code, claude ai, cli, workflow, productivity, mcp, 자동화, 프롬프트]
author: j-ho
img_path: /assets/img/for_post/
pin: false
description: Claude Code 제작자 Boris Cherny의 실제 워크플로우(병렬 세션, Plan mode, CLAUDE.md, slash command, sub-agent, hooks, permissions, MCP, 검증 루프)를 한국어로 정리합니다.
---

> **📌 KEYWORDS**  
> `Claude Code` `Plan mode` `병렬 세션` `CLAUDE.md` `Slash Commands` `Sub-agents` `Hooks` `Permissions` `MCP` `검증 루프`
{: .prompt-info }

> **📄 출처**  
> 이 글은 Claude Code 제작자 **Boris Cherny**가 공유한 “Claude Code 사용 팁(1~13)”을 바탕으로 작성했습니다.
{: .prompt-info }

---

## 🚀 들어가며

Claude Code를 쓰다 보면 결국 이런 질문으로 돌아오곤 합니다.

> “잘 쓰는 사람은 대체 어떻게 쓰지?”

재미있는 점은, Claude Code를 만든 Boris의 셋업이 **의외로 ‘바닐라(vanilla)’**라는 것입니다. 기본이 이미 좋아서, 그는 과도한 커스터마이징보다는 **반복되는 루프를 자동화**하고, **검증을 붙여 품질을 끌어올리는 방식**에 더 많은 에너지를 씁니다.

그리고 이 글에서 가장 중요한 메시지는 두 가지입니다.

- 정답은 없다. 팀과 개인의 워크플로우에 맞게 커스터마이즈하라.
- 단, “검증 루프”를 만들면 결과물이 2~3배 좋아진다.

## ✅ 한 장 요약(바로 적용 체크리스트)

- **(1) 병렬 세션**: 터미널/웹에서 여러 Claude를 동시에 돌리고 알림으로 회수한다.
- **(2) Plan mode**: PR 목표라면 계획을 먼저 다듬고, 실행은 1-shot을 노린다.
- **(3) CLAUDE.md 운영**: “자주 틀리는 것”을 팀 규칙으로 박제해서 재발을 줄인다.
- **(4) Slash command/Sub-agent/Hooks**: 반복 작업은 명령/에이전트/훅으로 자동화한다.
- **(5) Permissions/MCP**: 권한 프롬프트와 외부 도구 연동을 ‘팀 설정’으로 관리한다.
- **(6) 검증 방법 제공**: 테스트/브라우저 검증 등 피드백 루프를 Claude에게 준다.

---

## 1. 터미널에서 5개 세션 병렬 + 시스템 알림으로 회수하기

Boris는 터미널에서 **5개의 Claude 세션을 동시에** 돌리고, 탭을 1~5로 번호 붙여 관리합니다. 중요한 건 “기다리지 말고”, **알림으로 회수**하는 방식입니다.

- **핵심 요약**: 입력이 필요한 순간에만 알림으로 회수하면, 병렬 세션이 “생산성”이 됩니다.
- **바로 따라하기**:
  - 탭을 1~5로 번호를 붙이고, 각 탭 역할(리뷰/리팩터/테스트/문서)을 정해둡니다.
  - iTerm2의 시스템 알림을 켜서, 입력이 필요할 때 놓치지 않게 합니다.
- **참고 링크**: [iTerm 2 system notifications](https://code.claude.com/docs/en/terminal-config#iterm-2-system-notifications)
- **주의/트레이드오프**: 세션이 늘수록 문맥 스위칭 비용이 증가합니다. “항상 5개”보다 “필요할 때만 5개”가 더 현실적일 때도 많습니다.

## 2. 웹(claude.ai/code)에서도 5~10개 병렬 + &/teleport/모바일 세션

터미널만이 아닙니다. Boris는 `claude.ai/code`에서도 **5~10개 세션을 병렬**로 운영합니다. 로컬 세션을 웹으로 넘기거나(`&`), `--teleport`로 오가고, 아침마다 모바일(Claude iOS 앱)에서 몇 개 세션을 시작해두고 나중에 확인하기도 합니다.

![claude.ai/code 병렬 세션](2026-01-04-image1.png)
_웹(claude.ai/code)에서 여러 세션을 병렬로 운영하는 예시_

- **핵심 요약**: 아이디어/리서치를 먼저 병렬로 뿌려두고, “유효한 것만” 회수합니다.
- **바로 따라하기**:
  - 성격이 다른 작업(리서치/코딩/검증/문서화)을 세션 단위로 분리합니다.
  - 세션 첫 메시지에 “목표/완료 조건”을 적어, 나중에 다시 들어갔을 때 시간을 아끼세요.
- **주의/트레이드오프**: 세션 수가 늘면 관리 비용이 생깁니다. “세션을 늘리는 것” 자체가 목적이 되지 않게, 회수 기준을 명확히 잡는 게 좋습니다.

## 3. Opus 4.5 + thinking을 기본값으로 사용하기

Boris는 **Opus 4.5 + thinking**을 거의 모든 작업의 기본값으로 씁니다. Sonnet보다 크고 느릴 수 있지만, **덜 조종해도 되고(tool use가 안정적이라), 결국 전체 속도가 더 빠른 경우가 많다**는 이유입니다.

- **핵심 요약**: 모델은 “단일 응답 속도”가 아니라 “완료까지의 왕복 횟수”로 평가해야 합니다.
- **바로 따라하기**:
  - 복잡한 작업(대규모 수정/디버깅/테스트 반복)은 큰 모델이 오히려 유리할 수 있습니다.
  - 단순 생성/요약처럼 조종 비용이 낮은 작업은 더 작은 모델이 합리적일 수 있습니다.
- **주의/트레이드오프**: 팀 예산/쿼터가 제한적이면 “기본은 가볍게, 중요한 구간만 상향” 전략이 현실적입니다.

## 4. 팀이 공유하는 `CLAUDE.md`를 git에 체크인하고 계속 업데이트하기

Claude Code 팀은 레포에 **공용 `CLAUDE.md`**를 두고, 팀원들이 자주 업데이트합니다. Claude가 뭔가를 “잘못”하면, 그 내용을 `CLAUDE.md`에 추가해서 다음번엔 같은 실수를 줄이는 방식입니다. 다른 팀은 각자 자신들의 `CLAUDE.md`를 운영하기도 합니다.

![팀 공용 CLAUDE.md 예시](2026-01-04-image2.png)
_git에 체크인해서 팀이 함께 유지보수하는 CLAUDE.md_

- **핵심 요약**: 프롬프트는 ‘한 번 잘 쓰는 문장’이 아니라, **팀이 유지보수하는 규칙 집합**입니다.
- **바로 따라하기**:
  - “절대 하면 안 되는 것”과 “PR 전에 반드시 해야 하는 것”을 먼저 고정합니다.
  - Claude가 반복적으로 틀리는 패턴이 보이면, 그 즉시 `CLAUDE.md`에 추가합니다.
- **참고 링크**: [Claude Code Docs](https://code.claude.com/docs/)
- **주의/트레이드오프**: `CLAUDE.md`가 너무 길어지면 비용이 올라갑니다. “회귀 위험이 큰 것” 위주로 유지하는 편이 좋습니다.

## 5. 코드리뷰에서 @.claude로 `CLAUDE.md` 업데이트를 PR 일부로 만들기

Boris는 코드리뷰 중에 동료 PR에 **@.claude**를 태그해, “이번에 배운 규칙을 `CLAUDE.md`에 반영하자”를 PR의 일부로 만들곤 합니다. 이를 위해 Claude Code GitHub action(예: `/install-github-action`)을 사용합니다.

![PR 코멘트로 CLAUDE.md 업데이트 요청](2026-01-04-image3.png)
_코드리뷰 중 ‘규칙 업데이트’를 PR 일부로 만드는 예시_

- **핵심 요약**: 개인의 배움을 팀의 규칙으로 승격시키면, 누적 효과(compounding)가 생깁니다.
- **바로 따라하기**:
  - 리뷰에서 “다음에도 또 틀릴 듯” 싶은 포인트를 발견하면, 즉시 규칙 업데이트를 함께 요청합니다.
  - 규칙 변경이 합의되면, 같은 PR에서 함께 반영해 회귀를 줄입니다.
- **주의/트레이드오프**: 규칙은 늘릴수록 생산성을 갉아먹을 수 있습니다. 팀 합의와 기준(언제 규칙으로 올릴지)이 필요합니다.

## 6. 대부분의 세션은 Plan mode로 시작한다(계획이 PR 품질을 좌우)

Boris는 대부분의 세션을 **Plan mode**로 시작합니다(예: `shift+tab` 두 번). 목표가 Pull Request라면 Plan mode로 계획을 다듬고, 만족스러우면 auto-accept edits 모드로 전환해 구현을 1-shot에 가깝게 시도합니다.

![Plan mode on](2026-01-04-image4.png)
_Plan mode에서 계획을 확정한 뒤 실행으로 넘어가기_

- **핵심 요약**: 좋은 계획이 있으면 구현은 빨라지고, 리뷰/회귀 위험은 줄어듭니다.
- **바로 따라하기**:
  - 계획에 “변경 범위/리스크/테스트 전략/롤백”이 포함됐는지 확인합니다.
  - 계획이 마음에 들 때까지 질문으로 다듬고, 그 다음 실행으로 넘어갑니다.
- **주의/트레이드오프**: 계획을 길게 쓰는 게 목적이 아닙니다. 실행 가능한 체크리스트 정도가 가장 효율적일 때가 많습니다.

## 7. 매일 반복하는 작업은 slash command로 만든다

Boris는 하루에 여러 번 하는 작업을 **slash command**로 표준화합니다. 커맨드는 `.claude/commands/`에 두고 git에 체크인해 팀이 공유합니다. 예로 `/commit-push-pr` 같은 커맨드는 인라인 bash로 `git status`를 미리 계산해, 모델과의 왕복을 줄입니다.

- **핵심 요약**: 반복 프롬프트를 줄이면, 사람도 덜 지치고 Claude도 더 안정적으로 일합니다.
- **바로 따라하기**:
  - 내 “inner loop”(커밋/푸시/PR/리포맷/테스트)를 나열합니다.
  - 가장 빈도가 높은 1~2개부터 slash command로 고정합니다.
- **참고 링크**: [Bash command execution](https://code.claude.com/docs/en/slash-commands#bash-command-execution)
- **주의/트레이드오프**: 인라인 bash는 편하지만 환경 의존이 커질 수 있습니다. 팀 공유 커맨드는 최소한의 가정 위에서 설계하는 게 좋습니다.

## 8. 서브에이전트로 공통 PR 워크플로우를 자동화한다

Boris는 `code-simplifier`, `verify-app` 같은 **서브에이전트(sub-agent)**를 정기적으로 사용합니다. slash command가 “작은 명령”이라면, sub-agent는 “반복되는 워크플로우 전체”를 자동화하는 개념입니다.

- **핵심 요약**: PR마다 반복되는 ‘후처리’를 자동화하면 결과물이 누적해서 좋아집니다.
- **바로 따라하기**:
  - 대부분의 PR에 공통으로 필요한 루프(정리/단순화/검증/문서)를 sub-agent로 분리합니다.
  - sub-agent 지시문에는 입력/출력/검증 기준을 명확히 적습니다.
- **참고 링크**: [Sub-agents](https://code.claude.com/docs/en/sub-agents)
- **주의/트레이드오프**: 에이전트가 많아질수록 관리 비용이 생깁니다. “자주 쓰는 것” 위주로 제한하는 편이 좋습니다.

## 9. PostToolUse hook으로 포맷팅(마지막 10%를 자동 처리)

Claude가 보통은 포맷을 잘 맞추지만, CI에서 “마지막 10%”가 터지는 순간이 있습니다. Boris 팀은 **PostToolUse hook**으로 포맷팅을 자동 적용해, 포맷 실수로 인한 CI 실패를 줄입니다.

![PostToolUse hook 예시](2026-01-04-image5.png)
_tool use 이후 포맷을 자동으로 맞추는 PostToolUse hook 예시_

- **핵심 요약**: 실패가 자주 나는 지점을 자동화하면, 리뷰/CI 비용이 줄어듭니다.
- **바로 따라하기**:
  - 프로젝트에 맞는 포맷터(prettier/rubocop/black 등)를 훅에서 실행합니다.
  - 훅이 실패해도 진행을 막지 않도록 설계하되(예: `|| true`), CI에서 반드시 잡히게 만드는 전략도 가능합니다.
- **주의/트레이드오프**: 자동 수정은 “왜 바뀌었는지”가 안 보일 수 있습니다. 팀이 훅 동작을 이해할 수 있도록 문서화가 필요합니다.

## 10. `--dangerously-skip-permissions` 대신 `/permissions`로 안전한 커맨드만 사전 허용

Boris는 기본적으로 `--dangerously-skip-permissions`를 쓰지 않습니다. 대신 `/permissions`에서 안전하다고 확신하는 커맨드를 미리 허용해, 불필요한 프롬프트를 줄입니다. 설정은 `.claude/settings.json`에 담아 팀과 공유하기도 합니다.

![/permissions 예시](2026-01-04-image6.png)
_권한 프롬프트를 줄이기 위해 안전한 커맨드를 미리 허용하는 흐름_

- **핵심 요약**: 편의성과 안전성을 함께 잡으려면, 허용 범위를 좁게 잡아야 합니다.
- **바로 따라하기**:
  - `git status`, 테스트/린트 실행 등 “안전한 읽기/검증” 커맨드부터 허용합니다.
  - 허용 목록은 코드리뷰를 통해 관리합니다.
- **주의/트레이드오프**: 허용을 넓히는 순간 위험도 커집니다. 파괴적 명령(삭제/배포/비밀값 출력)은 항상 예외로 둡니다.

## 11. Claude Code가 내 도구를 대신 쓰게 한다(MCP로 Slack/Sentry/BigQuery 등)

Boris는 Claude Code가 “코딩만” 하지 않게 만듭니다. Slack에 검색/포스팅을 하거나, BigQuery 쿼리를 `bq` CLI로 돌리거나, Sentry에서 에러 로그를 가져오는 등 **팀이 쓰는 도구를 Claude가 대신 사용**하도록 구성합니다. 설정은 `.mcp.json` 같은 파일로 팀과 공유합니다.

- **핵심 요약**: Claude가 손발이 되려면, 코드 바깥의 도구까지 연결돼야 합니다.
- **바로 따라하기**:
  - 팀에서 공식적으로 쓰는 도구(로그/분석/티켓/메신저)를 먼저 연결합니다.
  - 민감정보/권한은 최소 권한 원칙으로 분리합니다.
- **주의/트레이드오프**: 외부 시스템 연동은 보안/감사/권한 관리가 핵심입니다. 팀 정책에 맞춰 운영해야 합니다.

## 12. 장기 작업은 background agent/Stop hook/플러그인으로 “끝까지” 굴린다

오래 걸리는 작업은 Claude가 끝나도 “확인”이 필요합니다. Boris는 작업 종료 시점에 background agent로 검증을 돌리거나, Stop hook으로 더 결정적으로 만들거나, 필요하면 `ralph-wiggum` 같은 플러그인을 사용하기도 합니다. 또한 샌드박스에서는 `--permission-mode=dontAsk`나 `--dangerously-skip-permissions`를 써서 세션이 막히지 않게 운영하기도 합니다.

- **핵심 요약**: 사람이 자리에 없을 때도 “완료 → 검증”까지 흘러가게 만들어야 합니다.
- **바로 따라하기**:
  - 작업 완료 후 자동 검증(테스트/리그레션 체크)을 워크플로우에 포함합니다.
  - 공격적인 권한 모드는 샌드박스/격리 환경에서만 사용합니다.
- **참고 링크**: [ralph-wiggum 플러그인](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-wiggum)
- **주의/트레이드오프**: 장기 작업 자동화는 실패 시 피해 범위가 커질 수 있습니다. 격리/롤백 전략을 같이 둬야 합니다.

## 13. 가장 중요한 팁: Claude에게 ‘검증 방법’을 제공하라(피드백 루프)

마지막 팁이자, Boris가 가장 강조하는 팁입니다.

> 결과를 좋게 만드는 가장 확실한 방법은 **Claude가 스스로 검증할 수 있게** 만드는 것이다.

Claude Code 팀은 변경을 랜딩하기 전에, Claude가 Chrome extension을 통해 브라우저를 열고 UI를 테스트하며, 실패하면 다시 고치고 반복하도록 운영합니다.

- **핵심 요약**: 피드백 루프가 있으면 결과 품질이 2~3배 좋아집니다.
- **바로 따라하기**:
  - 테스트 명령/검증 체크리스트/샘플 입력을 Claude에게 제공합니다.
  - “통과해야 하는 조건(성공 기준)”을 명시합니다.
- **참고 링크**: [Chrome extension](https://code.claude.com/docs/en/chrome)
- **주의/트레이드오프**: 검증이 없으면 Claude는 ‘그럴듯함’에서 멈춥니다. 작은 프로젝트일수록 더더욱 검증이 중요합니다.

---

## 🎯 내 워크플로우에 적용하기(추천 적용 순서)

처음부터 13개를 다 적용할 필요는 없습니다. 체감이 큰 순서로 추천하면:

1. **Plan mode + 성공 기준/테스트 포함한 계획**
2. **검증 루프(테스트/브라우저 체크리스트) 제공**
3. **팀 `CLAUDE.md` 운영(회귀 방지 규칙 축적)**
4. **slash command로 inner loop 자동화**
5. **sub-agent/hook로 ‘후처리’를 자동화**
6. (필요할 때) **MCP/권한 설정/플러그인으로 확장**

---

## 📚 참고 링크

- [Claude Code Docs](https://code.claude.com/docs/)
- [iTerm 2 system notifications](https://code.claude.com/docs/en/terminal-config#iterm-2-system-notifications)
- [Bash command execution](https://code.claude.com/docs/en/slash-commands#bash-command-execution)
- [Sub-agents](https://code.claude.com/docs/en/sub-agents)
- [Chrome extension](https://code.claude.com/docs/en/chrome)
- [ralph-wiggum 플러그인](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-wiggum)


