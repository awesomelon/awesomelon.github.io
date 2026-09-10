---
title: NestJS 예외 처리 (Error Exception)
date: 2023-01-07 17:00:00 +0900
categories: [ENGINEERING, BACKEND, NestJS]
tags: [nestjs, error handling, error, exception]
author: j-ho
img_path: /assets/img/for_post/
description: NestJS 내장 예외 처리 레이어와 커스텀 Exception Filter 사용법을 정리합니다.
---

![2023-01-07-image1](2023-01-07-image1.png)
_NestJS Exception Handling_

[NestJS](https://docs.nestjs.com/exception-filters)에는 요청 처리 과정에서 잡히지 않은 예외를 처리하는 Exceptions Layer가 내장되어 있습니다. 다만 요청 흐름 밖의 타이머나 백그라운드 작업에서 발생한 예외까지 모두 처리하는 것은 아닙니다.

![2023-01-07-image2](2023-01-07-image2.png)
_NestJS Exception Layer 동작 구조_

기본 필터는 `HttpException`이면 해당 상태 코드와 응답 내용을 사용합니다. 그 외에 알 수 없는 예외는 일반적으로 아래와 같은 500 응답으로 처리합니다.

```json
{
  "statusCode": 500,
  "message": "Internal server error"
}
```

---

## Exception Filters

기본 예외 필터가 자동으로 많은 경우의 예외 처리를 해주지만 custom으로 제어를 하고 싶은 경우가 있습니다. 예를 들어 다른 형태의 JSON 스키마로 반환하고 싶은 경우입니다.

```typescript
import { ExceptionFilter, Catch, ArgumentsHost, HttpException } from '@nestjs/common';
import { Request, Response } from 'express';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    const status = exception.getStatus();
    const exceptionResponse = exception.getResponse();

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message:
        typeof exceptionResponse === 'string'
          ? exceptionResponse
          : (exceptionResponse as { message?: string | string[] }).message ?? exception.message,
    });
  }
}
```

`@Catch(HttpException)`은 `HttpException`과 그 하위 클래스의 예외를 처리한다는 뜻입니다. HTTP 요청 중 발생한 모든 오류를 뜻하지는 않아요. 모든 예외를 받으려면 `@Catch()`를 사용하고 매개변수를 `unknown`으로 받은 뒤, `instanceof HttpException`으로 확인해 상태 코드와 응답을 분기해야 합니다. 위 코드는 Express 어댑터 기준입니다.

---

## Usage

### 컨트롤러 전체에 적용

```typescript
@UseFilters(HttpExceptionFilter)
@Controller('user')
export class UserController {
  constructor(private userService: UsersService) {}
  // ...
}
```

### 특정 라우팅 핸들러에만 적용

```typescript
@Controller('user')
export class UserController {
  constructor(private userService: UsersService) {}

  @UseFilters(HttpExceptionFilter)
  @Get()
  async find() {
    // ...
  }
}
```

### 적용 결과

```json
{
  "statusCode": 401,
  "timestamp": "2022-10-21T08:04:19.635Z",
  "path": "/api/v1/test",
  "message": "여기에 에러 메시지가 들어옵니다."
}
```

이렇게 커스텀 Exception Filter를 만들면 에러 응답 형식을 원하는 대로 통일할 수 있어요.
