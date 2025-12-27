---
title: Kafka를 설치 및 연동해보자 (with NestJS)
date: 2023-05-20 17:24:00 +0900
categories: [ENGINEERING,BACKEND, Kafka]
tags: [kafka, message queue, pub/sub, nestjs, installation]
author: j-ho
img_path: /assets/img/for_post/
description: Apache Kafka를 설치하고 NestJS 프로젝트에 연동하는 전체 과정을 단계별로 알아봅니다.
---

![2023-05-20-image1](2023-05-20-image1.jpg)
_Apache Kafka_

이 글에서는 Kafka 설치부터 NestJS 연동까지의 전체 과정을 다룹니다. Kafka의 기본 개념이 궁금하다면 [카프카(kafka)란?](https://j-ho.dev/posts/kafka가-뭐야) 글을 먼저 참고하세요.

## 설치 방법

### STEP 1. Kafka 다운로드
```bash
# 다운로드
wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.13-2.8.0.tgz

# 압축 풀기
tar xvf kafka_2.13-2.8.0.tgz

cd kafka_2.13-2.8.0
```

### STEP 2. Zookeeper 구동
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

백그라운드로 구동시키고 싶을 경우 `-daemon` 명령어를 추가합니다.
```bash
bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
```

#### Zookeeper란?

분산 애플리케이션을 구축하다보면, 분산 애플리케이션 관리를 위한 안정적인 코디네이션 애플리케이션이 추가로 필요하게 됩니다. 따라서 안정적인 코디네이션 서비스로 검증된 주키퍼를 많이 사용하게 됩니다.

**주키퍼**는 분산 애플리케이션이 안정적인 서비스를 할 수 있도록 분산되어 있는 각 애플리케이션의 정보를 중앙에 집중하고 구성 관리, 그룹 관리 네이밍, 동기화 등의 서비스를 제공합니다.

![2023-05-20-image3](2023-05-20-image3.png)
_Zookeeper 아키텍처 구조_

서버 여러 대를 클러스터로 구성하고, 분산 애플리케이션들이 각각 클라이언트가 되어 주키퍼 서버들과 커넥션을 맺은 후 **상태 정보** 등을 주고 받습니다.

위의 그림에서 Server는 주키퍼, Client는 카프카가 됩니다.

> Zookeeper는 Kafka의 메타데이터 관리와 클러스터 코디네이션을 담당합니다. Kafka 2.8+에서는 Zookeeper 없이도 운영 가능한 KRaft 모드가 도입되었습니다.
{: .prompt-info }

### STEP 3. Kafka 구동
```bash
bin/kafka-server-start.sh -daemon config/server.properties
```

서비스가 제대로 띄워졌는지 확인해보려면 포트가 정상적으로 리스닝 중인 것을 확인해보면 됩니다.
```bash
netstat -an | grep 2181 # 2181포트는 zookeeper의 client Port
```

![2023-05-20-image2](2023-05-20-image2.png)
_Zookeeper 포트 확인_

### STEP 4. 동작 테스트

#### 토픽 생성
```bash
bin/kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092

# 결과 로그
Created topic test-topic
```

**예시:**

![2023-05-20-image4](2023-05-20-image4.png)
_토픽 생성 결과_

**주요 옵션:**
- `--create`: 토픽 생성
- `--topic [topic-name]`: 생성할 토픽 이름
- `--partitions [number]`: 생성할 토픽의 파티션 개수
- `--replication-factor [number]`: 각 파티션 내 메시지를 복제할 Replica의 개수
- `--bootstrap-server`: 연결될 카프카 서버

#### 토픽 리스트 확인
```bash
bin/kafka-topics.sh --list --zookeeper localhost:2181

# 결과 로그
test-topic
```

**예시:**

![2023-05-20-image5](2023-05-20-image5.png)
_토픽 리스트 확인_

#### 메시지 발행 (Producer)
```bash
bin/kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092
```

명령어 실행 후 `>` 라인이 생기면 메시지 입력 가능합니다. Enter 키 입력 시 메시지가 발행됩니다.

![2023-05-20-image6](2023-05-20-image6.png)
_Producer를 통한 메시지 발행_

#### 메시지 구독 (Consumer)
```bash
bin/kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server localhost:9092
```

Producer로 발행한 메시지 내용을 확인해 볼 수 있습니다.

![2023-05-20-image7](2023-05-20-image7.png)
_Consumer를 통한 메시지 구독_

> `--from-beginning` 옵션을 사용하면 토픽에 저장된 모든 메시지를 처음부터 읽어옵니다.
{: .prompt-tip }

## NestJS와 연동하기

NestJS가 기본적으로 설치되어 있다고 가정합니다.

### 1. kafkajs 설치
```bash
yarn add kafkajs
```

### 2. Kafka Service 로직 생성
```typescript
import { Injectable, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { Kafka, Producer, Partitioners, Consumer } from 'kafkajs';
import { SUBSCRIBER_FN_REF_MAP, SUBSCRIBER_OBJ_REF_MAP } from './kafka.decorator';
import { KafkaConfig } from './kafka.message';

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

  async onModuleInit(): Promise<void> {
    await this.connect();

    SUBSCRIBER_FN_REF_MAP.forEach((functionRef, topic) => {
      console.log('subscribe', topic);
      this.bindAllTopicToConsumer(functionRef, topic);
    });

    await this.consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        const functionRef = SUBSCRIBER_FN_REF_MAP.get(topic);
        const object = SUBSCRIBER_OBJ_REF_MAP.get(topic);
        await functionRef.apply(object, [message.value.toString()]);
      },
    });
  }

  async onModuleDestroy(): Promise<void> {
    await this.disconnect();
  }

  async connect() {
    await this.producer.connect();
    await this.consumer.connect();
  }

  async disconnect() {
    await this.producer.disconnect();
    await this.consumer.disconnect();
  }

  async sendMessage(kafkaTopic: string, kafkaMessage) {
    await this.producer.connect();
    const metadata = await this.producer
      .send({
        topic: kafkaTopic,
        messages: [{ value: JSON.stringify(kafkaMessage) }],
      })
      .catch((e) => console.error(e.message, e));
    await this.producer.disconnect();
    return metadata;
  }

  async bindAllTopicToConsumer(callback, _topic) {
    await this.consumer.subscribe({ topic: _topic, fromBeginning: false });
  }
}
```

### 3. Kafka Module 생성
```typescript
import { DynamicModule, Global, Module } from '@nestjs/common';
import { KafkaService } from './kafka.service';
import { KafkaConfig } from './kafka.message';

@Global()
@Module({})
export class KafkaModule {
  static register(kafkaConfig: KafkaConfig): DynamicModule {
    console.log('KafkaModule.register', kafkaConfig);
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

### 4. Kafka Type 및 Decorator 생성
```typescript
// type
export class KafkaPayload {
  public body: any;
  public messageId: string;
  public messageType: string;
  public topicName: string;
  public createdTime?: string;

  create?(messageId, body, messageType, topicName): KafkaPayload {
    return {
      messageId,
      body,
      messageType,
      topicName,
      createdTime: new Date().toISOString(),
    };
  }
}

export declare class KafkaConfig {
  clientId: string;
  brokers: string[];
  groupId: string;
}

// decorator
export const SUBSCRIBER_FN_REF_MAP = new Map();
export const SUBSCRIBER_OBJ_REF_MAP = new Map();

export function SubscribeTo(topic) {
  return (target, propertyKey, descriptor) => {
    const originalMethod = target[propertyKey];
    SUBSCRIBER_FN_REF_MAP.set(topic, originalMethod);
    SUBSCRIBER_OBJ_REF_MAP.set(topic, target);
    return descriptor;
  };
}
```

> `@SubscribeTo` 데코레이터를 사용하면 특정 토픽을 구독하는 메서드를 간단하게 정의할 수 있습니다.
{: .prompt-tip }

### 5. App Module에 Kafka Module Import
```typescript
import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { KafkaModule } from './kafka/kafka.module';

@Module({
  imports: [
    KafkaModule.register({
      clientId: `test-id`,
      brokers: ['localhost:9092'],
      groupId: 'consumer-group-id',
    }),
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```

### 6. App Service Producer 함수 생성
```typescript
import { Injectable } from '@nestjs/common';
import { Producer } from 'kafkajs';
import { KafkaService } from './kafka/kafka.service';

@Injectable()
export class AppService {
  constructor(private readonly kafkaService: KafkaService) {}

  async sendMessage() {
    return this.kafkaService.sendMessage('test-topic', 'Hello World!');
  }
}
```

### 7. Producer 테스트
```bash
# 메시지 발행
curl -X POST http://localhost:3000/send-message

# 메시지 구독
bin/kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server localhost:9092
```

![2023-05-20-gif1](2023-05-20-gif1.gif)
_NestJS Producer 테스트 결과_

### 8. App Service Consumer 함수 생성
```typescript
import { Injectable } from '@nestjs/common';
import { SubscribeTo } from './kafka/kafka.decorator';
import { KafkaService } from './kafka/kafka.service';

@Injectable()
export class AppService {
  // ... 이전 코드

  @SubscribeTo('test-topic')
  async subscribeToTestTopic(message: string) {
    console.log('message', message);
  }
}
```

![2023-05-20-gif2](2023-05-20-gif2.gif)
_NestJS Consumer 테스트 결과_

## 정리

Kafka 설치 및 NestJS 연동 단계:

### 설치 과정

| 단계 | 명령어 | 설명 |
|:---:|:---|:---|
| **1** | Kafka 다운로드 및 압축 해제 | wget으로 다운로드 후 tar로 압축 해제 |
| **2** | Zookeeper 구동 | `zookeeper-server-start.sh` |
| **3** | Kafka 구동 | `kafka-server-start.sh` |
| **4** | 동작 테스트 | 토픽 생성 및 메시지 송수신 테스트 |

### NestJS 연동 과정

**필요한 컴포넌트:**
1. **KafkaService**: Kafka 연결 및 메시지 송수신 로직
2. **KafkaModule**: Dynamic Module로 설정 주입
3. **Decorator**: `@SubscribeTo`로 토픽 구독 선언
4. **Type 정의**: KafkaConfig, KafkaPayload 등

**주요 기능:**
- **Producer**: `sendMessage()` 메서드로 메시지 발행
- **Consumer**: `@SubscribeTo` 데코레이터로 토픽 구독
- **자동 연결 관리**: `OnModuleInit`/`OnModuleDestroy` 훅 활용

> Producer와 Consumer를 분리하여 구현하면 마이크로서비스 아키텍처에서 유연하게 활용할 수 있습니다.
{: .prompt-info }

더 자세한 내용은 [Kafka 공식 문서](https://kafka.apache.org/documentation)를 참고하세요.