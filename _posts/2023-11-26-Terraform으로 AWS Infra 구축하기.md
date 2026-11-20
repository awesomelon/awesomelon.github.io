---
title: Terraform으로 AWS 인프라 구축하기
last_modified_at: 2026-09-12 13:38:07 +0900
date: 2023-11-26 16:00:00 +0900
categories: [ENGINEERING, DEVOPS, IaC]
tags: [terraform, iac, aws, infrastructure, automation]
author: j-ho
img_path: /assets/img/for_post/
description: Terraform으로 AWS 인프라를 코드로 관리하고 EC2, Load Balancer, Route53을 구성한 과정을 정리했다.
---

IaC(Infrastructure as Code)는 콘솔에서 수동으로 인프라를 만드는 대신 코드로 인프라를 생성하고 관리하는 방식이다. 리소스 구성을 버전 관리할 수 있고, 같은 구성을 다시 쓰거나 공유하기도 쉽다.

대표 도구로 HashiCorp에서 개발 중인 Terraform이 있다. AWS, GCP, Azure와 같은 주요 클라우드 서비스를 프로바이더 방식으로 지원하므로 멀티 클라우드 리소스도 선언하고 관리할 수 있다.

> 2023년에 Terraform 1.6.4와 AWS provider 5 계열로 진행했던 구성을 바탕으로, 기존 VPC·ALB에 서비스 하나를 연결하는 흐름을 정리했다. 이후 바뀐 S3 state 잠금 옵션은 글 마지막 운영 팁에 덧붙여 두었다.
{: .prompt-info }

**생성할 리소스:** EC2와 Security Group, Target Group·attachment, ALB listener rule, Route53 alias record.

**미리 준비할 리소스:** 같은 리전의 VPC·서브넷·키 페어, 해당 VPC의 internet-facing ALB, 대상 도메인을 포함하는 인증서가 연결된 HTTPS 443 listener, 올바르게 위임된 public Route53 Hosted Zone이 있어야 한다. listener priority는 기존 규칙과 겹치지 않아야 한다.

**사전 조건**

- EC2를 배치할 서브넷의 가용 영역(AZ)은 기존 ALB에서 활성화된 영역과 맞아야 한다. 같은 VPC여도 이 조건이 맞지 않으면 대상 등록 후 `Target.NotInUse` 상태로 남아 트래픽을 받지 못한다([AWS의 대상 상태 설명](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/check-target-health.html)).
- EC2에 애플리케이션을 설치·실행하는 과정은 따로 다루지 않는다. 준비된 AMI를 쓰거나 별도로 띄워 target port와 `/health`가 응답하도록 맞춰 둔다.
- EC2에 SSH로 접속하려면 VPN이나 bastion 등 해당 서브넷으로 접근할 수 있는 경로가 필요하다.
- 이 예시는 단일 EC2 구성이라 고가용성 환경으로 쓰려면 별도로 확장해야 한다.

리소스를 한 개씩 `apply`하는 대신 파일을 모두 작성하고 전체 plan을 확인한다. Terraform은 파일에 적힌 순서가 아니라 참조 관계로 의존성을 계산한다.

---

## Terraform 설치

새로운 macOS 환경에서는 아래 [HashiCorp 공식 Homebrew 설치 경로](https://developer.hashicorp.com/terraform/install)를 사용할 수 있다. 본문의 1.6 예시와 다른 최신 CLI가 설치될 수 있으므로, 기존 프로젝트에서는 팀이 정한 버전을 선택한다.

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
terraform version
```

당시 쓰던 1.6.4 동작을 그대로 맞춰보고 싶다면 tfenv 같은 버전 관리 도구로 해당 버전을 선택해 쓸 수 있다.

```bash
brew install tfenv
tfenv install 1.6.4
tfenv use 1.6.4
```

> tfenv와 terraform을 동시에 설치하면 에러가 발생할 수 있으므로 둘 중 하나만 설치한다.
{: .prompt-warning }

---

## 프로젝트 설정

폴더를 생성하고 provider.tf 파일을 만든다.

```bash
mkdir aws_infra && cd aws_infra
touch provider.tf
```

자격 증명은 코드에 직접 넣지 않는다. 팀이 IAM Identity Center를 사용한다면 [AWS CLI의 SSO 인증](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html) 안내에 따라 `aws configure sso --profile blog-infra`로 초기 설정을 마쳐 두고 로그인하면 편하다. 아래는 그 설정을 마쳤다고 가정한 예시다.

```bash
aws sso login --profile blog-infra
export AWS_PROFILE=blog-infra
export AWS_DEFAULT_REGION=ap-northeast-2
aws sts get-caller-identity
```

출력에 나타난 AWS 계정과 역할이 의도한 대상인지 확인한다. SSO를 쓰지 않는 환경에서도 역할 기반 임시 자격 증명을 우선하고, 임시 키를 직접 주입한다면 session token까지 준비해야 한다. CI 인증은 사용하는 CI의 역할 연동 방식에 맞춰 별도로 구성한다.

`provider.tf`에는 예시의 버전 범위를 명시한다.

```hcl
terraform {
  required_version = ">= 1.6.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-northeast-2"
}
```

Terraform을 초기화한다. `~> 5.0`은 5.0만 고정한다는 뜻이 아니라 5.x 범위를 허용한다. 실제로 선택된 provider 버전은 `.terraform.lock.hcl`에 기록되며, 이 파일은 Git으로 관리한다. provider의 메이저 버전을 변경할 때는 별도로 plan을 검토한다.

```bash
terraform init
```

![2023-11-26-image1](2023-11-26-image1.png)
_Terraform 초기화 완료_

---

## Security Group 생성

main.tf 파일을 생성하고 SSH와 ALB에서 오는 애플리케이션 트래픽을 허용하는 Security Group을 정의한다. 아래에서 사용하는 변수는 뒤의 `variables.tf` 예시에 모두 정의한다.

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

ALB의 보안 그룹도 타겟 포트로 나가는 트래픽을 허용해야 한다. 위 예시에는 EC2의 아웃바운드 규칙이 없으므로 패키지 다운로드나 외부 API 접속이 필요하다면 egress 규칙을 별도로 추가한다.

실제 plan과 apply는 아래 파일과 변수를 모두 준비한 뒤 마지막 실행 절차에서 진행한다.

---

## EC2 인스턴스 생성

```hcl
resource "aws_instance" "this" {
  ami           = var.ami_id
  instance_type = "t2.micro"
  key_name      = var.key_name
  subnet_id     = var.subnet_id

  metadata_options {
    http_tokens = "required"
  }

  root_block_device {
    encrypted = true
  }

  tags = {
    Name = "blog-example"
  }

  vpc_security_group_ids = [
    aws_security_group.sg.id
  ]
}
```

![2023-11-26-image6](2023-11-26-image6.png)
_Terraform Console에서 리소스 정보 확인_

---

## 변수 정의

variables.tf에 변수를 정의한다.

```hcl
variable "vpc_id" {
  description = "Existing VPC used by the EC2 and ALB"
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

variable "listener_priority" {
  description = "Unused listener rule priority, 1 to 50000"
  type        = number

  validation {
    condition     = var.listener_priority >= 1 && var.listener_priority <= 50000 && floor(var.listener_priority) == var.listener_priority
    error_message = "Use an integer priority from 1 to 50000."
  }
}
```

---

## Target Group 생성

main.tf에 Target Group 리소스를 추가한다.

```hcl
resource "aws_lb_target_group" "target_group_client" {
  name_prefix     = "blog-"
  port            = var.target_port
  ip_address_type = "ipv4"
  protocol        = "HTTP"
  vpc_id          = var.vpc_id
  target_type     = "instance"

  health_check {
    path    = "/health"
    matcher = "200"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lb_target_group_attachment" "target_group_attach" {
  target_group_arn = aws_lb_target_group.target_group_client.arn
  target_id        = aws_instance.this.id
  port             = var.target_port
}
```

---

## Load Balancer 설정

기존 Load Balancer를 데이터 소스로 가져온다.

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
  priority     = var.listener_priority

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

## 값 입력과 전체 적용

다음 내용을 `terraform.tfvars`에 저장하고 예시 값을 모두 자신의 환경에 맞게 바꾼다. 도메인은 끝의 점 없이 입력한다. `admin_cidr`는 모든 사설망이 아니라 실제 운영자·VPN의 최소 범위로 지정한다.

```hcl
vpc_id            = "vpc-REPLACE"
subnet_id         = "subnet-REPLACE"
ami_id            = "ami-REPLACE"
key_name          = "existing-key-pair"
admin_cidr        = "192.0.2.10/32"
lb_name           = "existing-public-alb"
domain_name       = "example.com"
sub_domain        = "app"
target_port       = 8080
listener_priority = 100
```

`192.0.2.10`과 `example.com` 같은 예시 값은 자기 환경에 맞게 바꾸어 넣는다. AMI가 서울 리전에서 쓸 수 있고 `t2.micro` 아키텍처와 IMDSv2에 맞는지, 비용과 인스턴스 종류도 AWS 환경에서 함께 확인한다.

```bash
terraform fmt
terraform validate
terraform plan -out=tfplan
terraform show tfplan
# 위 계획의 계정·대상·변경·삭제 목록을 검토한 뒤 실행
terraform apply tfplan
```

`apply tfplan`은 저장된 계획을 추가 승인 질문 없이 바로 적용하므로 실행 전에 내용을 꼼꼼히 훑어봐야 한다. 코드나 환경이 바뀌었다면 새 plan을 만든다.

[Terraform plan 문서](https://developer.hashicorp.com/terraform/cli/commands/plan)에서 주의하듯 plan 파일에도 민감한 리소스 정보가 들어갈 수 있어 Git이나 공개 빌드 산출물에 올리지 않는다.

![2023-11-26-image3](2023-11-26-image3.png)
_당시 Terraform Plan 결과_

![2023-11-26-image4](2023-11-26-image4.png)
_당시 Terraform Apply 결과_

`apply` 성공은 AWS 리소스가 만들어졌다는 뜻이지 애플리케이션의 정상 응답까지 대신해 주지는 않는다. 실제 동작은 아래 표처럼 경계를 나눠 점검한다.

| 확인 | 실패할 때 확인할 경계 |
| --- | --- |
| Target Group이 healthy | 앱의 target port·`/health`, ALB에서 활성화된 AZ에 EC2가 있는지, ALB와 EC2의 보안 그룹, NACL |
| HTTPS로 도메인 접속 성공 | DNS 위임·alias, listener 인증서의 도메인 범위 |
| 올바른 앱이 응답 | host-header 규칙과 priority, target attachment |
| 다시 plan했을 때 예상치 못한 변경 없음 | 수동 변경, 동적 입력, provider 차이 |

외부에 공개한 URL에서 대표 요청을 확인하고, 생성한 보안 그룹의 SSH 허용 범위도 다시 점검한다.

## 핵심 명령어

```bash
terraform init      # 초기화
terraform plan      # 계획 확인
terraform apply     # 적용
terraform show      # 리소스 확인
terraform console   # 콘솔 접속
terraform plan -destroy  # 관리 중인 리소스의 삭제 계획 검토
```

---

## 운영 팁

**State는 코드와 별도로 보호한다.** `.terraform/`, `*.tfstate*`, `tfplan`은 Git에서 제외하고 `.terraform.lock.hcl`만 추적한다. [민감 정보와 state 문서](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)에서 다루듯 state 파일에는 민감한 값이 그대로 남을 수 있으므로, 화면 출력만 가리는 수준에 기대지 말고 저장소 접근 제어와 암호화를 챙겨야 한다.

다음은 Terraform 1.6 계열에서 쓰던 S3 + DynamoDB 잠금 방식이다. 버킷과 `LockID`(String) 파티션 키가 있는 테이블은 미리 만들어져 있고, 실행 역할이 두 저장소를 사용하는 데 필요한 권한을 갖고 있다고 가정한다.

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "ap-northeast-2"
    encrypt        = true
    dynamodb_table = "terraform-state-locks"
  }
}
```

backend 설정은 선택 사항이며, 처음 적용한 뒤 나중에 추가했다면 `terraform init`을 다시 실행해야 한다.

이후 [S3 backend 문서](https://developer.hashicorp.com/terraform/language/backend/s3)에서는 DynamoDB 잠금이 deprecated로 바뀌고 S3 자체 lockfile(`use_lockfile = true`)이 도입되었다. 새로 구성할 때는 사용 중인 CLI가 `use_lockfile = true`를 지원하는지 확인한 뒤 검토하는 편이 좋다(1.6.4 설정에 그대로 넣으면 안 된다).

S3 버킷에는 versioning과 암호화, 제한된 접근 권한을 걸고 state 복구 방법도 정해 둔다. lockfile 방식을 쓴다면 state 객체뿐 아니라 `.tflock` 객체의 읽기·쓰기·삭제 권한도 함께 필요하다. 기존 backend를 바꿀 때는 먼저 state를 백업하고 팀에서 다른 Terraform 작업이 돌지 않도록 조율한 뒤 `terraform init -migrate-state`로 이전한다.

가능하면 이 실습 리소스와 state 저장소는 생명주기를 분리해 두자. 환경을 정리할 때도 state가 관리하는 범위를 먼저 확인해야 한다. 여기서 data source로 불러온 기존 ALB·VPC·Hosted Zone은 Terraform이 새로 만든 리소스와 다르므로, 삭제 계획을 검토한 뒤 필요한 경우에만 `terraform destroy`를 실행한다.

코드로 인프라를 관리하면 구성을 다시 읽고 변경을 비교할 수 있다. 그 장점을 유지하려면 리소스 코드뿐 아니라 **실행 버전, 실제 입력값, state, 애플리케이션 검증**까지 함께 관리해야 한다.

당시 작성한 예제 코드는 [simple-aws-terraform](https://github.com/awesomelon/simple-aws-terraform) 저장소에 올려두었다. 본문에서는 읽고 따라 하기 편하도록 `provider.tf`·`main.tf`·`variables.tf`·`terraform.tfvars` 파일 네 개로 나누어 정리했다.

## 참고 자료

- [AWS: ALB 보안 그룹과 타겟 접근](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-update-security-groups.html)
- [HashiCorp: S3 Backend와 State Locking](https://developer.hashicorp.com/terraform/language/backend/s3)
- [tfenv: 버전 설치와 선택](https://github.com/tfutils/tfenv)
- [HashiCorp: Terraform 설치](https://developer.hashicorp.com/terraform/install)
- [HashiCorp: 저장된 plan 적용 방식](https://developer.hashicorp.com/terraform/cli/commands/plan)
- [AWS: CLI의 SSO 인증](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html)
