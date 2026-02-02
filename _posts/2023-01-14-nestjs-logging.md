---
title: NestJS 로깅 도입하기 (winston)
date: 2023-01-14 15:00:00 +0900
categories: [ENGINEERING, BACKEND, NestJS]
tags: [nestjs, logging, winston]
author: j-ho
img_path: /assets/img/for_post/
description: NestJS에 Winston 로깅 모듈을 도입하여 효과적으로 로그를 관리하는 방법을 알아봅니다.
---

![2023-01-14-image1](2023-01-14-image1.png)
_Winston 로깅 시스템_

웹 API 서버를 운영할 때 중요한 게 로그를 쌓는 거예요. NestJS에 Node.js의 대표적인 로그 모듈인 [winston](https://www.npmjs.com/package/winston)을 도입해 로그를 남기는 방법을 알아봅시다.

---

## Middleware

미들웨어는 라우터 핸들러(컨트롤러) 전에 호출되는 함수예요. Request - Response 사이클 중에 request, response 객체에 접근할 수 있고, next 미들웨어 기능에 접근할 수 있습니다.

![2023-01-14-image2](2023-01-14-image2.png)
_NestJS 미들웨어 실행 흐름_

NestJS의 Middleware는 기본적으로 [express](https://expressjs.com/en/guide/using-middleware.html)의 Middleware와 동일합니다.

미들웨어에서 `next()`를 호출하지 않으면 Request는 계속 응답 대기 상태가 됩니다.

---

## Winston 도입하기

### Installation

```bash
npm i winston
npm i nest-winston
```

### Logger Service

```typescript
import { LoggerService as LS } from '@nestjs/common';
import * as winston from 'winston';
import * as moment from 'moment';
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
              return `${info.message}`;
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
              return `${info.message}`;
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
  error(message: string, trace: string) {
    this.logger.error(message, trace);
  }
  warn(message: string) {
    this.logger.warning(message);
  }
  debug(message: string) {
    this.logger.debug(message);
  }
  verbose(message: string) {
    this.logger.verbose(message);
  }
}
```

transports를 보면 level을 여러 개로 나눠놨는데, log 레벨에 따라 파일을 다르게 생성하기 위해서예요.

### Logger Middleware

```typescript
import { Injectable, NestMiddleware } from '@nestjs/common';
import { LoggerService } from './logger.service';
import { Request, Response } from 'express';

@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  constructor() {}
  use(req: Request, res: Response, next: Function) {
    const loggerService = new LoggerService(
      req.url.slice(1).split('/')[req.url.slice(1).split('/').length - 1],
    );
    const tempUrl = req.method + ' ' + req.url.split('?')[0];
    const _headers = req.headers ? req.headers : {};
    const _query = req.query ? req.query : {};
    const _body = req.body ? req.body : {};
    const _url = tempUrl ? tempUrl : {};

    loggerService.info(
      JSON.stringify({
        url: _url,
        headers: _headers,
        query: _query,
        body: _body,
      }),
    );

    next();
  }
}
```

header, query, body 등등을 log 파일로 남깁니다.

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

로그 파일은 날짜별로 자동 생성되고, 최대 크기에 도달하면 새 파일이 만들어져요.
