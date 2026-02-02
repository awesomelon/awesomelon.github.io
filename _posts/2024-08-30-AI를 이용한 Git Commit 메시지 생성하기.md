---
title: "AI를 이용한 Git Commit 메시지 생성하기"
date: 2024-08-30 14:58:00 +0900
categories: [ENGINEERING, PLAYGROUND]
tags: [ai, git, claude ai, cli, commit message, 자동화]
author: j-ho
img_path: /assets/img/for_post/
pin: false
description: Claude AI를 활용하여 Git 커밋 메시지를 자동으로 생성해주는 CLI 도구 commit-ai를 소개합니다.
---

`commit-ai`는 AI를 활용하여 Git 커밋 메시지를 자동으로 생성해주는 CLI 도구입니다. 일관성 있고 명확한 커밋 메시지를 쉽게 작성할 수 있으며, 개발자들이 더 중요한 작업에 집중할 수 있게 도와줘요.

![commit-ai 동작 예시](2024-08-30-example.gif)
_commit-ai를 사용한 커밋 메시지 자동 생성 과정_

---

## 개발 배경

Git을 사용하는 개발자라면 누구나 경험해 봤을 것입니다. 작업을 마치고 커밋을 하려는 순간, 적절한 커밋 메시지를 작성하는 데 시간을 허비하는 경우가 많습니다. 때로는 `fixed`, `feat` 같은 모호한 메시지로 마무리 짓기도 하죠.

Git 커밋 메시지는 단순한 기록이 아닙니다. 코드 변경의 목적과 내용을 명확히 전달하고, 팀원들과의 효과적인 의사소통 수단이 되며, 프로젝트 히스토리 추적과 디버깅을 지원합니다.

이러한 문제를 해결하고자 AI를 이용해 자동으로 명확하고 구체적인 커밋 메시지를 생성해주는 도구를 만들게 됐어요.

---

## 주요 기능

**AI 기반 다중 커밋 메시지 제안**: Anthropic의 Claude 3.5 모델을 이용해 고품질의 커밋 메시지를 생성해요. AI가 변경 사항을 분석하여 여러 가지 선택지를 제공합니다.

**Git 커밋 템플릿 지원**: 커밋 메시지를 일관되게 유지하기 위한 템플릿 기능을 지원해요.

**커스터마이즈 가능한 생성 옵션**: 최대 토큰 수, 온도(Temperature), 언어 설정 등을 조절할 수 있습니다.

**대화형 커밋 메시지 선택**: 화살표 키를 이용해 생성된 커밋 메시지 중 원하는 메시지를 선택하고, 필요 시 즉시 편집할 수 있습니다.

**스마트 파일 필터링**: 잠금 파일(package-lock.json 등), 대용량 파일(100KB 이상), 바이너리 파일을 자동으로 제외합니다.

---

## 프로젝트 구조

```text
commit-ai/
├── src/
│   ├── cli.ts                          # CLI 인터페이스
│   ├── GitCommitMessageGenerator.ts    # 핵심 로직
│   ├── commitMessageTemplate.ts        # 다국어 템플릿
│   └── utils/
│       ├── gitUtils.ts                 # Git 관련 유틸
│       └── configUtils.ts              # 설정 관리
```

주요 라이브러리로는 @anthropic-ai/sdk(AI API 연동), @inquirer/prompts(대화형 UI), commander(CLI 프레임워크), configstore(설정 관리), ora(로딩 스피너)를 사용합니다.

---

## 사용 방법

### 설치 및 초기 설정

```bash
# NPM을 통한 전역 설치
$ npm install -g @j-ho/commit-ai

# Anthropic API 키 설정
$ commit-ai --key YOUR_API_KEY

# (선택) 기본 언어 설정
$ commit-ai --language ko
```

Anthropic API 키는 [console.anthropic.com](https://console.anthropic.com)에서 발급받을 수 있습니다.

### 기본 사용법

```bash
# 1. 변경사항 스테이징
$ git add .

# 2. commit-ai 실행
$ commit-ai

# 3. 생성된 메시지 중 선택
# 4. (선택) 메시지 편집
# 5. 커밋 완료!
```

### 인터랙티브 워크플로우

```text
$ commit-ai

⠹ Generating commit messages...
✔ Messages generated!

? Select a commit message to use
  ❯ feat: Add user authentication
    feat: Implement login functionality
    feat: Create authentication system
    ✏️  Edit commit message
    🌟 Cancel
```

---

## 기술적 도전과 해결 방안

### 대용량 파일 처리

Git diff에 대용량 파일이 포함될 경우 AI 모델의 토큰 제한을 초과할 수 있습니다. 100KB 이상의 파일은 필터링하여 파일명만 포함하도록 했어요.

### 커밋 템플릿 지원

팀마다 다른 커밋 메시지 형식을 사용합니다. Git 설정에서 템플릿 경로를 읽어와 AI 프롬프트에 반영하도록 했습니다.

### AI 응답 파싱

Claude AI의 응답 형식이 항상 일정하지 않을 수 있습니다. Markdown JSON 블록, Raw JSON, 텍스트 파싱 순으로 다층 파싱 로직을 구현하여 안정성을 확보했어요.

---

## 향후 계획

- 다른 AI 모델 지원 (GPT-4, Gemini 등)
- Conventional Commits 자동 검증
- Git hooks 통합
- VS Code 확장

---

## 참고 자료

- [GitHub - commit-ai 소스 코드](https://github.com/awesomelon/commitAI)
- [NPM - @j-ho/commit-ai](https://www.npmjs.com/package/@j-ho/commit-ai)
- [Anthropic Claude API Documentation](https://docs.anthropic.com)
- [Conventional Commits](https://www.conventionalcommits.org)
