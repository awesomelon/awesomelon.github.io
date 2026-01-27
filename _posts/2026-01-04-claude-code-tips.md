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

> 이 글은 Claude Code 제작자 Boris Cherny가 공유한 사용 팁을 바탕으로 작성했습니다.
{: .prompt-info }

---

Claude Code를 쓰다 보면 결국 이런 질문으로 돌아옵니다. "잘 쓰는 사람은 대체 어떻게 쓰지?"

재미있는 건, Boris의 셋업이 의외로 바닐라에 가깝다는 점입니다. 기본이 이미 좋아서, 그는 과도한 커스터마이징보다는 반복 루프를 자동화하고 검증을 붙이는 데 에너지를 씁니다.

이 글의 핵심 메시지는 두 가지입니다.
- 정답은 없다. 팀과 개인의 워크플로우에 맞게 커스터마이즈하라.
- 단, 검증 루프를 만들면 결과물이 2~3배 좋아진다.

## 한 장 요약

1. 병렬 세션: 터미널/웹에서 여러 Claude를 동시에 돌리고 알림으로 회수
2. Plan mode: PR 목표라면 계획을 먼저 다듬고, 실행은 1-shot을 노림
3. CLAUDE.md 운영: 자주 틀리는 것을 팀 규칙으로 박제
4. Slash command/Sub-agent/Hooks: 반복 작업을 자동화
5. Permissions/MCP: 권한과 외부 도구 연동을 팀 설정으로 관리
6. 검증 루프 제공: 테스트/브라우저 검증을 Claude에게 줌

---

## 1. 터미널에서 5개 세션 병렬 + 알림으로 회수

Boris는 터미널에서 5개의 Claude 세션을 동시에 돌리고, 탭을 1~5로 번호 붙여 관리합니다. 핵심은 기다리지 말고 알림으로 회수하는 것입니다.

탭마다 역할(리뷰/리팩터/테스트/문서)을 정해두고, iTerm2의 시스템 알림을 켜서 입력이 필요할 때 놓치지 않게 합니다. 다만 세션이 늘수록 문맥 스위칭 비용도 늘어납니다. "항상 5개"보다 "필요할 때만 5개"가 현실적일 때도 많습니다.

참고: [iTerm 2 system notifications](https://code.claude.com/docs/en/terminal-config#iterm-2-system-notifications)

## 2. 웹에서도 5~10개 병렬 + teleport/모바일

터미널만이 아닙니다. Boris는 `claude.ai/code`에서도 5~10개 세션을 병렬로 운영합니다. 로컬 세션을 웹으로 넘기거나(`&`), `--teleport`로 오가고, 아침마다 모바일에서 몇 개 세션을 시작해두고 나중에 확인하기도 합니다.

![claude.ai/code 병렬 세션](2026-01-04-image1.png)
_웹에서 여러 세션을 병렬로 운영하는 예시_

성격이 다른 작업(리서치/코딩/검증/문서화)을 세션 단위로 분리하고, 첫 메시지에 목표와 완료 조건을 적어두면 나중에 다시 들어갔을 때 시간을 아낄 수 있습니다. 세션 수가 늘면 관리 비용도 생기니, 세션을 늘리는 것 자체가 목적이 되지 않게 주의하세요.

## 3. Opus 4.5 + thinking을 기본값으로

Boris는 Opus 4.5 + thinking을 거의 모든 작업의 기본값으로 씁니다. Sonnet보다 느릴 수 있지만, 덜 조종해도 되고 tool use가 안정적이라 결국 전체 속도가 더 빠른 경우가 많다는 이유입니다.

모델은 단일 응답 속도가 아니라 완료까지의 왕복 횟수로 평가해야 합니다. 복잡한 작업은 큰 모델이 유리하고, 단순 생성/요약은 작은 모델이 합리적입니다. 팀 예산이 제한적이면 "기본은 가볍게, 중요한 구간만 상향" 전략이 현실적입니다.

## 4. CLAUDE.md를 git에 체크인하고 계속 업데이트

Claude Code 팀은 레포에 공용 CLAUDE.md를 두고 팀원들이 자주 업데이트합니다. Claude가 뭔가를 잘못하면 그 내용을 추가해서 다음번엔 같은 실수를 줄이는 방식입니다.

![팀 공용 CLAUDE.md 예시](2026-01-04-image2.png)
_git에 체크인해서 팀이 함께 유지보수하는 CLAUDE.md_

프롬프트는 한 번 잘 쓰는 문장이 아니라 팀이 유지보수하는 규칙 집합입니다. "절대 하면 안 되는 것"과 "PR 전에 반드시 해야 하는 것"을 먼저 고정하고, Claude가 반복적으로 틀리는 패턴이 보이면 즉시 추가합니다. 단, CLAUDE.md가 너무 길어지면 비용이 올라가니 회귀 위험이 큰 것 위주로 유지하세요.

참고: [Claude Code Docs](https://code.claude.com/docs/)

## 5. 코드리뷰에서 CLAUDE.md 업데이트를 PR에 포함

Boris는 코드리뷰 중에 동료 PR에 @.claude를 태그해, 이번에 배운 규칙을 CLAUDE.md에 반영하자고 요청합니다. Claude Code GitHub action을 사용해서요.

![PR 코멘트로 CLAUDE.md 업데이트 요청](2026-01-04-image3.png)
_코드리뷰 중 규칙 업데이트를 PR에 포함시키는 예시_

개인의 배움을 팀 규칙으로 승격시키면 누적 효과가 생깁니다. 리뷰에서 "다음에도 틀릴 것 같다" 싶은 포인트가 보이면 즉시 규칙 업데이트를 함께 요청하세요. 규칙은 늘릴수록 생산성을 갉아먹을 수 있으니, 언제 규칙으로 올릴지 팀 기준이 필요합니다.

## 6. 대부분의 세션은 Plan mode로 시작

Boris는 대부분의 세션을 Plan mode로 시작합니다(`shift+tab` 두 번). 목표가 PR이라면 계획을 다듬고, 만족스러우면 auto-accept edits 모드로 전환해 구현을 1-shot에 가깝게 시도합니다.

![Plan mode on](2026-01-04-image4.png)
_Plan mode에서 계획을 확정한 뒤 실행으로 넘어가기_

좋은 계획이 있으면 구현은 빨라지고 리뷰/회귀 위험은 줄어듭니다. 계획에 변경 범위, 리스크, 테스트 전략, 롤백이 포함됐는지 확인하세요. 계획이 마음에 들 때까지 질문으로 다듬고, 그 다음 실행으로 넘어갑니다. 계획을 길게 쓰는 게 목적이 아니라, 실행 가능한 체크리스트 정도가 가장 효율적입니다.

## 7. 매일 반복하는 작업은 slash command로

하루에 여러 번 하는 작업은 slash command로 표준화합니다. 커맨드는 `.claude/commands/`에 두고 git에 체크인해 팀이 공유합니다. `/commit-push-pr` 같은 커맨드는 인라인 bash로 `git status`를 미리 계산해 모델과의 왕복을 줄입니다.

내 inner loop(커밋/푸시/PR/리포맷/테스트)를 나열하고, 빈도가 높은 1~2개부터 slash command로 고정하세요. 인라인 bash는 편하지만 환경 의존이 커질 수 있으니, 팀 공유 커맨드는 최소한의 가정 위에서 설계하는 게 좋습니다.

참고: [Bash command execution](https://code.claude.com/docs/en/slash-commands#bash-command-execution)

## 8. 서브에이전트로 공통 PR 워크플로우 자동화

Boris는 `code-simplifier`, `verify-app` 같은 서브에이전트를 정기적으로 사용합니다. slash command가 작은 명령이라면, sub-agent는 반복되는 워크플로우 전체를 자동화하는 개념입니다.

PR마다 반복되는 후처리(정리/단순화/검증/문서)를 sub-agent로 분리하고, 지시문에는 입력/출력/검증 기준을 명확히 적습니다. 에이전트가 많아질수록 관리 비용이 생기니, 자주 쓰는 것 위주로 제한하세요.

참고: [Sub-agents](https://code.claude.com/docs/en/sub-agents)

## 9. PostToolUse hook으로 포맷팅 자동화

Claude가 보통은 포맷을 잘 맞추지만, CI에서 마지막 10%가 터지는 순간이 있습니다. Boris 팀은 PostToolUse hook으로 포맷팅을 자동 적용해 CI 실패를 줄입니다.

![PostToolUse hook 예시](2026-01-04-image5.png)
_tool use 이후 포맷을 자동으로 맞추는 hook_

프로젝트에 맞는 포맷터(prettier/rubocop/black 등)를 훅에서 실행합니다. 훅이 실패해도 진행을 막지 않도록(`|| true`) 설계하되, CI에서는 잡히게 만드는 전략도 있습니다. 자동 수정은 왜 바뀌었는지 안 보일 수 있으니 팀이 훅 동작을 이해하도록 문서화하세요.

## 10. `/permissions`로 안전한 커맨드만 사전 허용

Boris는 `--dangerously-skip-permissions`를 쓰지 않습니다. 대신 `/permissions`에서 안전하다고 확신하는 커맨드를 미리 허용해 불필요한 프롬프트를 줄입니다. 설정은 `.claude/settings.json`에 담아 팀과 공유합니다.

![/permissions 예시](2026-01-04-image6.png)
_안전한 커맨드를 미리 허용하는 흐름_

`git status`, 테스트/린트 실행 등 안전한 읽기/검증 커맨드부터 허용하고, 허용 목록은 코드리뷰를 통해 관리합니다. 허용을 넓히는 순간 위험도 커지니, 파괴적 명령(삭제/배포/비밀값 출력)은 항상 예외로 두세요.

## 11. MCP로 Slack/Sentry/BigQuery 연동

Boris는 Claude Code가 코딩만 하지 않게 만듭니다. Slack 검색/포스팅, BigQuery 쿼리, Sentry 에러 로그 가져오기 등 팀이 쓰는 도구를 Claude가 대신 사용하도록 구성합니다. 설정은 `.mcp.json`으로 팀과 공유합니다.

팀에서 공식적으로 쓰는 도구(로그/분석/티켓/메신저)를 먼저 연결하고, 민감정보와 권한은 최소 권한 원칙으로 분리합니다. 외부 시스템 연동은 보안/감사/권한 관리가 핵심이니 팀 정책에 맞춰 운영하세요.

## 12. 장기 작업은 background agent로 끝까지

오래 걸리는 작업은 Claude가 끝나도 확인이 필요합니다. Boris는 작업 종료 시점에 background agent로 검증을 돌리거나, Stop hook으로 더 결정적으로 만들거나, `ralph-wiggum` 같은 플러그인을 사용합니다. 샌드박스에서는 `--permission-mode=dontAsk`로 세션이 막히지 않게 운영하기도 합니다.

사람이 자리에 없을 때도 완료에서 검증까지 흘러가게 만들어야 합니다. 작업 완료 후 자동 검증을 워크플로우에 포함하고, 공격적인 권한 모드는 샌드박스/격리 환경에서만 사용하세요. 장기 작업 자동화는 실패 시 피해 범위가 클 수 있으니 격리/롤백 전략을 같이 두세요.

참고: [ralph-wiggum 플러그인](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-wiggum)

## 13. Claude에게 검증 방법을 제공하라

마지막이자 Boris가 가장 강조하는 팁입니다.

> 결과를 좋게 만드는 가장 확실한 방법은 Claude가 스스로 검증할 수 있게 만드는 것이다.

Claude Code 팀은 변경을 랜딩하기 전에 Claude가 Chrome extension으로 브라우저를 열고 UI를 테스트하며, 실패하면 다시 고치고 반복하도록 운영합니다.

테스트 명령, 검증 체크리스트, 샘플 입력을 Claude에게 제공하고, 통과해야 하는 조건을 명시하세요. 검증이 없으면 Claude는 그럴듯함에서 멈춥니다. 작은 프로젝트일수록 검증이 더 중요합니다.

참고: [Chrome extension](https://code.claude.com/docs/en/chrome)

---

## 추천 적용 순서

처음부터 13개를 다 적용할 필요는 없습니다. 체감이 큰 순서로:

1. Plan mode + 성공 기준/테스트 포함한 계획
2. 검증 루프(테스트/브라우저 체크리스트) 제공
3. 팀 CLAUDE.md 운영
4. slash command로 inner loop 자동화
5. sub-agent/hook로 후처리 자동화
6. 필요할 때 MCP/권한 설정/플러그인으로 확장

---

## 참고 링크

- [Claude Code Docs](https://code.claude.com/docs/)
- [iTerm 2 system notifications](https://code.claude.com/docs/en/terminal-config#iterm-2-system-notifications)
- [Bash command execution](https://code.claude.com/docs/en/slash-commands#bash-command-execution)
- [Sub-agents](https://code.claude.com/docs/en/sub-agents)
- [Chrome extension](https://code.claude.com/docs/en/chrome)
- [ralph-wiggum 플러그인](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-wiggum)
