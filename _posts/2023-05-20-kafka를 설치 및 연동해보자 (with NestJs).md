---
title: Kafka를 설치 및 연동해보자 (with NestJS)
date: 2023-05-20 17:24:00 +0900
categories: [ENGINEERING, BACKEND, Kafka]
tags: [kafka, message queue, pub/sub, nestjs, installation]
author: j-ho
img_path: /assets/img/for_post/
description: Kafka 설치부터 NestJS 연동까지 전체 과정 정리
---

![2023-05-20-image1](2023-05-20-image1.jpg)
_Apache Kafka_

Kafka 설치부터 NestJS 연동까지 전체 과정을 정리했어요. Kafka의 기본 개념이 궁금하다면 [카프카(kafka)란?](/posts/kafka가-뭐야) 글을 먼저 읽어보세요.

---

## 설치 방법

이 설치 예제는 Kafka 2.8.0의 ZooKeeper 구성을 재현합니다. Java 8 이상이 설치되어 있어야 하며, 최신 Kafka 버전의 설치 절차와는 다를 수 있습니다.

### Kafka 다운로드

```bash
wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.13-2.8.0.tgz
tar xvf kafka_2.13-2.8.0.tgz
cd kafka_2.13-2.8.0
```

### Zookeeper 구동

```bash
bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
```

Zookeeper는 분산 애플리케이션의 코디네이션 서비스로 Kafka 클러스터의 메타데이터를 관리해요.

![2023-05-20-image3](2023-05-20-image3.png)
_Zookeeper 아키텍처 구조_

### Kafka 구동

```bash
bin/kafka-server-start.sh -daemon config/server.properties
```

### 동작 테스트

```bash
# 토픽 생성
bin/kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092

# 토픽 리스트 확인
bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# 메시지 발행
bin/kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092

# 메시지 구독
bin/kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server localhost:9092
```

![2023-05-20-image6](2023-05-20-image6.png)
_Producer를 통한 메시지 발행_

![2023-05-20-image7](2023-05-20-image7.png)
_Consumer를 통한 메시지 구독_

---

## NestJS와 연동하기

### kafkajs 설치

```bash
yarn add kafkajs@2
```

### Kafka Service 생성

```typescript
import { Injectable, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { Kafka, Producer, Partitioners, Consumer } from 'kafkajs';

export interface KafkaConfig {
  clientId: string;
  brokers: string[];
  groupId: string;
}

@Injectable()
export class KafkaService implements OnModuleInit, OnModuleDestroy {
  private kafka: Kafka;
  private producer: Producer;
  private consumer: Consumer;

  constructor(private kafkaConfig: KafkaConfig) {
    this.kafka = new Kafka({
      clientId: this.kafkaConfig.clientId,
      brokers: this.kafkaConfig.brokers,
    });
    this.producer = this.kafka.producer({
      createPartitioner: Partitioners.DefaultPartitioner,
      allowAutoTopicCreation: true,
    });
    this.consumer = this.kafka.consumer({
      allowAutoTopicCreation: true,
      groupId: this.kafkaConfig.groupId,
    });
  }

  async onModuleInit() {
    await this.producer.connect();
    await this.consumer.connect();
  }

  async onModuleDestroy() {
    await this.consumer.disconnect();
    await this.producer.disconnect();
  }

  async sendMessage(kafkaTopic: string, kafkaMessage: string) {
    return this.producer.send({
      topic: kafkaTopic,
      messages: [{ value: kafkaMessage }],
    });
  }

  async subscribeTo(
    kafkaTopic: string,
    handler: (message: string | null) => Promise<void>,
  ) {
    await this.consumer.subscribe({ topic: kafkaTopic, fromBeginning: true });
    await this.consumer.run({
      eachMessage: async ({ message }) => {
        await handler(message.value?.toString() ?? null);
      },
    });
  }
}
```

이 예제는 문자열 메시지를 전송합니다. 연결은 모듈 초기화 때 한 번 열고 종료 시 닫아, 메시지마다 연결을 끊거나 동시 전송 도중 다른 요청의 연결을 닫지 않도록 합니다.

### Kafka Module 생성

```typescript
import { DynamicModule, Module } from '@nestjs/common';
import { KafkaConfig, KafkaService } from './kafka.service';

@Module({})
export class KafkaModule {
  static register(kafkaConfig: KafkaConfig): DynamicModule {
    return {
      global: true,
      module: KafkaModule,
      providers: [
        {
          provide: KafkaService,
          useValue: new KafkaService(kafkaConfig),
        },
      ],
      exports: [KafkaService],
    };
  }
}
```

### App Module에 Import

```typescript
import { Module } from '@nestjs/common';
import { KafkaModule } from './kafka.module';
import { AppService } from './app.service';

@Module({
  imports: [
    KafkaModule.register({
      clientId: `test-id`,
      brokers: ['localhost:9092'],
      groupId: 'consumer-group-id',
    }),
  ],
  providers: [AppService],
})
export class AppModule {}
```

### Producer 사용

```typescript
import { Injectable } from '@nestjs/common';
import { KafkaService } from './kafka.service';

@Injectable()
export class AppService {
  constructor(private readonly kafkaService: KafkaService) {}

  async sendMessage() {
    return this.kafkaService.sendMessage('test-topic', 'Hello World!');
  }
}
```

![2023-05-20-gif1](2023-05-20-gif1.gif)
_NestJS Producer 테스트 결과_

### Consumer 구독하기

`@SubscribeTo`는 NestJS나 KafkaJS가 기본 제공하는 데코레이터가 아닙니다. 별도 구현 없이도 실행할 수 있도록 위 AppService를 아래처럼 확장합니다. 이 간단한 예제에서는 하나의 Topic과 handler를 등록하고, KafkaService의 연결이 끝난 뒤 구독을 시작합니다.

```typescript
import { Injectable, OnApplicationBootstrap } from '@nestjs/common';
import { KafkaService } from './kafka.service';

@Injectable()
export class AppService implements OnApplicationBootstrap {
  constructor(private readonly kafkaService: KafkaService) {}

  async onApplicationBootstrap() {
    await this.kafkaService.subscribeTo('test-topic', async (message) => {
      console.log('message', message);
    });
  }

  async sendMessage() {
    return this.kafkaService.sendMessage('test-topic', 'Hello World!');
  }
}
```

`fromBeginning: true`는 그룹에 유효한 commit offset이 없을 때 처음부터 읽도록 합니다. 매번 모든 메시지를 다시 읽는 설정은 아닙니다. 프로세스 종료 신호에도 Nest의 종료 훅을 실행하려면 `main.ts`에서 `app.enableShutdownHooks()`를 호출하세요.

![2023-05-20-gif2](2023-05-20-gif2.gif)
_NestJS Consumer 테스트 결과_

자세한 내용은 [Kafka 공식 문서](https://kafka.apache.org/documentation), [KafkaJS 2.2.4 Producer 문서](https://github.com/tulios/kafkajs/blob/v2.2.4/docs/Producing.md), [Consumer 문서](https://github.com/tulios/kafkajs/blob/v2.2.4/docs/Consuming.md), [NestJS 생명주기 훅](https://docs.nestjs.com/fundamentals/lifecycle-events)을 확인해 보세요.
