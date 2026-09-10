---
title: Terraform으로 AWS 인프라 구축하기
date: 2023-11-26 16:00:00 +0900
categories: [ENGINEERING, DEVOPS, IaC]
tags: [terraform, iac, aws, infrastructure, automation]
author: j-ho
img_path: /assets/img/for_post/
description: Terraform으로 AWS 인프라를 코드로 관리하고 EC2, Load Balancer, Route53을 구성한 과정을 정리합니다.
---

IaC(Infrastructure as Code)는 콘솔에서 수동으로 인프라를 만드는 대신 코드로 인프라를 생성하고 관리하는 방식이에요. 리소스 구성을 버전 관리할 수 있고 같은 구성을 다시 쓰거나 공유하기도 쉽습니다.

대표적인 도구로 HashiCorp에서 개발 중인 Terraform이 있습니다. AWS, GCP, Azure와 같은 주요 클라우드 서비스를 프로바이더 방식으로 지원하고 있어 멀티 클라우드 리소스를 선언하고 관리하는 것도 가능합니다.

> 전제 조건: 키 페어, VPC와 서브넷, HTTPS 443 리스너가 설정된 Application Load Balancer, 도메인의 퍼블릭 Route53 Hosted Zone이 이미 존재한다고 가정합니다. EC2와 타겟 그룹은 같은 VPC를 사용하며, EC2에서 애플리케이션을 설치·실행하는 과정은 이 예시에 포함하지 않습니다.
{: .prompt-info }

**구축 순서:** EC2 생성 → 타겟 그룹 생성 → LB Rule 추가 후 타겟 그룹 매칭 → Route53 생성 후 LB 매칭

---

## Terraform 설치

아래는 2023년 당시 Homebrew 설치 예시입니다. 새로운 환경에서는 [HashiCorp 공식 설치 안내](https://developer.hashicorp.com/terraform/install)의 저장소와 지원 버전을 확인해주세요.

```bash
brew install terraform
terraform version
```

여러 버전을 사용하는 경우 tfenv를 권장해요.

```bash
brew install tfenv
tfenv install 1.6.4
tfenv use 1.6.4
```

> tfenv와 terraform을 동시에 설치하면 에러가 발생할 수 있으므로 둘 중 하나만 설치하세요.
{: .prompt-warning }

---

## 프로젝트 설정

폴더를 생성하고 provider.tf 파일을 추가합니다.

```bash
mkdir aws_infra && cd aws_infra
touch provider.tf
```

AWS 접근 키는 환경변수로 등록 후 사용하는 것을 권장해요.

```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
export AWS_DEFAULT_REGION="ap-northeast-2"
```

provider.tf에는 간단히 아래와 같이 작성합니다.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {}
```

Terraform을 초기화해요.

```bash
terraform init
```

![2023-11-26-image1](2023-11-26-image1.png)
_Terraform 초기화 완료_

---

## Security Group 생성

main.tf 파일을 생성하고 SSH와 ALB에서 오는 애플리케이션 트래픽을 허용하는 Security Group을 정의합니다. 아래에서 사용하는 변수는 뒤의 `variables.tf` 예시에 모두 정의합니다.

```hcl
resource "aws_security_group" "sg" {
  name        = "allow_ssh_and_alb"
  description = "Allow SSH from admin network and application traffic from ALB"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  ingress {
    from_port       = var.target_port
    to_port         = var.target_port
    protocol        = "tcp"
    security_groups = data.aws_lb.this_lb.security_groups
  }
}
```

ALB의 보안 그룹도 타겟 포트로 나가는 트래픽을 허용해야 합니다. 타겟 포트에서 애플리케이션이 실행되고 헬스 체크에 응답해야 정상 서비스가 가능해요. 위 예시에는 EC2의 아웃바운드 규칙이 없으므로 패키지 다운로드나 외부 API 접속이 필요하면 필요한 egress 규칙을 별도로 추가합니다.

뒤의 리소스와 변수 정의까지 작성하고 실제 환경 값을 입력한 뒤, plan을 실행하여 생성될 리소스를 확인합니다.

```bash
terraform plan
```

![2023-11-26-image3](2023-11-26-image3.png)
_Terraform Plan 결과_

적용해요.

```bash
terraform apply
```

![2023-11-26-image4](2023-11-26-image4.png)
_Terraform Apply 완료_

---

## EC2 인스턴스 생성

```hcl
resource "aws_instance" "this" {
  ami           = var.ami_id
  instance_type = "t2.micro"
  key_name      = var.key_name
  subnet_id     = var.subnet_id

  tags = {
    Name = "EC2 NAME"
  }

  vpc_security_group_ids = [
    aws_security_group.sg.id
  ]
}
```

![2023-11-26-image6](2023-11-26-image6.png)
_Terraform Console에서 리소스 정보 확인_

---

## Target Group 생성

variables.tf에 변수를 정의합니다.

```hcl
variable "vpc_id" {
  description = "value of vpc"
  type        = string
}

variable "subnet_id" {
  description = "Subnet in the target VPC"
  type        = string
}

variable "ami_id" {
  description = "AMI compatible with t2.micro in the selected region"
  type        = string
}

variable "admin_cidr" {
  description = "Allowed administrator or VPN IPv4 CIDR"
  type        = string
}

variable "lb_name" {
  description = "Existing Application Load Balancer name"
  type        = string
}

variable "domain_name" {
  description = "Existing public hosted zone domain"
  type        = string
}

variable "sub_domain" {
  description = "Subdomain to route to the application"
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

main.tf에 Target Group 리소스를 추가해요.

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

resource "aws_lb_target_group_attachment" "target_group_attach" {
  target_group_arn = aws_lb_target_group.target_group_client.arn
  target_id        = aws_instance.this.id
  port             = var.target_port
}
```

---

## Load Balancer 설정

기존 Load Balancer를 데이터 소스로 가져옵니다.

```hcl
data "aws_lb" "this_lb" {
  name = var.lb_name
}

data "aws_lb_listener" "this_lb443" {
  load_balancer_arn = data.aws_lb.this_lb.arn
  port              = 443
}

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

---

## Route53 설정

```hcl
data "aws_route53_zone" "route53" {
  name         = var.domain_name
  private_zone = false
}

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

---

## 핵심 명령어

```bash
terraform init      # 초기화
terraform plan      # 계획 확인
terraform apply     # 적용
terraform show      # 리소스 확인
terraform console   # 콘솔 접속
terraform destroy   # 리소스 삭제
```

---

## 운영 팁

**State 관리**

```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "ap-northeast-2"
  }
}
```

Access Key는 코드에 하드코딩하지 마세요. State 파일에는 민감 정보가 들어갈 수 있으므로 S3의 접근 권한과 암호화를 관리해야 합니다. 위 예시는 이미 생성된 S3 버킷을 사용하며 State Locking 설정은 포함하지 않습니다. 이 글에서 사용한 Terraform 1.6 계열에서는 DynamoDB 테이블과 `dynamodb_table` 설정으로 잠금을 구성할 수 있습니다. 이후 버전은 S3 잠금 파일도 지원하므로 새로 구성할 때는 해당 버전의 문서를 확인해주세요.

전체 코드는 [GitHub 저장소](https://github.com/awesomelon/simple-aws-terraform)를 확인해주세요.

## 참고 자료

- [AWS: ALB 보안 그룹과 타겟 접근](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-update-security-groups.html)
- [HashiCorp: S3 Backend와 State Locking](https://developer.hashicorp.com/terraform/language/backend/s3)
- [tfenv: 버전 설치와 선택](https://github.com/tfutils/tfenv)
