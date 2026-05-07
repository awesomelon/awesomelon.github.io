---
title: "AI를 이용한 Git Commit 메시지 생성하기"
date: 2024-08-30 14:58:00 +0900
categories: [ENGINEERING, PLAYGROUND]
tags: [ai, git, claude ai, cli, commit message, 자동화]
author: j-ho
img_path: /assets/img/for_post/
pin: false
description: Claude AI로 Git 커밋 메시지를 생성하는 CLI 도구 commit-ai를 소개합니다.
---

`commit-ai`는 AI로 Git 커밋 메시지를 자동 생성해주는 CLI 도구입니다. 커밋 메시지 고민하는 시간을 줄여줘요.

![commit-ai 동작 예시](2024-08-30-example.gif)
_commit-ai를 사용한 커밋 메시지 자동 생성 과정_

---

## 개발 배경

Git 쓰는 개발자라면 다들 겪어봤을 겁니다. 작업 끝나고 커밋하려는데 메시지 쓰는 게 은근히 귀찮은 거죠. 결국 `fixed`, `feat` 같은 대충 쓴 메시지로 끝내기도 하고요.

커밋 메시지는 코드 변경의 목적을 전달하고, 팀원과 소통하고, 나중에 히스토리를 추적할 때 쓰이는 건데, 매번 잘 쓰기가 쉽지 않습니다.

그래서 AI가 diff를 보고 커밋 메시지를 만들어주면 어떨까 싶어서 도구를 만들게 됐어요.

---

## 주요 기능

**AI 기반 다중 커밋 메시지 제안**: Anthropic의 Claude 3.5 모델로 커밋 메시지를 생성합니다. 변경 사항을 분석해서 여러 선택지를 보여줘요.

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

Git diff에 큰 파일이 포함되면 AI 모델의 토큰 제한을 넘길 수 있습니다. 100KB 이상 파일은 빼고 파일명만 넘기도록 했어요.

### 커밋 템플릿 지원

팀마다 커밋 메시지 형식이 다릅니다. Git 설정에서 템플릿 경로를 읽어와 AI 프롬프트에 반영하도록 했습니다.

### AI 응답 파싱

Claude AI의 응답 형식이 매번 같지는 않습니다. Markdown JSON 블록, Raw JSON, 텍스트 파싱 순서로 시도하는 다층 파싱 로직을 넣어서 안정성을 높였어요.

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
