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

> **📌 KEYWORDS**  
> `AI` `Git` `Claude AI` `CLI` `자동화` `커밋 메시지`
{: .prompt-info }

---

## 🚀 들어가며

오늘은 제가 개발한 `commit-ai`라는 도구에 대해 소개하고자 합니다.

`commit-ai`는 **AI를 활용하여 Git 커밋 메시지를 자동으로 생성**해주는 CLI 도구입니다. 이 도구를 통해 일관성 있고 명확한 커밋 메시지를 쉽게 작성할 수 있으며, 개발자들이 불필요하게 시간을 낭비하지 않고 더 중요한 작업에 집중할 수 있게 도와줍니다.

![commit-ai 동작 예시](2024-08-30-example.gif)
_commit-ai를 사용한 커밋 메시지 자동 생성 과정_

---

## 💡 개발 배경

Git을 사용하는 개발자라면 누구나 경험해 봤을 것입니다.

작업을 마치고 커밋을 하려는 순간, **적절한 커밋 메시지를 작성하는 데 시간을 허비**하는 경우가 많습니다. 때로는 `fixed`, `feat` 같은 모호한 메시지로 마무리 짓기도 하죠.

### 왜 커밋 메시지가 중요한가?

Git 커밋 메시지는 단순한 기록이 아닙니다:

| 역할 | 설명 |
|:---|:---|
| 📝 **변경 사항 요약** | 코드 변경의 목적과 내용을 명확히 전달 |
| 💬 **팀 커뮤니케이션** | 팀원들과의 효과적인 의사소통 수단 |
| 🔍 **유지보수성 향상** | 프로젝트 히스토리 추적과 디버깅 지원 |
| 📊 **프로젝트 문서화** | 자동 changelog 생성의 기반 |

> **⚠️ 현실의 문제**  
> 바쁜 일정이나 많은 코드 변경 후에 적절한 커밋 메시지를 작성하는 것이 쉽지 않을 때가 많습니다.
{: .prompt-warning }

### commit-ai의 솔루션

이러한 문제를 해결하고자 AI를 이용해 **자동으로 명확하고 구체적인 커밋 메시지**를 생성해주는 도구를 만들게 되었습니다.

이 도구를 사용하면:
- 매번 커밋 메시지를 고민하지 않아도 됨
- 일관된 형식을 유지할 수 있음
- 코드베이스의 가독성과 협업 효율 향상

---

## ✨ 주요 기능

commit-ai는 다음과 같은 핵심 기능을 제공합니다:

### 1. AI 기반 다중 커밋 메시지 제안

**Anthropic의 Claude 3.5** 모델을 이용해 고품질의 커밋 메시지를 생성합니다.

> **🤖 AI의 힘**  
> AI가 변경 사항을 분석하여 여러 가지 선택지를 제공하고, 그중 가장 적합한 메시지를 선택할 수 있도록 돕습니다.
{: .prompt-tip }

### 2. Git 커밋 템플릿 지원

커밋 메시지를 일관되게 유지하기 위한 템플릿 기능을 지원합니다.

### 3. 커스터마이즈 가능한 생성 옵션

| 옵션 | 설명 |
|:---|:---|
| **최대 토큰 수** | 생성되는 메시지의 길이 조절 |
| **온도(Temperature)** | 메시지의 창의성 수준 조정 |
| **언어 설정** | 다국어 커밋 메시지 생성 |

### 4. 사용하기 쉬운 CLI

명령줄에서 간편하게 커밋 메시지를 생성하고 선택할 수 있습니다.

> **🎯 직관적 인터페이스**  
> 복잡한 설정 없이 바로 도구를 활용할 수 있습니다.
{: .prompt-info }

### 5. 대화형 커밋 메시지 선택

화살표 키를 이용해 생성된 커밋 메시지 중 원하는 메시지를 선택할 수 있습니다.

- 여러 제안 중 최적의 메시지 선택
- 필요 시 즉시 편집 가능
- 제목과 본문 개별 수정 지원

### 6. 스마트 파일 필터링

| 제외 대상 | 이유 |
|:---|:---|
| 🔒 **잠금 파일** | package-lock.json, yarn.lock 등 |
| 📦 **대용량 파일** | 100KB 이상 파일 (설정 가능) |
| 🗂️ **바이너리 파일** | 이미지, 폰트 등 |

> **⚡ 성능 최적화**  
> 불필요한 파일을 자동으로 제외하여 AI 모델의 효율성을 높였습니다.
{: .prompt-tip }

---

## 🏗️ 구현 과정

### 프로젝트 구조 설계

각 기능을 모듈화하여 유지보수성과 확장성을 높였습니다.
```text
commit-ai/
├── src/
│   ├── cli.ts                          # CLI 인터페이스
│   ├── GitCommitMessageGenerator.ts    # 핵심 로직
│   ├── commitMessageTemplate.ts        # 다국어 템플릿
│   └── utils/
│       ├── gitUtils.ts                 # Git 관련 유틸
│       └── configUtils.ts              # 설정 관리
├── package.json
└── tsconfig.json
```
{: .nolineno }

#### 주요 모듈 설명

| 모듈 | 역할 |
|:---|:---|
| **cli.ts** | 명령줄 인터페이스 구현, 사용자 입력 처리 |
| **GitCommitMessageGenerator.ts** | AI 호출 및 커밋 메시지 생성 로직 |
| **commitMessageTemplate.ts** | 다국어 지원을 위한 템플릿 제공 |

---

### 기술 스택

commit-ai는 다음 라이브러리들을 활용합니다:
```typescript
// package.json 주요 dependencies
{
  "@anthropic-ai/sdk": "^0.x.x",      // AI API 연동
  "@inquirer/prompts": "^5.x.x",      // 대화형 UI
  "commander": "^12.x.x",             // CLI 프레임워크
  "configstore": "^7.x.x",            // 설정 관리
  "ora": "^8.x.x"                     // 로딩 스피너
}
```
{: file='package.json' .nolineno }

| 라이브러리 | 용도 |
|:---|:---|
| **@anthropic-ai/sdk** | Claude AI API 통신 |
| **@inquirer/prompts** | 인터랙티브한 사용자 입력 처리 |
| **commander** | CLI 명령어 및 옵션 정의 |
| **configstore** | 사용자 설정 영구 저장 |
| **ora** | 시각적 피드백(로딩 스피너) |

---

### 커밋 메시지 생성 로직

`GitCommitMessageGenerator` 클래스의 핵심 워크플로우:

#### 1. Git Diff 분석
```typescript
async analyzeDiff(): Promise<string> {
  // 스테이징된 변경사항 가져오기
  const diff = execSync('git diff --cached', { 
    encoding: 'utf-8' 
  });
  
  // 대용량 파일 필터링
  const filteredDiff = this.filterLargeFiles(diff);
  
  return filteredDiff;
}
```
{: file='GitCommitMessageGenerator.ts' .nolineno }

#### 2. AI 호출
```typescript
async generateMessages(diff: string): Promise<CommitMessage[]> {
  const response = await this.anthropic.messages.create({
    model: 'claude-3-5-sonnet-20241022',
    max_tokens: this.maxTokens,
    temperature: this.temperature,
    messages: [{
      role: 'user',
      content: this.buildPrompt(diff)
    }]
  });
  
  return this.parseResponse(response);
}
```
{: file='GitCommitMessageGenerator.ts' .nolineno }

#### 3. 응답 파싱
```typescript
parseResponse(response: Message): CommitMessage[] {
  const content = response.content[0].text;
  
  // JSON 형식 추출
  const jsonMatch = content.match(/```json\n([\s\S]*?)\n```/);
  if (!jsonMatch) {
    throw new Error('Invalid response format');
  }
  
  const messages = JSON.parse(jsonMatch[1]);
  return messages.map(msg => ({
    title: msg.title,
    body: msg.body || ''
  }));
}
```
{: file='GitCommitMessageGenerator.ts' .nolineno }

> **🔄 유연한 설계**  
> 온도(temperature) 값을 조정하여 메시지의 창의성을 높이거나 낮출 수 있습니다.
{: .prompt-info }

---

### 사용자 경험 최적화

**ora**와 **@inquirer/prompts**를 활용한 인터랙티브 UI 구현:
```typescript
import ora from 'ora';
import { select, confirm, input } from '@inquirer/prompts';

async function selectCommitMessage(messages: CommitMessage[]) {
  const spinner = ora('Generating commit messages...').start();
  
  try {
    const generated = await generateMessages();
    spinner.succeed('Messages generated!');
    
    const choices = generated.map((msg, idx) => ({
      name: msg.title,
      value: idx
    }));
    
    const selected = await select({
      message: 'Select a commit message',
      choices: [
        ...choices,
        { name: '✏️  Edit commit message', value: -1 },
        { name: '🌟 Cancel', value: -2 }
      ]
    });
    
    if (selected >= 0) {
      return await editMessageIfNeeded(generated[selected]);
    }
  } catch (error) {
    spinner.fail('Failed to generate messages');
    throw error;
  }
}
```
{: file='cli.ts' }

#### UX 개선 포인트

| 기능 | 효과 |
|:---|:---|
| 🔄 **로딩 스피너** | AI 처리 중 시각적 피드백 제공 |
| ⌨️ **화살표 키 네비게이션** | 직관적인 메시지 선택 |
| ✏️ **즉시 편집** | 생성된 메시지 커스터마이징 |
| 💾 **설정 저장** | API 키, 언어 등 재사용 |

---

## 📖 사용 방법

### 설치 및 초기 설정
```bash
# NPM을 통한 전역 설치
$ npm install -g @j-ho/commit-ai

# Anthropic API 키 설정
$ commit-ai --key YOUR_API_KEY

# (선택) 기본 언어 설정
$ commit-ai --language ko
```

> **🔑 API 키 발급**  
> Anthropic API 키는 [console.anthropic.com](https://console.anthropic.com)에서 발급받을 수 있습니다.
{: .prompt-info }

---

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

---

### 고급 옵션

#### API 키 및 언어 설정
```bash
# 동시 설정
$ commit-ai --key YOUR_API_KEY --language ko

# 개별 설정
$ commit-ai --key YOUR_API_KEY
$ commit-ai --language ja

# 현재 설정 확인
$ commit-ai --show-config
```

#### 일회성 언어 변경
```bash
# 한 번만 한국어로 생성
$ commit-ai -l ko

# 한 번만 일본어로 생성
$ commit-ai -l ja
```

---

### 인터랙티브 워크플로우

실제 사용 시 다음과 같은 순서로 진행됩니다:
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

# 메시지 선택 후
? Would you like to edit the commit title? (y/N) y
✏️  Enter new title: feat: Implement secure user authentication

? Would you like to edit the commit body? (y/N) y
✏️  Enter commit body:
Add JWT-based authentication system
- Implement login endpoint
- Add password hashing with bcrypt
- Create authentication middleware

✔ Commit created successfully!
```
{: .nolineno }

---

## 🔧 기술적 도전과 해결 방안

### 1. 대용량 파일 처리

#### 문제

Git diff에 대용량 파일이 포함될 경우 AI 모델의 **토큰 제한**을 초과할 수 있습니다.

#### 해결책
```typescript
const MAX_FILE_SIZE = 100 * 1024; // 100KB

function filterLargeFiles(diff: string): string {
  const files = diff.split('diff --git');
  
  return files
    .filter(file => {
      const size = Buffer.byteLength(file, 'utf8');
      return size < MAX_FILE_SIZE;
    })
    .join('diff --git');
}
```
{: file='GitCommitMessageGenerator.ts' .nolineno }

| 파일 크기 | 처리 방식 |
|:---|:---|
| < 100KB | ✅ 전체 포함 |
| ≥ 100KB | ⚠️ 파일명만 포함 |

> **⚡ 성능 최적화**  
> 불필요한 리소스 소비를 줄이고 AI의 성능을 최적화합니다.
{: .prompt-tip }

---

### 2. 커밋 템플릿 지원

#### 문제

팀마다 다른 커밋 메시지 형식을 사용합니다.

#### 해결책
```typescript
function getCommitTemplate(): string | null {
  try {
    // Git 설정에서 템플릿 경로 읽기
    const templatePath = execSync(
      'git config --get commit.template',
      { encoding: 'utf-8' }
    ).trim();
    
    if (templatePath) {
      // 템플릿 파일 읽기
      return fs.readFileSync(
        path.resolve(templatePath),
        'utf-8'
      );
    }
  } catch (error) {
    // 템플릿이 설정되지 않은 경우
    return null;
  }
  
  return null;
}
```
{: file='gitUtils.ts' }

> **🎯 일관성 유지**  
> 팀 내에서 합의된 커밋 메시지 형식을 쉽게 유지할 수 있습니다.
{: .prompt-info }

---

### 3. AI 응답 파싱

#### 문제

Claude AI의 응답 형식이 항상 일정하지 않을 수 있습니다.

#### 해결책
```typescript
function parseAIResponse(response: string): CommitMessage[] {
  // 1. JSON 블록 추출 시도
  let jsonMatch = response.match(/```json\n([\s\S]*?)\n```/);
  
  if (!jsonMatch) {
    // 2. 백틱 없는 JSON 추출 시도
    jsonMatch = response.match(/\[[\s\S]*\]/);
  }
  
  if (!jsonMatch) {
    // 3. 폴백: 텍스트 파싱
    return parseTextResponse(response);
  }
  
  try {
    return JSON.parse(jsonMatch[1] || jsonMatch[0]);
  } catch (error) {
    throw new Error('Failed to parse AI response');
  }
}
```
{: file='GitCommitMessageGenerator.ts' }

| 단계 | 시도하는 형식 | 성공률 |
|:---:|:---|:---:|
| 1 | Markdown JSON 블록 | ~95% |
| 2 | Raw JSON | ~4% |
| 3 | 텍스트 파싱 | ~1% |

> **🛡️ 안정성 확보**  
> 다양한 상황에서도 안정적으로 동작하도록 다층 파싱 로직을 구현했습니다.
{: .prompt-tip }

---

## 💡 개선 사항 및 향후 계획

### 현재 제공 기능

| 기능 | 상태 |
|:---|:---:|
| Claude AI 통합 | ✅ |
| 다국어 지원 | ✅ |
| 커밋 템플릿 | ✅ |
| 대화형 UI | ✅ |
| 설정 관리 | ✅ |

### 향후 계획
```text
📋 로드맵
├── v2.0
│   ├── 다른 AI 모델 지원 (GPT-4, Gemini 등)
│   ├── Conventional Commits 자동 검증
│   └── 커밋 히스토리 기반 학습
├── v2.1
│   ├── Git hooks 통합
│   ├── PR 템플릿 생성
│   └── 팀 설정 공유 기능
└── v3.0
    ├── VS Code 확장
    ├── 웹 인터페이스
    └── 커밋 품질 분석 대시보드
```
{: .nolineno }

> **🔄 지속적 개선**  
> 사용자 피드백을 반영하여 지속적으로 개선해 나갈 예정입니다.
{: .prompt-info }

---

## 🎓 마무리

`commit-ai`는 개발자들이 **커밋 메시지 작성에 드는 시간을 줄이고**, **일관성 있는 메시지**를 작성하는 데 도움을 주기 위해 만들어졌습니다.

### 핵심 가치

| 가치 | 효과 |
|:---|:---|
| ⏱️ **시간 절약** | 메시지 고민 시간 최소화 |
| 📝 **품질 향상** | AI 기반 명확한 메시지 |
| 🔄 **일관성** | 통일된 커밋 형식 유지 |
| 🤝 **협업 효율** | 팀 커뮤니케이션 개선 |

AI를 통해 커밋 메시지의 품질을 높이고, 개발 프로세스에서 발생하는 반복적인 작업을 자동화하여 **개발자들이 더 창의적이고 중요한 작업에 집중**할 수 있게 합니다.

> **🚀 함께 만들어가는 도구**  
> 이 도구가 여러분의 개발 워크플로우에 실질적인 도움이 되길 바랍니다. `commit-ai`와 함께 더 효율적인 개발을 경험해 보세요!
{: .prompt-tip }

---

## 📚 참고 자료

- [GitHub - commit-ai 소스 코드](https://github.com/awesomelon/commitAI)
- [NPM - @j-ho/commit-ai](https://www.npmjs.com/package/@j-ho/commit-ai)
- [Anthropic Claude API Documentation](https://docs.anthropic.com)
- [Conventional Commits](https://www.conventionalcommits.org)