---
title: "Chain-of-Visual-Thought (CoVT) 기술 분석"
date: 2025-12-01 10:24:34 +0900
categories: [AI/ML, Computer Vision]
tags: [vlm, chain-of-thought, computer vision, multimodal, visual reasoning, covt]
author: j-ho
img_path: /assets/img/for_post/
pin: false
description: Vision-Language Model이 시각적으로 사고하도록 만드는 CoVT 프레임워크를 분석합니다.
---

> 이 글은 UC Berkeley와 UCLA 연구진이 발표한 논문 "Chain-of-Visual-Thought: Teaching VLMs to See and Think Better with Continuous Visual Tokens"를 토대로 작성되었습니다.
{: .prompt-info }

---

Chain-of-Thought(CoT)는 LLM의 추론 능력을 크게 개선한 기법이죠. 복잡한 문제를 단계별로 쪼개어 해결하는 방식인데, Vision-Language Model(VLM)에서는 한계가 있었습니다.

"사과가 몇 개지?", "책상 뒤에 가려진 건 뭐지?" 같은 시각적 인식 문제를 풀 때, 텍스트만으로는 이미지의 공간적/기하학적 정보를 담아내기 어렵기 때문입니다.

![CoVT 프레임워크](2025-12-01-image1.jpg)
_Chain-of-Visual-Thought 프레임워크 개요_

이 논문은 텍스트뿐만 아니라 연속적인 시각 토큰(Continuous Visual Tokens)을 활용해 모델이 시각적으로 사고하게 만드는 CoVT 프레임워크를 제안합니다.

---

## 1. 문제: 언어 병목 현상

기존 VLM의 CoT 방식은 시각 정보를 텍스트 공간에 억지로 끼워 맞추는 식이었습니다. 물체의 위치 관계를 파악할 때 "A는 왼쪽에, B는 뒤에 있다"라고 텍스트로 먼저 변환한 뒤 추론을 시작합니다.

이 과정에서 언어 병목(Language Bottleneck)이 발생합니다. 이미지의 엣지, 깊이, 세밀한 분할 정보는 텍스트로 온전히 표현하기 힘듭니다. 또한 텍스트 변환 과정에서 시각 정보를 잘못 해석하면, 이후 논리가 정교해도 오답을 내게 됩니다.

CoVT는 추론 과정에서 텍스트 토큰과 함께 시각 정보를 담은 토큰을 생성하는 방식으로 이 문제를 해결합니다.

---

## 2. 핵심 원리: 연속적 시각 토큰

CoVT의 핵심은 추론 과정에서 생성되는 토큰이 단순한 텍스트가 아닌 압축된 시각적 잠재 표현이라는 점입니다.

연구진은 인간의 시각 인지 과정을 모방해 4가지 시각 능력을 정의했습니다:

1. **Segmentation Tokens**: 물체가 어디에 있고 어떤 모양인지 (교사 모델: SAM)
2. **Depth Tokens**: 픽셀 단위의 원근감과 깊이 정보 (교사 모델: DepthAnything v2)
3. **Edge Tokens**: 물체의 경계선과 구조적 단서 (교사 모델: PIDINet)
4. **Semantic Tokens**: 패치 수준의 의미론적 특징 (교사 모델: DINOv2)

VLM은 이 4가지 유형의 시각 토큰을 순차적으로 예측하도록 학습합니다. 학습할 때는 4개의 전문가 모델을 사용하지만, 추론할 때는 VLM만으로 시각 토큰을 생성합니다. 외부 모델 없이도 시각적 사고가 가능해집니다.

---

## 3. 학습 파이프라인

CoVT는 학습 단계에서 외부 전문가 모델의 능력을 VLM 파라미터 안에 녹여내는 방식을 택했습니다. "Think → Decode → Reconstruct" 구조입니다.

### 정렬 전략

전문가 모델마다 다른 학습 방식을 적용했습니다:

- **Task-Oriented Alignment**: SAM이나 DepthAnything처럼 결과물의 디테일이 중요한 경우, VLM이 생성한 토큰을 Decoder 프롬프트로 활용해 최종 결과물(마스크, 깊이 맵)을 만들고 정답 데이터와 비교합니다.
- **Feature Alignment**: DINO처럼 표현 학습이 핵심인 모델은 특징 벡터 공간에서의 유사도를 좁히는 방식으로 학습합니다.

### 4단계 커리큘럼

1. **Comprehension**: 시각 토큰이 무엇을 의미하는지 배우는 기초 단계
2. **Generation**: 주어진 이미지에 맞는 정확한 시각 토큰을 생성하도록 훈련
3. **Reasoning**: 질문에 답하는 과정에 시각 토큰을 자연스럽게 섞어 쓰도록 학습
4. **Efficient Reasoning**: 시각 토큰 일부를 무작위로 제거해도 강건하게 추론하도록 학습

---

## 4. 기술적 강점

### 해석 가능한 추론

기존 Latent Reasoning 모델들은 내부 동작이 블랙박스에 가까웠습니다. CoVT는 생성된 시각 토큰을 디코더에 통과시켜 사람이 직관적으로 볼 수 있는 이미지(Segmentation Mask, Depth Map 등)로 복원해 줍니다. 모델이 어떤 과정을 거쳐 판단했는지 눈으로 확인할 수 있습니다.

### 추론 효율성

학습할 때는 5개 모델(VLM + 4 전문가)을 사용하지만, 추론할 때는 VLM 하나만 로드하면 됩니다. 시각화가 필요한 순간에만 선택적으로 디코딩하므로 연산 효율이 좋습니다.

### 벤치마크 성능

| 벤치마크 | 기존 SOTA | CoVT | 개선 |
|:---|:---:|:---:|:---:|
| CV-Bench | 75.2% | 78.9% | +3.7% |
| MMVP | 68.5% | 73.1% | +4.6% |
| RealWorldQA | 71.3% | 76.8% | +5.5% |
| Counting Tasks | 62.1% | 79.4% | +17.3% |
| Depth Estimation | 58.7% | 74.2% | +15.5% |

특히 깊이 추정이나 개수 세기처럼 텍스트만으로는 한계가 있던 시각 작업에서 10-17%의 성능 향상을 보였습니다.

---

## 5. 정리

CoVT는 VLM이 텍스트라는 이산적 상징의 한계를 넘어, 이미지의 물리적/공간적 특성을 시뮬레이션하며 추론하는 단계로 진화했음을 보여주죠.

핵심 기여는 다음과 같습니다.
- 연속적 시각 토큰으로 텍스트 병목 제거
- 4가지 시각 능력을 단일 VLM에 내재화
- 해석 가능한 추론 과정
- 추론 시 외부 모델 불필요

연속적인 시각 토큰을 사고의 도구로 내재화했다는 점은 멀티모달 AI 연구에서 의미 있는 진전입니다.

---

## 참고 자료

- Qin et al., "Chain-of-Visual-Thought: Teaching VLMs to See and Think Better with Continuous Visual Tokens", arXiv:2511.19418, 2025
- [논문 링크](https://arxiv.org/abs/2511.19418)
- [SAM](https://segment-anything.com/)
- [DepthAnything v2](https://depth-anything-v2.github.io/)
- [PIDINet](https://github.com/hellozhuo/pidinet)
- [DINOv2](https://github.com/facebookresearch/dinov2)
