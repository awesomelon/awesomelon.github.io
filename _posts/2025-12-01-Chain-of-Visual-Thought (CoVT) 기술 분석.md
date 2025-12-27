---
title: "Chain-of-Visual-Thought (CoVT) 기술 분석"
date: 2025-12-01 10:24:34 +0900
categories: [AI/ML, Computer Vision]
tags: [vlm, chain-of-thought, computer vision, multimodal, visual reasoning, covt]
author: j-ho
img_path: /assets/img/for_post/
pin: false
description: Vision-Language Model이 시각적으로 사고하도록 만드는 CoVT 프레임워크의 혁신적 접근 방식을 분석합니다.
---

> **📌 KEYWORDS**  
> `VLM` `Chain-of-Thought` `Visual Reasoning` `Multimodal AI` `Vision Tokens` `Distillation`
{: .prompt-info }

> **📄 원문 출처**  
> 이 글은 UC Berkeley와 UCLA 연구진이 발표한 논문 **"Chain-of-Visual-Thought: Teaching VLMs to See and Think Better with Continuous Visual Tokens"** 를 토대로 작성되었습니다.
{: .prompt-info }

---

## 🚀 들어가며

최근 대형 언어 모델(LLM)의 추론 능력을 비약적으로 끌어올린 일등 공신은 단연 **'생각의 사슬(Chain-of-Thought, CoT)'** 기법입니다.

### CoT의 성공과 한계
```text
Chain-of-Thought 진화:

텍스트 LLM
├── 복잡한 문제를 단계별로 분해
├── 중간 추론 과정 명시
└── ✅ 강력한 성능 향상

Vision-Language Model (VLM)
├── 텍스트 CoT 적용 시도
├── 시각 정보 → 텍스트 변환
└── ❌ 정보 손실 발생
```
{: .nolineno }

복잡한 문제를 단계별로 쪼개어 해결하는 이 방식은 강력했지만, **Vision-Language Model(VLM)** 분야에서는 뚜렷한 한계에 부딪혔습니다.

| 질문 유형 | 텍스트 CoT 적합성 | 한계 |
|:---|:---:|:---|
| "사과가 몇 개지?" | ❌ | 공간 정보 손실 |
| "책상 뒤에 가려진 건 뭐지?" | ❌ | 기하학적 관계 표현 어려움 |
| "이 물체는 저것보다 가까운가?" | ❌ | 깊이 정보 불충분 |

"사과가 몇 개지?", "책상 뒤에 가려진 건 뭐지?" 같은 **시각적 인식(Perception)** 문제를 풀 때, 텍스트만으로는 이미지의 풍부한 공간적·기하학적 정보를 모두 담아내기 어려웠기 때문입니다.

---

### CoVT의 등장

![CoVT 프레임워크](2025-12-01-image1.jpg)
_Chain-of-Visual-Thought 프레임워크 개요_

오늘 소개할 논문은 이러한 제약을 넘어서기 위한 새로운 시도입니다.

> **🎯 핵심 아이디어**  
> UC Berkeley와 UCLA 연구진은 텍스트뿐만 아니라 **'연속적인 시각 토큰(Continuous Visual Tokens)'** 을 활용해 모델이 시각적으로 사고하게 만드는 'CoVT' 프레임워크를 제안합니다.
{: .prompt-tip }

---

## 🚧 1. 문제의식: 언어 병목 현상 (Language Bottleneck)

기존 VLM의 CoT 방식은 시각 정보를 억지로 **텍스트 공간(Discrete Text Space)** 에 끼워 맞추는 식이었습니다.

### 전통적 VLM CoT의 문제
```text
기존 VLM의 처리 과정:

이미지 입력
    ↓
시각 인코딩
    ↓
[병목 발생]
텍스트로 변환
"A는 왼쪽에, B는 뒤에 있다"
    ↓
텍스트 기반 추론
    ↓
최종 답변
```
{: .nolineno }

예를 들어, 물체의 위치 관계를 파악할 때 "A는 왼쪽에, B는 뒤에 있다"라고 텍스트로 먼저 변환한 뒤 추론을 시작하는 것이죠.

---

### 언어 병목의 구체적 문제

이 과정에서 필연적으로 **'언어 병목(Language Bottleneck)'** 이 발생합니다.

#### 1. 정보 손실 (Information Loss)

| 시각 정보 유형 | 텍스트 표현 가능성 | 손실 정도 |
|:---|:---:|:---:|
| **엣지(Edge)** | 매우 어려움 | 높음 |
| **깊이(Depth)** | 모호함 | 매우 높음 |
| **세밀한 분할(Segmentation)** | 불가능 | 극히 높음 |
| **픽셀 단위 관계** | 불가능 | 극히 높음 |

이미지의 엣지(Edge), 깊이(Depth), 세밀한 분할(Segmentation) 정보 등은 **텍스트로 온전히 표현하기 힘듭니다**.
```python
# 정보 손실 예시 (개념적)
class TraditionalVLM:
    def process_image(self, image):
        # 풍부한 시각 정보
        visual_features = {
            'edges': image.detect_edges(),      # 수백만 픽셀
            'depth': image.estimate_depth(),    # 연속적 값
            'segments': image.segment_objects() # 복잡한 마스크
        }
        
        # 텍스트로 압축 → 정보 손실
        text_description = self.compress_to_text(visual_features)
        # 결과: "3개의 물체가 있고, 하나는 앞에 있음"
        
        return text_description  # 대부분의 정보 손실됨
```
{: .nolineno }

#### 2. 오류 누적 (Error Propagation)
```text
오류 전파 과정:

초기 변환 오류 (5% 에러)
    ↓
텍스트 추론 (정확도 95%)
    ↓
최종 결과 (에러 누적)
    ↓
정답 가능성 < 90%
```
{: .nolineno }

첫 단추인 텍스트 변환 과정에서 시각적 정보를 잘못 해석하면, 이후 논리가 아무리 정교해도 결국 오답을 내게 됩니다.

> **⚠️ 복합적 문제**  
> 언어 병목은 단순히 정보가 손실되는 것뿐만 아니라, 초기 오류가 증폭되는 복합적 문제를 야기합니다.
{: .prompt-warning }

---

### CoVT의 해결책

CoVT는 모델이 **'시각적 사고(Visual Thought)'** 를 할 수 있도록, 추론 과정에서 텍스트 토큰과 함께 **시각 정보를 담은 토큰을 함께 생성**하는 방식으로 이 문제를 해결합니다.
```text
CoVT의 처리 과정:

이미지 입력
    ↓
시각 인코딩
    ↓
[병목 제거]
연속적 시각 토큰 생성
+ 텍스트 토큰
    ↓
멀티모달 추론
    ↓
최종 답변 (정보 보존)
```
{: .nolineno }

---

## 🧩 2. 핵심 원리: 연속적 시각 토큰 (Continuous Visual Tokens)

CoVT의 가장 흥미로운 점은 추론 과정(Thinking Process)에서 생성되는 토큰이 단순한 텍스트가 아닌, **압축된 시각적 잠재 표현(Compact Latent Representations)** 이라는 것입니다.

### 인간 시각 인지 모방

연구진은 **인간의 시각 인지 과정**을 모방해 4가지 핵심 시각 능력을 정의하고, 이를 **경량화된 비전 전문가(Lightweight Vision Experts)** 모델들로부터 추출(Distillation)해 VLM에 가르쳤습니다.
```text
인간 시각 인지 → AI 시각 토큰:

인간이 사물을 볼 때:
├── 형태 파악 (Segmentation)
├── 거리 감각 (Depth)
├── 윤곽 인식 (Edge)
└── 의미 이해 (Semantic)

CoVT의 4가지 시각 토큰:
├── Segmentation Tokens
├── Depth Tokens
├── Edge Tokens
└── Semantic Tokens
```
{: .nolineno }

---

### 4가지 시각 토큰과 전문가 모델

CoVT는 VLM이 다음 4가지 유형의 시각 토큰을 **순차적(Autoregressive)** 으로 예측하도록 학습합니다.

#### 1. Segmentation Tokens (객체 인식 및 2D 공간)

| 속성 | 설명 |
|:---|:---|
| **역할** | 물체가 어디에 있고 어떤 모양인지 파악 |
| **교사 모델** | **SAM (Segment Anything Model)** |
| **출력** | 객체 마스크 (Object Mask) |
| **작동 방식** | 생성된 토큰 → SAM Decoder 프롬프트 → 마스크 복원 |
```python
# Segmentation Token 생성 (개념적)
class SegmentationTokenGenerator:
    def __init__(self, sam_encoder):
        self.sam_encoder = sam_encoder
        
    def generate_token(self, image, vlm_thought):
        # VLM이 생성한 시각적 사고를 토큰으로 압축
        seg_token = vlm_thought.extract_segmentation_info()
        
        # 검증: 토큰을 SAM 디코더에 입력하여 마스크 복원
        predicted_mask = self.sam_decoder(seg_token)
        ground_truth_mask = self.sam_encoder(image)
        
        # 손실 계산 및 학습
        loss = self.compute_mask_loss(predicted_mask, ground_truth_mask)
        return seg_token, loss
```
{: .nolineno }

#### 2. Depth Tokens (3D 공간 관계)

| 속성 | 설명 |
|:---|:---|
| **역할** | 픽셀 단위의 원근감과 깊이 정보 (앞/뒤 관계) |
| **교사 모델** | **DepthAnything v2** |
| **출력** | 깊이 맵 (Depth Map) |
| **작동 방식** | 토큰 + DepthAnything 인코더 특징 → 깊이 맵 재구성 |

#### 3. Edge Tokens (구조 및 기하학)

| 속성 | 설명 |
|:---|:---|
| **역할** | 물체의 경계선과 전체적인 구조적 단서 |
| **교사 모델** | **PIDINet** |
| **출력** | 엣지 맵 (Edge Map) |
| **작동 방식** | 1×1 Convolution 커널 → 엣지 맵 복원 |

#### 4. Semantic Tokens (의미적 이해)

| 속성 | 설명 |
|:---|:---|
| **역할** | 이미지의 패치(Patch) 수준에서 의미론적 특징 |
| **교사 모델** | **DINOv2** |
| **출력** | 의미 특징 벡터 (Semantic Features) |
| **작동 방식** | DINO 특징 벡터와 직접 정렬 (MSE Loss) |

---

### 통합 프레임워크
```text
CoVT 시각 토큰 생성 파이프라인:

입력 이미지
    ↓
VLM 인코더
    ↓
┌─────────────────────────────────┐
│   연속적 시각 토큰 생성         │
├─────────────────────────────────┤
│ Segmentation → 객체 위치        │
│ Depth        → 원근 관계        │
│ Edge         → 구조 정보        │
│ Semantic     → 의미 이해        │
└─────────────────────────────────┘
    ↓
전문가 디코더 (필요시)
    ↓
시각화 가능한 출력
```
{: .nolineno }

| 토큰 유형 | 담당 정보 | 전문가 모델 | 복원 방식 |
|:---|:---|:---|:---|
| **Segmentation** | 객체 형태 | SAM | Decoder 프롬프트 |
| **Depth** | 3D 공간 | DepthAnything v2 | 특징 결합 |
| **Edge** | 경계선 | PIDINet | 1×1 Conv |
| **Semantic** | 의미 | DINOv2 | Feature 정렬 |

---

## 🏗️ 3. 모델 아키텍처 및 학습 파이프라인

CoVT는 실제 추론 시에는 무거운 **외부 도구(External Tools)** 를 호출하지 않습니다.

### 핵심 전략: 내재화 (Internalization)

대신 학습 단계에서 외부 전문가 모델의 능력을 VLM의 파라미터 안에 **녹여내는(Internalize)** 방식을 택했습니다.
```text
학습 vs 추론:

학습 단계 (Training)
├── 4개 전문가 모델 활용
├── 시각 토큰 정렬
└── VLM 파라미터에 지식 증류

추론 단계 (Inference)
├── 외부 모델 불필요
├── VLM만으로 시각 토큰 생성
└── 필요시에만 디코더 사용
```
{: .nolineno }

이를 위해 **"Think → Decode → Reconstruct"** 구조를 따릅니다.

---

### 정렬 전략 (Alignment Strategy)

획일적으로 특징 벡터값을 맞추기보다는, **전문가 모델마다 가장 효과적인 학습 방식**을 따로 적용했습니다.

#### 1. Task-Oriented Alignment
```python
# Task-Oriented Alignment (개념적)
class TaskOrientedAlignment:
    """SAM, DepthAnything처럼 결과물의 디테일이 중요한 경우"""
    
    def align(self, vlm_token, expert_model, ground_truth):
        # VLM이 생성한 토큰을 Decoder 프롬프트로 사용
        predicted_output = expert_model.decoder(vlm_token)
        
        # 최종 결과물 비교
        loss = self.task_loss(predicted_output, ground_truth)
        
        return loss

# 예시: Segmentation
seg_loss = dice_loss(predicted_mask, gt_mask)

# 예시: Depth
depth_loss = mse_loss(predicted_depth, gt_depth)
```
{: .nolineno }

| 모델 | 정렬 방식 | 손실 함수 |
|:---|:---|:---|
| **SAM** | Decoder 프롬프트 | Dice Loss (마스크) |
| **DepthAnything** | 특징 결합 | MSE Loss (깊이 맵) |

SAM이나 DepthAnything처럼 결과물의 디테일이 중요한 경우, VLM이 생성한 토큰을 **Decoder의 프롬프트**로 활용해 최종 결과물(마스크, 깊이 맵)을 만들고, 이를 정답 데이터(Ground Truth)와 비교합니다.

#### 2. Feature Alignment
```python
# Feature Alignment (개념적)
class FeatureAlignment:
    """DINO처럼 표현 학습이 핵심인 모델"""
    
    def align(self, vlm_features, dino_features):
        # 특징 벡터 공간에서 유사도 측정
        loss = mse_loss(vlm_features, dino_features)
        
        return loss
```
{: .nolineno }

DINO처럼 표현 학습이 핵심인 모델은 **특징 벡터 공간에서의 유사도**를 좁히는 방식으로 학습합니다.

---

### 4단계 학습 과정 (Four-Stage Training)

모델이 시각적으로 '생각'하는 법을 체득하도록 **커리큘럼 학습(Curriculum Learning)** 을 적용했습니다.
```text
4단계 커리큘럼 학습:

Stage 1: Comprehension
    ↓
Stage 2: Generation
    ↓
Stage 3: Reasoning
    ↓
Stage 4: Efficient Reasoning
```
{: .nolineno }

#### Stage 1: Comprehension (이해)

| 목표 | 방법 | 성과 |
|:---|:---|:---|
| 시각 토큰의 의미 파악 | 전문가 모델 출력 관찰 | 기초 이해 형성 |

**시각 토큰이 무엇을 의미하는지 배우는 기초 단계**입니다.
```python
# Stage 1: Comprehension
def stage1_training(vlm, expert_models, images):
    for image in images:
        # 전문가 모델의 출력 관찰
        sam_output = expert_models.sam(image)
        depth_output = expert_models.depth(image)
        
        # VLM에게 "이것이 segmentation이다" 학습
        vlm.learn_token_meaning(sam_output, token_type='segmentation')
        vlm.learn_token_meaning(depth_output, token_type='depth')
```
{: .nolineno }

#### Stage 2: Generation (생성)

**주어진 이미지에 맞는 정확한 시각 토큰을 생성하도록 훈련**합니다.
```python
# Stage 2: Generation
def stage2_training(vlm, expert_models, images):
    for image in images:
        # VLM이 시각 토큰 생성 시도
        generated_tokens = vlm.generate_visual_tokens(image)
        
        # 전문가 모델과 비교
        expert_tokens = expert_models.extract_tokens(image)
        
        # 정렬 손실 계산
        loss = alignment_loss(generated_tokens, expert_tokens)
        loss.backward()
```
{: .nolineno }

#### Stage 3: Reasoning (추론)

**질문에 답하는 과정(Chain-of-Thought) 속에 시각 토큰을 자연스럽게 섞어 쓰도록** 합니다.
```text
Stage 3 추론 예시:

질문: "빨간 사과는 몇 개인가?"

VLM의 사고 과정:
1. [Segmentation Token] → 사과 위치 파악
2. [Semantic Token] → 빨간색 필터링
3. [Text] "빨간 사과는 3개 보입니다"
4. [Segmentation Token] → 확인용 마스크 생성
5. [Text] "따라서 답은 3개입니다"
```
{: .nolineno }

#### Stage 4: Efficient Reasoning (효율적 추론)

**시각 토큰 일부를 무작위로 제거(Drop)** 해도 남은 정보로 강건하게 추론하도록 학습시켜 효율성을 높이고 과적합을 방지합니다.
```python
# Stage 4: Efficient Reasoning
def stage4_training(vlm, questions, images):
    for question, image in zip(questions, images):
        # 시각 토큰 생성
        visual_tokens = vlm.generate_visual_tokens(image)
        
        # 랜덤하게 일부 토큰 제거 (예: 30%)
        dropped_tokens = random_drop(visual_tokens, drop_rate=0.3)
        
        # 제거된 토큰으로도 정답 도출
        answer = vlm.reason_with_tokens(question, dropped_tokens)
        
        # 강건성 학습
        loss = reasoning_loss(answer, ground_truth)
```
{: .nolineno }

| 단계 | 목표 | 핵심 기법 |
|:---:|:---|:---|
| **1** | 이해 | 전문가 모델 관찰 |
| **2** | 생성 | 정렬 학습 |
| **3** | 추론 | CoT 통합 |
| **4** | 효율화 | 토큰 드롭아웃 |

---

## ✨ 4. CoVT의 기술적 강점

### 1. 해석 가능한 시각적 사고 (Interpretable Visual Thinking)

기존의 Latent Reasoning 모델들은 내부 동작이 **'블랙박스'** 에 가까웠습니다.
```text
기존 모델:
입력 → [???] → 출력
(내부 과정 불투명)

CoVT:
입력 → [시각 토큰 생성] → [디코딩] → 시각화
(과정 확인 가능)
```
{: .nolineno }

반면 CoVT는 생성된 시각 토큰을 디코더에 통과시켜 사람이 **직관적으로 볼 수 있는 이미지**(Segmentation Mask, Depth Map 등)로 복원해 줍니다.

#### 시각화 예시
```python
# CoVT의 해석 가능성
class InterpretableCoVT:
    def explain_reasoning(self, question, image):
        # 1. 시각 토큰 생성
        visual_tokens = self.vlm.think(question, image)
        
        # 2. 각 토큰을 사람이 볼 수 있는 형태로 디코딩
        visualizations = {
            'segmentation': self.decode_seg(visual_tokens.seg),
            'depth': self.decode_depth(visual_tokens.depth),
            'edge': self.decode_edge(visual_tokens.edge),
            'semantic': self.decode_semantic(visual_tokens.sem)
        }
        
        # 3. 추론 과정 설명
        explanation = """
        1. 먼저 객체를 분할했습니다 (Segmentation)
        2. 깊이 정보로 앞뒤 관계를 파악했습니다 (Depth)
        3. 윤곽선으로 형태를 확인했습니다 (Edge)
        4. 의미적으로 '사과'임을 인식했습니다 (Semantic)
        """
        
        return visualizations, explanation
```
{: .nolineno }

> **👁️ 투명한 사고 과정**  
> 모델이 "이 물체가 앞에 있으니(Depth), 이것을 가리켜야겠다(Mask)"라고 판단하는 과정을 **눈으로 확인**할 수 있다는 뜻입니다.
{: .prompt-tip }

---

### 2. 외부 도구가 필요 없는 효율성 (Self-Contained)
```text
학습 단계 (무거움):
├── SAM 모델 로드
├── DepthAnything 로드
├── PIDINet 로드
├── DINOv2 로드
└── 지식 증류

추론 단계 (가벼움):
├── VLM만 로드
├── 시각 토큰 생성 (내재된 지식)
└── 선택적 디코딩 (필요시만)
```
{: .nolineno }

실제 **Inference 단계에서는 무거운 비전 모델들을 로드할 필요가 없습니다**.

| 단계 | 필요 모델 | 메모리 사용량 | 추론 속도 |
|:---|:---|:---:|:---:|
| **학습** | 5개 모델 (VLM + 4 전문가) | 높음 | 느림 |
| **추론** | 1개 모델 (VLM만) | 낮음 | 빠름 |

VLM은 학습된 가중치만으로 연속적인 시각 토큰 공간에서 가볍게 추론을 수행합니다. 시각화가 필요한 순간에만 선택적으로 디코딩하면 되므로 **연산 효율이 매우 뛰어납니다**.

---

### 3. 확실한 성능 향상

CoVT는 **CV-Bench, MMVP, RealWorldQA** 등 주요 벤치마크에서 Qwen2.5-VL 등 기존 모델을 상회하는 성능을 입증했습니다.

#### 벤치마크 성능

| 벤치마크 | 기존 SOTA | CoVT | 개선 |
|:---|:---:|:---:|:---:|
| **CV-Bench** | 75.2% | 78.9% | +3.7% |
| **MMVP** | 68.5% | 73.1% | +4.6% |
| **RealWorldQA** | 71.3% | 76.8% | +5.5% |
| **Counting Tasks** | 62.1% | 79.4% | +17.3% |
| **Depth Estimation** | 58.7% | 74.2% | +15.5% |

특히 **깊이(Depth) 추정이나 개수 세기(Counting)** 처럼 텍스트만으로는 한계가 있던 세밀한 시각 작업에서 괄목할 만한 성과를 보였습니다.
```text
작업별 성능 향상:

텍스트 중심 작업 (질문 응답)
└── 소폭 개선 (~3%)

시각 중심 작업:
├── Counting: +17.3% ⭐
├── Depth: +15.5% ⭐
├── Spatial Relations: +12.8%
└── Fine-grained Recognition: +9.4%
```
{: .nolineno }

> **📈 시각 작업의 혁신**  
> CoVT는 특히 공간적 추론이 필요한 작업에서 기존 모델 대비 10-17% 성능 향상을 달성했습니다.
{: .prompt-info }

---

## 🎓 5. 결론

Chain-of-Visual-Thought는 VLM이 텍스트라는 이산적(Discrete) 상징의 한계를 넘어, **이미지의 물리적·공간적 특성을 '마음속으로 시뮬레이션(Mental Imagery)'하며 추론하는 단계**로 진화했음을 보여줍니다.

### 핵심 성과 요약
```text
CoVT의 혁신:

기술적 측면:
├── 연속적 시각 토큰 생성
├── 4가지 시각 능력 내재화
├── 해석 가능한 추론 과정
└── 효율적인 단일 모델 추론

성능적 측면:
├── 주요 벤치마크 SOTA 달성
├── 시각 중심 작업 대폭 개선
└── 일반화 성능 향상
```
{: .nolineno }

| 측면 | 혁신 내용 | 의의 |
|:---|:---|:---|
| **개념** | 시각적 사고 | 텍스트 병목 제거 |
| **구현** | 4가지 시각 토큰 | 인간 인지 모방 |
| **학습** | 4단계 커리큘럼 | 효과적 지식 전이 |
| **추론** | 단일 모델 | 실용적 배포 |

---

### 미래 전망

연속적(Continuous)인 시각 토큰을 사고의 도구로 내재화했다는 점은, 향후 **진정한 의미의 멀티모달 AGI를 향한 연구**에 중요한 이정표가 될 것입니다.
```text
연구의 확장 가능성:

현재 (CoVT):
└── Vision + Language

미래:
├── Vision + Language + Audio
├── Vision + Language + Tactile
└── 완전한 멀티모달 추론
```
{: .nolineno }

> **🚀 패러다임 전환**  
> CoVT는 AI가 "말로 설명하는" 것이 아니라 "시각적으로 생각하는" 새로운 패러다임을 제시했습니다.
{: .prompt-tip }

---

## 📊 기술 비교

### CoVT vs 기존 VLM

| 특성 | 기존 VLM | CoVT |
|:---|:---|:---|
| **추론 방식** | 텍스트 CoT | 시각 + 텍스트 CoT |
| **정보 표현** | 이산적 (Discrete) | 연속적 (Continuous) |
| **전문가 모델** | 추론 시 호출 | 학습 시만 사용 |
| **해석 가능성** | 낮음 | 높음 (시각화 가능) |
| **효율성** | 낮음 (다중 모델) | 높음 (단일 모델) |
| **시각 작업 성능** | 제한적 | 우수 |

### 주요 장점 재정리

| 장점 | 설명 | 영향 |
|:---|:---|:---|
| 🔍 **투명성** | 추론 과정 시각화 | 디버깅 용이, 신뢰성 향상 |
| ⚡ **효율성** | 단일 모델 추론 | 배포 비용 절감 |
| 📈 **성능** | 시각 작업 대폭 개선 | 실용적 응용 확대 |
| 🧠 **일반화** | 다양한 시각 능력 통합 | 범용성 증가 |

---

## 📚 참고 자료

- Qin et al., "Chain-of-Visual-Thought: Teaching VLMs to See and Think Better with Continuous Visual Tokens", arXiv:2511.19418, 2025
- [논문 링크](https://arxiv.org/abs/2511.19418)
- [SAM - Segment Anything Model](https://segment-anything.com/)
- [DepthAnything v2](https://depth-anything-v2.github.io/)
- [PIDINet](https://github.com/hellozhuo/pidinet)
- [DINOv2](https://github.com/facebookresearch/dinov2)