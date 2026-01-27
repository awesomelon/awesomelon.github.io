---
title: Terraform으로 AWS 인프라 구축하기
date: 2023-11-26 16:00:00 +0900
categories: [ENGINEERING, DEVOPS, IaC]
tags: [terraform, iac, aws, infrastructure, automation]
author: j-ho
img_path: /assets/img/for_post/
description: Terraform을 사용하여 AWS 인프라를 코드로 관리하고, EC2부터 Load Balancer, Route53까지 자동화하는 방법을 알아봅니다.
---

IaC(Infrastructure as Code)는 수동으로 인프라를 구축하는 것이 아닌 코드를 통해 인프라를 생성하고 관리하는 방법입니다. 버전 관리, 재사용, 공유할 수 있는 리소스 구성을 정의하여 안전하고 일관되게 인프라를 구축, 변경, 관리할 수 있습니다.

그중 가장 많이 쓰는 도구로 HashiCorp에서 개발중인 Terraform이 있습니다. AWS, GCP, Azure와 같은 주요 클라우드 서비스를 프로바이더 방식으로 제공하고 있어 멀티 클라우드 리소스를 선언하고 관리하는 것도 가능합니다.

> 전제 조건: 키 페어와 Load Balancer는 이미 존재한다고 가정합니다.
{: .prompt-info }

**구축 순서:** EC2 생성 → 타겟 그룹 생성 → LB Rule 추가 후 타겟 그룹 매칭 → Route53 생성 후 LB 매칭

---

## Terraform 설치

Homebrew를 사용하면 손쉽게 설치할 수 있습니다.

```bash
brew install terraform
terraform version
```

여러 버전을 사용하는 경우 tfenv를 권장합니다.

```bash
brew install tfenv
tfenv install 1.6.4
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

AWS 접근 키는 환경변수로 등록 후 사용하는 것을 권장합니다.

```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
export AWS_DEFAULT_REGION="ap-northeast-2"
```

provider.tf에는 간단히 아래와 같이 작성합니다.

```hcl
provider "aws" {}
```

Terraform을 초기화합니다.

```bash
terraform init
```

![2023-11-26-image1](2023-11-26-image1.png)
_Terraform 초기화 완료_

---

## Security Group 생성

main.tf 파일을 생성하고 22번 포트(SSH)를 열어주는 Security Group을 정의합니다.

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

plan을 실행하여 생성될 리소스를 확인합니다.

```bash
terraform plan
```

![2023-11-26-image3](2023-11-26-image3.png)
_Terraform Plan 결과_

적용합니다.

```bash
terraform apply
```

![2023-11-26-image4](2023-11-26-image4.png)
_Terraform Apply 완료_

---

## EC2 인스턴스 생성

```hcl
data "aws_security_group" "sg" {
  name = "allow_ssh_from_all"
}

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

![2023-11-26-image6](2023-11-26-image6.png)
_Terraform Console에서 리소스 정보 확인_

---

## Target Group 생성

variables.tf에 변수를 정의합니다.

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

main.tf에 Target Group 리소스를 추가합니다.

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

## 모범 사례

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

**주의사항:**
- Access Key를 코드에 하드코딩하지 말 것
- State 파일에는 민감 정보가 포함되므로 S3 + 암호화 사용
- `terraform plan`으로 항상 사전 확인
- Remote State 사용 시 State Locking 설정 (DynamoDB)

전체 코드는 [GitHub 저장소](https://github.com/awesomelon/simple-aws-terraform)를 확인해주세요.
