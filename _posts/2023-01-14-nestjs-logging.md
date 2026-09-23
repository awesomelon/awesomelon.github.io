---
title: NestJS 로깅 도입하기 (winston)
date: 2023-01-14 15:00:00 +0900
categories: [ENGINEERING, BACKEND, NestJS]
tags: [nestjs, logging, winston]
author: j-ho
img_path: /assets/img/for_post/
description: NestJS에 Winston 로깅 모듈을 붙이고 로그를 관리하는 과정을 정리합니다.
---

![2023-01-14-image1](2023-01-14-image1.png)
_Winston 로깅 시스템_

웹 API 서버를 운영하면 로그를 쌓는 게 정말 중요해요. NestJS에 Node.js의 대표적인 로그 모듈인 [winston](https://www.npmjs.com/package/winston)을 도입해서 로그를 남기는 방법을 정리해봤습니다.

---

## Middleware

미들웨어는 라우터 핸들러(컨트롤러) 전에 호출되는 함수예요. 요청·응답 객체에 접근하고 `next()`를 호출해 다음 미들웨어로 요청을 넘길 수 있습니다.

![2023-01-14-image2](2023-01-14-image2.png)
_NestJS 미들웨어 실행 흐름_

NestJS의 Middleware는 기본적으로 [express](https://expressjs.com/en/guide/using-middleware.html)의 Middleware와 동일합니다.

미들웨어에서 응답을 끝내지도 않고 `next()`도 호출하지 않으면 Request는 계속 응답 대기 상태가 됩니다.

---

## Winston 도입하기

### Installation

```bash
npm i winston
npm i nest-winston
npm i moment
```

### Logger Service

```typescript
import { LoggerService as LS } from '@nestjs/common';
import * as winston from 'winston';
import moment = require('moment');
import { utilities as nestWinstonModuleUtilities } from 'nest-winston';

const { errors, combine, timestamp, printf } = winston.format;

export class LoggerService implements LS {
  private logger: winston.Logger;

  constructor(service: string) {
    this.logger = winston.createLogger({
      transports: [
        new winston.transports.File({
          level: 'error',
          filename: `error-${moment(new Date()).format('YYYY-MM-DD')}.log`,
          dirname: 'logs',
          maxsize: 5000000,
          format: combine(
            errors({ stack: true }),
            timestamp({ format: 'isoDateTime' }),
            printf((info) => {
              return `${info.timestamp} ${info.level}: ${info.message}${info.stack ? '\n' + info.stack : ''}`;
            }),
          ),
        }),
        new winston.transports.Console({
          level: 'debug',
          format: combine(
            timestamp({ format: 'isoDateTime' }),
            nestWinstonModuleUtilities.format.nestLike(service, {
              prettyPrint: true,
            }),
          ),
        }),
        new winston.transports.File({
          filename: `application-${moment(new Date()).format('YYYY-MM-DD')}.log`,
          dirname: 'logs',
          maxsize: 5000000,
          format: combine(
            timestamp({ format: 'isoDateTime' }),
            printf((info) => {
              return `${info.timestamp} ${info.level}: ${info.message}${info.stack ? '\n' + info.stack : ''}`;
            }),
          ),
        }),
      ],
    });
  }

  log(message: string) {
    this.logger.log({ level: 'info', message });
  }
  info(message: string) {
    this.logger.info(message);
  }
  error(message: string, trace?: string) {
    this.logger.error(message, { stack: trace });
  }
  warn(message: string) {
    this.logger.warn(message);
  }
  debug(message: string) {
    this.logger.debug(message);
  }
  verbose(message: string) {
    this.logger.verbose(message);
  }
}
```

transport별 `level`은 기록할 중요도의 기준입니다. `error` 파일에는 오류만, 기본 `info` 레벨인 application 파일에는 info와 그보다 중요한 warn, error가 함께 기록됩니다. 기본 로그 레벨에서 경고 메서드 이름은 `warning()`이 아니라 `warn()`입니다.

### Logger Middleware

```typescript
import { Injectable, NestMiddleware } from '@nestjs/common';
import { LoggerService } from './logger.service';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  private readonly loggerService = new LoggerService('HTTP');

  use(req: Request, res: Response, next: NextFunction) {
    const tempUrl = req.method + ' ' + req.url.split('?')[0];
    this.loggerService.info(JSON.stringify({ url: tempUrl }));

    next();
  }
}
```

요청 메서드와 경로를 로그 파일로 남깁니다. 요청마다 로거와 파일 transport를 새로 만들지 않고 재사용합니다. header, query, body 전체를 기록하면 토큰이나 비밀번호도 남을 수 있으니, 추가 데이터는 필요한 필드만 선택하고 민감한 값은 마스킹해야 합니다.

### AppModule

```typescript
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(LoggerMiddleware).forRoutes(YourController);
  }
}
```

AppModule에 NestModule을 implements 합니다. LoggerMiddleware를 원하는 컨트롤러에 연결하면 끝이에요.

### 결과 확인

![2023-01-14-image3](2023-01-14-image3.png)
_생성된 로그 파일들_

위 예제의 날짜는 로거를 생성할 때 파일명에 고정됩니다. `maxsize`에 따른 파일 분할은 되지만, 프로세스를 계속 실행한 채 날짜가 바뀐다고 파일명이 자동으로 바뀌지는 않아요. 날짜별 회전이 필요하다면 별도의 회전 transport를 설정해야 합니다.

참고: [Winston 로그 레벨과 transport 설정](https://github.com/winstonjs/winston), [Express 미들웨어](https://expressjs.com/en/guide/using-middleware.html)
