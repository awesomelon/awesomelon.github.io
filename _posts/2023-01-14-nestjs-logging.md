---
title: NestJS 로깅 도입하기 (winston)
date: 2023-01-14 15:00:00 +0900
categories: [ENGINEERING, BACKEND, NestJS]
tags: [nestjs, logging, winston]
author: j-ho
img_path: /assets/img/for_post/
description: Winston을 NestJS에 주입하고 요청 ID·상태·지연·중단을 구조화해 기록하며 파일 회전과 보관 정책을 정리합니다.
last_modified_at: 2026-09-12 13:38:07 +0900
---

![Winston을 이용한 NestJS 로깅 소개](2023-01-14-image1.png)

웹 API 서버의 로그는 문제가 생겼을 때 무슨 요청이 어떻게 끝났는지 찾기 위한 기록입니다. 요청 URL만 남기면 호출은 알 수 있지만, 성공했는지 얼마나 걸렸는지는 알기 어렵습니다.

NestJS에 Winston을 연결하고 **요청 ID·상태 코드·처리 시간**을 구조화해서 남기는 방법을 정리해보겠습니다. 로거를 한 번 생성해 재사용하고, 파일이 계속 커지는 문제도 함께 다룹니다.

> 2023년 글을 보완했습니다. 원래 날짜 문자열로 파일명을 만들던 예제를, Nest의 의존성 주입과 크기·개수 제한을 사용하는 구성으로 바꿨습니다. 코드는 Express 어댑터와 `winston`·`nest-winston`을 사용하는 NestJS 애플리케이션을 가정합니다.

## 요청 시작보다 완료 시점이 필요한 이유

미들웨어는 요청 처리 앞부분에서 실행되므로 request·response를 보고 다음 단계로 넘길 수 있습니다. 응답을 직접 끝내지 않는다면 `next()`를 호출해야 다음 처리로 진행합니다. [NestJS 미들웨어 문서](https://docs.nestjs.com/middleware)는 어댑터별 차이와 등록 방법을 설명합니다.

![미들웨어와 요청 처리 단계의 관계](2023-01-14-image2.png)

요청 시작 때 로그를 남기면 최종 상태 코드는 아직 모릅니다. 아래 예제는 응답의 `finish` 이벤트에서 기록하고, 완료 전에 연결이 닫힌 경우는 `aborted`로 구분합니다.

단, `finish`는 Node.js가 응답 데이터를 전송 계층에 넘겼다는 의미입니다. 사용자의 브라우저가 모두 받았거나 화면까지 표시했다는 확인은 아닙니다. [Node.js HTTP 응답 이벤트](https://nodejs.org/api/http.html#event-finish)의 의미에 맞게 지표를 해석해야 합니다.

## Winston을 한 번 설정한다

```bash
npm install winston nest-winston
```

날짜를 파일명에 넣기 위한 `moment`는 이 구성에 필요하지 않습니다. 설치 버전과 lockfile은 프로젝트에서 관리합니다.

다음은 로거 설정을 분리한 파일입니다. 애플리케이션 로그는 info 이상, 오류 파일은 error만 기록합니다. 콘솔은 `LOG_LEVEL`에 따라 상세도를 바꿀 수 있게 했습니다.

```typescript
// logging.options.ts
import { format, transports } from 'winston';

export const loggingOptions = {
  level: process.env.LOG_LEVEL ?? 'info',
  defaultMeta: { service: 'api' },
  format: format.combine(
    format.errors({ stack: true }),
    format.timestamp(),
    format.json(),
  ),
  transports: [
    new transports.Console(),
    new transports.File({
      level: 'info',
      filename: 'logs/application.log',
      maxsize: 5_000_000,
      maxFiles: 7,
    }),
    new transports.File({
      level: 'error',
      filename: 'logs/error.log',
      maxsize: 5_000_000,
      maxFiles: 7,
    }),
  ],
};
```

Winston 기본 레벨에서 `info`를 지정하면 `warn`, `error`도 포함됩니다. 따라서 오류는 application과 error 파일 양쪽에 남습니다. 별도 오류 파일이 필요 없다면 해당 transport를 제거하면 됩니다. 레벨명은 `warning`이 아니라 `warn`입니다. [Winston의 레벨·format·transport 문서](https://github.com/winstonjs/winston)에 이 관계가 정리돼 있습니다.

문자열을 합쳐 한 줄로 만드는 대신 JSON 필드로 남기면 `statusCode >= 500`, 특정 `requestId` 같은 조건으로 검색할 수 있습니다. JSON으로 포맷했다고 민감한 데이터가 자동으로 지워지는 것은 아니니 기록할 필드부터 정해야 합니다.

## 완료 로그를 남기는 미들웨어

다음 예제는 서버에서 요청 ID를 만들고 응답 헤더와 `res.locals`에 저장합니다. 외부에서 받은 임의의 값을 그대로 신뢰하는 정책은 두지 않았습니다.

```typescript
// http-logging.middleware.ts
import { Inject, Injectable, NestMiddleware } from '@nestjs/common';
import { randomUUID } from 'node:crypto';
import { performance } from 'node:perf_hooks';
import type { NextFunction, Request, Response } from 'express';
import { WINSTON_MODULE_PROVIDER } from 'nest-winston';
import type { Logger } from 'winston';

@Injectable()
export class HttpLoggingMiddleware implements NestMiddleware {
  constructor(
    @Inject(WINSTON_MODULE_PROVIDER) private readonly logger: Logger,
  ) {}

  use(req: Request, res: Response, next: NextFunction): void {
    const requestId = randomUUID();
    const startedAt = performance.now();
    res.locals.requestId = requestId;
    res.setHeader('X-Request-Id', requestId);
    let recorded = false;

    const record = (outcome: 'completed' | 'aborted') => {
      if (recorded) return;
      recorded = true;
      const statusCode = outcome === 'completed' ? res.statusCode : null;
      const level = outcome === 'aborted' ? 'warn'
        : res.statusCode >= 500 ? 'error'
        : res.statusCode >= 400 ? 'warn' : 'info';

      this.logger.log({
        level,
        message: 'http_request',
        requestId,
        method: req.method,
        route: typeof req.route?.path === 'string' ? req.route.path : 'unmatched',
        statusCode,
        outcome,
        durationMs: Number((performance.now() - startedAt).toFixed(1)),
      });
    };

    res.once('finish', () => record('completed'));
    res.once('close', () => record('aborted'));
    next();
  }
}
```

정상 응답 후에도 `close`가 발생할 수 있어 중복 기록을 막았습니다. 종료 전에 끊긴 요청에는 기본값인 200을 성공 상태처럼 남기지 않습니다. `performance.now()`로 구간을 재고, 로그의 시각은 Winston의 timestamp로 남깁니다.

예제는 실제 URL 대신 라우트 패턴을 사용합니다. `/users/123`보다 `/users/:id`가 로그 집계에 유리하고 식별자 노출도 줄일 수 있기 때문입니다. 라우트가 아직 결정되지 않았거나 찾지 못하면 `unmatched`가 남습니다. 라우터를 여러 경로에 마운트한 애플리케이션은 중복되지 않는 라우트 이름을 따로 정하는 편이 좋겠습니다.

헤더·query·body를 통째로 기록하지 않습니다. Authorization, Cookie, 비밀번호, 서명 문서 내용 등을 로그로 복제하는 실수를 피하고, 업무 추적에 필요한 필드를 허용 목록으로 추가하는 편이 낫습니다.

## 모듈과 Nest 기본 로거에 연결한다

기존 `AppModule`에 `WinstonModule` 설정과 미들웨어를 추가합니다. `AppController`는 기존 컨트롤러를 가정하며, 기록할 다른 컨트롤러가 있으면 등록 대상에 포함합니다. 기존 모듈 구성은 유지해야 합니다.

```typescript
// app.module.ts
import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
import { WinstonModule } from 'nest-winston';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { HttpLoggingMiddleware } from './http-logging.middleware';
import { loggingOptions } from './logging.options';

@Module({
  imports: [WinstonModule.forRoot(loggingOptions)],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer): void {
    consumer.apply(HttpLoggingMiddleware).forRoutes(AppController);
  }
}
```

애플리케이션 부팅 과정의 로그도 같은 로거로 넘기려면 `main.ts`에서 연결합니다.

```typescript
// main.ts
import { NestFactory } from '@nestjs/core';
import { WINSTON_MODULE_NEST_PROVIDER } from 'nest-winston';
import { AppModule } from './app.module';

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(AppModule, { bufferLogs: true });
  app.useLogger(app.get(WINSTON_MODULE_NEST_PROVIDER));
  await app.listen(Number(process.env.PORT ?? 3000));
}

void bootstrap();
```

미들웨어에는 Winston 원본 인스턴스인 `WINSTON_MODULE_PROVIDER`를 주입했고, Nest의 기본 로거에는 `LoggerService` 인터페이스를 맞춘 `WINSTON_MODULE_NEST_PROVIDER`를 전달했습니다. 두 토큰을 구분해야 합니다. [nest-winston의 주입 방식](https://github.com/gremo/nest-winston)과 [NestJS의 로그 버퍼링 설정](https://docs.nestjs.com/techniques/logger)을 참고할 수 있습니다.

예상 로그 형태는 다음과 같습니다. 실제 측정 결과가 아니라 필드 구조를 설명하는 예시입니다.

```json
{
  "level": "info",
  "message": "http_request",
  "service": "api",
  "requestId": "서버가 생성한 UUID",
  "method": "GET",
  "route": "/users/:id",
  "statusCode": 200,
  "outcome": "completed",
  "durationMs": 12.3,
  "timestamp": "2026-09-12T03:00:00.000Z"
}
```

## 파일 저장과 회전은 별개의 설정이다

원래 예제는 로거 생성 시 날짜를 계산해 파일명에 넣었습니다. 이 방식은 자정이 지나도 프로세스를 재시작하지 않는 한 파일명이 바뀌지 않습니다.

![원래 예제로 생성한 당시 로그 파일 화면](2023-01-14-image3.png)
_당시 화면이며, 위 수정 예제는 application.log와 error.log를 기준으로 저장합니다._

수정 예제는 `maxsize`와 `maxFiles`로 크기 기반 회전·보관 개수를 제한합니다. 날짜 기준으로 나누고 싶다면 [winston-daily-rotate-file](https://github.com/winstonjs/winston-daily-rotate-file)의 `%DATE%`, `datePattern`, `maxFiles` 등의 설정을 사용할 수 있습니다. 날짜가 들어 있는 파일명과 실제 회전 기능은 구분해야 해요.

파일 경로는 프로세스의 작업 디렉터리를 기준으로 합니다. 실행 계정의 쓰기 권한과 디스크 여유를 확인하고, transport의 파일 쓰기 오류도 감지해야 합니다. 여러 프로세스가 같은 파일에 쓰는 구조라면 회전 충돌까지 고려해야 합니다. 컨테이너나 중앙 로그 수집 환경에서는 콘솔 출력만 남기고 외부 수집기가 저장·회전을 맡는 구성이 더 적합할 수 있습니다.

## 도입 후 확인할 것

설정 파일이 만들어졌다고 로깅이 끝난 것은 아닙니다. 다음은 실제 애플리케이션에서 확인할 기준입니다.

- 정상·4xx·5xx 요청이 의도한 레벨로 한 번씩 기록되는가?
- 처리 도중 연결을 끊었을 때 성공으로 잘못 남지 않는가?
- 응답의 요청 ID로 해당 로그를 찾을 수 있는가?
- 오류 필터·업무 로그에도 같은 ID를 연결할 수 있는가?
- 비밀번호·토큰 등 기록하면 안 되는 값이 남지 않는가?
- 파일 회전, 보관 개수, 쓰기 실패를 확인했는가?

요청 ID는 이 예제만으로 모든 비동기 작업에 자동 전파되지 않습니다. 다른 계층에서도 연결하려면 값을 명시적으로 전달하거나 비동기 컨텍스트를 설계해야 합니다. 처음부터 거대한 로깅 체계를 만들기보다는 **한 요청이 어떻게 끝났는지 추적할 수 있는 최소 필드와 운영 가능한 저장 정책**부터 갖추면 좋겠습니다.
