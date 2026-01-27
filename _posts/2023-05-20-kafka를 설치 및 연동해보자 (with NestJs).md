---
title: Kafka를 설치 및 연동해보자 (with NestJS)
date: 2023-05-20 17:24:00 +0900
categories: [ENGINEERING, BACKEND, Kafka]
tags: [kafka, message queue, pub/sub, nestjs, installation]
author: j-ho
img_path: /assets/img/for_post/
description: Apache Kafka를 설치하고 NestJS 프로젝트에 연동하는 전체 과정을 단계별로 알아봅니다.
---

![2023-05-20-image1](2023-05-20-image1.jpg)
_Apache Kafka_

Kafka 설치부터 NestJS 연동까지의 전체 과정을 다룹니다. Kafka의 기본 개념이 궁금하다면 [카프카(kafka)란?](/posts/kafka가-뭐야) 글을 먼저 참고하세요.

---

## 설치 방법

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

Zookeeper는 분산 애플리케이션의 코디네이션 서비스로, Kafka 클러스터의 메타데이터 관리를 담당합니다.

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
bin/kafka-topics.sh --list --zookeeper localhost:2181

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
yarn add kafkajs
```

### Kafka Service 생성

```typescript
import { Injectable, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { Kafka, Producer, Partitioners, Consumer } from 'kafkajs';

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

  async sendMessage(kafkaTopic: string, kafkaMessage) {
    await this.producer.connect();
    const metadata = await this.producer.send({
      topic: kafkaTopic,
      messages: [{ value: JSON.stringify(kafkaMessage) }],
    });
    await this.producer.disconnect();
    return metadata;
  }
}
```

### Kafka Module 생성

```typescript
@Global()
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
@Module({
  imports: [
    KafkaModule.register({
      clientId: `test-id`,
      brokers: ['localhost:9092'],
      groupId: 'consumer-group-id',
    }),
  ],
})
export class AppModule {}
```

### Producer 사용

```typescript
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

### Consumer Decorator 사용

```typescript
@Injectable()
export class AppService {
  @SubscribeTo('test-topic')
  async subscribeToTestTopic(message: string) {
    console.log('message', message);
  }
}
```

![2023-05-20-gif2](2023-05-20-gif2.gif)
_NestJS Consumer 테스트 결과_

더 자세한 내용은 [Kafka 공식 문서](https://kafka.apache.org/documentation)를 참고하세요.
