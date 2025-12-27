---
title: Terraform으로 AWS 인프라 구축하기
date: 2023-11-26 16:00:00 +0900
categories: [ENGINEERING,DEVOPS, IaC]
tags: [terraform, iac, aws, infrastructure, automation]
author: j-ho
img_path: /assets/img/for_post/
description: Terraform을 사용하여 AWS 인프라를 코드로 관리하고, EC2부터 Load Balancer, Route53까지 자동화하는 방법을 알아봅니다.
---

요즘 `DevOps`를 논할 때 빠질 수 없는 용어가 있습니다. 바로 **IaC(Infrastructure as Code)**입니다.

수동으로 인프라를 구축하는 것이 아닌 코드를 통해 인프라를 생성하고 관리하는 것을 말합니다.

IaC를 사용하면 인프라 사양을 담은 구성 파일이 생성되므로 구성을 편집하고 배포하기가 더 쉬워집니다. 또한 IaC는 매번 동일한 환경을 `프로비저닝`하도록 보장합니다.

IaC를 사용하면 버전 관리, 재사용, 공유할 수 있는 리소스 구성을 정의하여 안전하고 일관되게 인프라를 구축, 변경, 관리할 수 있습니다.

그중 가장 많이 쓰는 도구로 하시코프(HashiCorp)에서 개발중인 `테라폼(Terraform)`이 있습니다.

[Terraform](https://developer.hashicorp.com/terraform/docs)의 경우 AWS, GCP, Azure와 같은 주요 클라우드 서비스를 비롯한 다양한 서비스를 프로바이더 방식으로 제공하고 있습니다. 이를 통해 테라폼만으로 멀티 클라우드의 리소스들을 선언하고 관리하는 것도 가능합니다.

이번에는 Terraform을 이용하여 AWS 인프라를 간단하게 구축해보도록 하겠습니다.

> **전제 조건:** 키 페어와 Load Balancer는 이미 존재한다고 가정합니다.
{: .prompt-info }

**구축 순서:**
1. EC2 생성
2. 타겟 그룹 생성
3. LB Rule 추가 후 타겟 그룹 매칭
4. Route53 생성 후 LB 매칭

## Terraform 설치

### Homebrew 사용

Homebrew를 사용하면 손쉽게 최신 버전을 다운받으실 수 있습니다.
```bash
brew install terraform

terraform version
# Terraform v1.6.4
```

### tfenv 사용 (권장)

여러 버전을 사용하는 경우 테라폼 버전 관리 도구를 사용하여 설치합니다. (Node 진영의 nvm과 유사)
```bash
brew install tfenv

# terraform 1.6.4 설치
tfenv install 1.6.4

terraform version
# Terraform v1.6.4
```

> **주의:** tfenv와 terraform을 동시에 설치하면 에러가 종종 발생하므로 둘 중 하나만 설치를 권장합니다.
{: .prompt-warning }

## 프로젝트 설정

### 폴더 구조 생성

폴더를 하나 생성 후 `provider.tf` 파일을 추가해줍니다.
```bash
mkdir aws_infra
cd aws_infra
touch provider.tf
```

> 디렉터리 이름과 파일 이름에 특별한 원칙은 없습니다. Terraform은 디렉터리 내의 모든 `.tf` 파일을 전부 읽어들인 후, 리소스 생성, 수정, 삭제 작업을 진행합니다.
{: .prompt-tip }

### Provider 정의

AWS의 접근 키를 프로바이더에 등록합니다. 하지만 민감한 정보를 저장소에 기록하면 보안 문제가 발생할 수 있으므로 환경변수로 등록 후 사용하는 것을 권장합니다.

**환경 변수 설정:**
```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
export AWS_DEFAULT_REGION="ap-northeast-2"
```

**provider.tf:**
```hcl
provider "aws" {}
```

> 환경 변수가 설정되어 있으면 Terraform이 자동으로 인식합니다.
{: .prompt-info }

## 기본 개념

이해를 돕기 위한 Terraform 핵심 개념입니다.

### 프로비저닝(Provisioning)

어떤 프로세스나 서비스를 실행하기 위한 준비 단계를 뜻합니다. 크게 네트워크나 컴퓨팅 자원을 준비하는 작업과 준비된 컴퓨팅 자원에 사이트 패키지나 애플리케이션 의존성을 준비하는 단계로 나뉩니다. Terraform은 주로 전자를 다룹니다.

### 프로바이더(Provider)

Terraform과 외부 서비스를 연결해주는 기능을 하는 모듈입니다. 예를 들어 Terraform으로 AWS 서비스의 컴퓨팅 자원을 생성하기 위해서는 AWS 프로바이더를 먼저 설정해야 합니다.

### 리소스(Resource)

특정 프로바이더가 제공해주는 조작 가능한 대상의 최소 단위입니다. 예를 들어 AWS 프로바이더는 `aws_instance` 리소스 타입을 제공하고, 이 리소스 타입을 사용하여 EC2의 리소스를 선언하고 조작하는 것이 가능합니다.

### HCL(HashiCorp Configuration Language)

Terraform에서 사용하는 설정 언어입니다. Terraform의 모든 설정과 선언은 HCL을 사용해 이루어집니다. 확장자는 `.tf`입니다.

### Plan

디렉터리 내의 모든 `.tf` 파일의 내용을 실제로 적용 가능한지 확인하는 작업을 plan이라고 합니다. `terraform plan` 명령어를 실행하면 어떤 리소스가 생성, 수정, 삭제될지 계획을 보여줍니다.

### Apply

디렉터리 내의 모든 `.tf` 파일의 내용대로 리소스를 생성, 수정, 삭제하는 일을 apply라고 합니다. `terraform apply` 명령어로 실행합니다.

## Terraform 초기화

프로바이더 설정이 완료되었으니 Terraform을 초기화하겠습니다. 초기화 시 Terraform은 프로바이더 설정을 참고하여 필요한 플러그인을 설치합니다.
```bash
terraform init
```

![2023-11-26-image1](2023-11-26-image1.png)
_Terraform 초기화 완료_

Terraform 버전을 확인하면 현재 Terraform 버전과 사용하고 있는 프로바이더 버전을 확인하실 수 있습니다.
```bash
terraform version
```

![2023-11-26-image2](2023-11-26-image2.png)
_Terraform 및 Provider 버전 확인_

## Security Group 생성

인스턴스를 생성해도 외부에서 접근할 수 없다면 그 인스턴스는 사용할 수 없습니다. 기본적으로 `22번 포트(SSH)`를 열어주는 Security Group을 먼저 생성하겠습니다.

`main.tf` 파일을 생성하고 아래와 같이 입력합니다.
```hcl
resource "aws_security_group" "sg" {
  name        = "allow_ssh_from_all"
  description = "Allow SSH from all"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

> `egress` 속성도 추가하여 아웃바운드 규칙을 설정할 수 있습니다.
{: .prompt-tip }

입력을 완료하셨다면 이제 `plan`을 실행해봅니다. 하나의 Security Group이 추가될 예정임을 확인할 수 있습니다.

![2023-11-26-image3](2023-11-26-image3.png)
_Terraform Plan 결과_

이제 위의 plan을 적용합니다. AWS Console에서 확인해보면 Security Group이 생성되어 있는 것을 확인하실 수 있습니다.
```bash
terraform apply
```

![2023-11-26-image4](2023-11-26-image4.png)
_Terraform Apply 완료_

### 기존 Security Group 참조

보안 그룹이 이미 존재한다면 `aws_security_group` 데이터 소스를 사용해 가져올 수도 있습니다.
```hcl
data "aws_security_group" "sg" {
  name = "allow_ssh_from_all"
}
```

## EC2 인스턴스 생성

이제 인스턴스를 정의해보겠습니다. 리소스 타입은 `aws_instance`입니다.
```hcl
resource "aws_instance" "this" {
  ami           = "ami-06d88f849af021b38"
  instance_type = "t2.micro"
  key_name      = var.key_name

  tags = {
    Name = "EC2 NAME"
  }

  vpc_security_group_ids = [
    data.aws_security_group.sg.id
  ]
}
```

리소스의 이름을 `this`로 지정했습니다. 인스턴스 생성 후 반환되는 id, public_ip, private_ip 등을 `aws_instance.this.id` 형식으로 가져올 수 있습니다.

### Plan 실행
```bash
terraform plan
```
```
data.aws_security_group.sg: Reading...
data.aws_security_group.sg: Read complete after 0s [id=sg-0a5bab6b1b735815b]

Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_instance.this will be created
  + resource "aws_instance" "this" {
      + ami                          = "ami-06311c5f6a3951ada"
      + arn                          = (known after apply)
      + associate_public_ip_address  = (known after apply)
      ...
      + vpc_security_group_ids       = [
          + "sg-0a5bab6b1b735815b",
        ]
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

### Apply 실행
```bash
terraform apply
```
```
aws_instance.this: Creating...
aws_instance.this: Still creating... [10s elapsed]
aws_instance.this: Still creating... [20s elapsed]
aws_instance.this: Still creating... [30s elapsed]
aws_instance.this: Creation complete after 31s [id=i-091eb4dfeef5c01ca]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

> EC2 생성은 20초 ~ 1분 정도의 시간이 소요됩니다.
{: .prompt-info }

### 리소스 정보 확인

`terraform console`을 통해 생성된 인스턴스의 id, public_ip 등의 정보를 확인할 수도 있습니다.

![2023-11-26-image6](2023-11-26-image6.png)
_Terraform Console에서 리소스 정보 확인_

## Target Group 생성

### Target Group 리소스 생성

이어서 `main.tf`에 Target Group 리소스를 추가하겠습니다.
```hcl
resource "aws_lb_target_group" "target_group_client" {
  name            = format("%s-%s", aws_instance.this.id, "example")
  depends_on      = [aws_instance.this]
  port            = var.target_port
  ip_address_type = "ipv4"
  protocol        = "HTTP"
  vpc_id          = var.vpc_id
  target_type     = "instance"
}
```

`format`은 두 문자열을 합치는 함수입니다. `%s-%s`는 두 문자열을 하이픈으로 합칩니다.

### Variables 정의

`var`는 `variable`로 `variables.tf`를 생성하여 선언해줍니다.
```hcl
variable "vpc_id" {
  description = "value of vpc"
  default     = "vpc-67ae5f0c"
  type        = string
}

variable "target_port" {
  description = "Target port for load balancer"
  default     = 80
  type        = number
}

variable "key_name" {
  description = "EC2 key pair name"
  type        = string
}
```

### Target Group Attachment

생성한 Target Group에 인스턴스를 참조합니다.
```hcl
resource "aws_lb_target_group_attachment" "target_group_attach" {
  target_group_arn = aws_lb_target_group.target_group_client.arn
  target_id        = aws_instance.this.id
  port             = var.target_port
}
```

## Load Balancer 설정

Security Group 섹션에서 이미 존재하는 Security Group을 가져온 것처럼 Load Balancer도 데이터 소스로 가져옵니다.

### Load Balancer 참조
```hcl
data "aws_lb" "this_lb" {
  name = var.lb_name
}
```

### Listener 참조 (SSL/TLS)

`SSL/TLS 인증서`가 있다면 추가로 필터링을 거친 후 가져올 수 있습니다.
```hcl
data "aws_lb_listener" "this_lb443" {
  load_balancer_arn = data.aws_lb.this_lb.arn
  port              = 443
}
```

### Listener Rule 추가
```hcl
resource "aws_lb_listener_rule" "rule" {
  listener_arn = data.aws_lb_listener.this_lb443.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target_group_client.arn
  }
  
  condition {
    host_header {
      values = ["${var.sub_domain}.${var.domain_name}"]
    }
  }
}
```

## Route53 설정

마지막으로 Route53의 Record를 추가해줍니다.

### Hosted Zone 참조
```hcl
data "aws_route53_zone" "route53" {
  name         = var.domain_name
  private_zone = false
}
```

### DNS Record 생성
```hcl
resource "aws_route53_record" "www" {
  zone_id = data.aws_route53_zone.route53.zone_id
  name    = "${var.sub_domain}.${var.domain_name}"
  type    = "A"
  
  alias {
    name                   = data.aws_lb.this_lb.dns_name
    zone_id                = data.aws_lb.this_lb.zone_id
    evaluate_target_health = true
  }
}
```

## 정리

Terraform을 활용한 AWS 인프라 구축 프로세스:

### 전체 워크플로우
```
1. Terraform 설치 및 초기화
   ↓
2. Provider 설정 (AWS)
   ↓
3. Security Group 생성
   ↓
4. EC2 인스턴스 생성
   ↓
5. Target Group 생성 및 연결
   ↓
6. Load Balancer Rule 추가
   ↓
7. Route53 DNS 레코드 생성
```

### 주요 리소스 구조

| 리소스 | 타입 | 용도 |
|:---|:---|:---|
| **Security Group** | aws_security_group | 방화벽 규칙 |
| **EC2** | aws_instance | 컴퓨팅 인스턴스 |
| **Target Group** | aws_lb_target_group | LB 타겟 관리 |
| **LB Listener Rule** | aws_lb_listener_rule | 라우팅 규칙 |
| **Route53 Record** | aws_route53_record | DNS 레코드 |

### Terraform 핵심 명령어
```bash
# 초기화
terraform init

# 계획 확인
terraform plan

# 적용
terraform apply

# 리소스 확인
terraform show

# 콘솔 접속
terraform console

# 리소스 삭제
terraform destroy
```

### IaC의 장점

테라폼을 사용해본 결과, 장점이 확실한 도구였습니다:

**자동화:**
- 하나하나 AWS Console에서 설정하던 것에 비해 빠르게 인프라 구축
- 반복 작업 제거

**일관성:**
- 동일한 환경을 매번 재현 가능
- 실수 감소

**버전 관리:**
- Git을 통한 인프라 변경 이력 추적
- 협업 용이

**재사용성:**
- Module화를 통한 코드 재사용
- 여러 환경(dev, staging, prod) 동일 구성 적용

### 모범 사례

**State 관리:**
```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "ap-northeast-2"
  }
}
```

**변수 파일 분리:**
```bash
# terraform.tfvars
vpc_id      = "vpc-67ae5f0c"
target_port = 80
key_name    = "my-keypair"
```

**민감 정보 관리:**
- 환경 변수 사용
- AWS Secrets Manager 활용
- `.gitignore`에 `*.tfvars` 추가

### 주의사항

**보안:**
- Access Key를 코드에 하드코딩하지 말 것
- State 파일에는 민감 정보가 포함되므로 S3 + 암호화 사용
- IAM 최소 권한 원칙 적용

**운영:**
- `terraform plan`으로 항상 사전 확인
- 프로덕션에서는 `terraform apply` 자동 승인 금지
- State 파일 백업 필수

**협업:**
- Remote State 사용 (S3, Terraform Cloud)
- State Locking 설정 (DynamoDB)
- 코드 리뷰 프로세스 수립

전체 코드는 [GitHub 저장소](https://github.com/awesomelon/simple-aws-terraform)를 확인해주세요.