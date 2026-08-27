# AWS Containerized Web Application

## 📌 Project Overview

This project demonstrates the deployment of a containerized Python web application on AWS using **Docker, Amazon ECR, Amazon ECS with AWS Fargate, Application Load Balancer, and GitHub Actions CI/CD**.

The project was designed as a hands-on cloud engineering exercise to demonstrate practical skills in:

* AWS networking
* Containerization
* Docker
* Amazon ECR
* Amazon ECS
* AWS Fargate
* Application Load Balancer
* IAM
* GitHub Actions
* GitHub OIDC
* Infrastructure and application deployment
* High availability
* Health checks and service recovery

The application runs as multiple containers on AWS Fargate behind an Application Load Balancer.

---

## 🏗️ Architecture

```text
                         Internet
                            │
                            ▼
                ┌─────────────────────┐
                │ Application Load    │
                │ Balancer             │
                │ HTTP :80             │
                └──────────┬──────────┘
                           │
                     Target Group
                       HTTP :5000
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
        ┌───────────────┐     ┌───────────────┐
        │ Fargate Task  │     │ Fargate Task  │
        │      #1       │     │      #2       │
        │               │     │               │
        │ Flask App     │     │ Flask App     │
        │ Port 5000     │     │ Port 5000     │
        └───────┬───────┘     └───────┬───────┘
                │                     │
                └──────────┬──────────┘
                           │
                    Docker Image
                           │
                           ▼
                ┌─────────────────────┐
                │ Amazon ECR          │
                │ Container Registry  │
                └──────────┬──────────┘
                           ▲
                           │
                    Docker Build/Push
                           │
                           │
                ┌─────────────────────┐
                │ GitHub Actions      │
                │ CI/CD Pipeline      │
                └──────────┬──────────┘
                           ▲
                           │
                       Git Push
                           │
                ┌─────────────────────┐
                │ GitHub Repository   │
                └─────────────────────┘
```

---

# ☁️ AWS Services Used

| AWS Service               | Purpose                                   |
| ------------------------- | ----------------------------------------- |
| Amazon VPC                | Network isolation                         |
| Public/Private Subnets    | Network segmentation                      |
| Security Groups           | Network access control                    |
| Application Load Balancer | Distributes traffic to containers         |
| Target Group              | Registers and health-checks Fargate tasks |
| Amazon ECS                | Container orchestration                   |
| AWS Fargate               | Serverless container compute              |
| Amazon ECR                | Docker image registry                     |
| AWS IAM                   | Identity and access management            |
| CloudWatch                | Monitoring and logging                    |
| GitHub Actions            | CI/CD automation                          |
| GitHub OIDC               | Secure authentication to AWS              |

---

# 🐳 Application

The application is a lightweight Python web application built using Flask.

### Application files

```text
aws-containerized-web-app/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── .dockerignore
│
└── .github/
    └── workflows/
        └── deploy.yml
```

---

## 🐍 Flask Application

The application is implemented using Python and Flask.

The application listens on:

```text
Port 5000
```

The container exposes the same port.

The application can be accessed through the Application Load Balancer after deployment.

---

# 🐳 Docker Containerization

The application is packaged into a Docker container to provide a consistent runtime environment.


## 📦 Amazon ECR

Amazon Elastic Container Registry (ECR) is used to store the Docker images.

Docker images are pushed to ECR as part of the CI/CD pipeline.


## 🚀 Amazon ECS with AWS Fargate

Amazon ECS is used as the container orchestration platform.

Running multiple tasks provides improved availability and allows the Application Load Balancer to distribute traffic between healthy containers.

## ⚖️ Application Load Balancer

An Application Load Balancer provides the public entry point to the application.

Traffic flow:

```text
Internet
   │
   ▼
Application Load Balancer
   │
   ▼
Target Group
   │
   ├── Fargate Task 1
   │
   └── Fargate Task 2
```

The ALB distributes incoming HTTP requests across healthy Fargate tasks.

---

## ❤️ Health Checks

The Target Group performs health checks against the container application.

Only healthy targets receive traffic.

This provides basic fault tolerance and automatic traffic removal for unhealthy containers.

## 🔐 Security Groups

Security groups are used to control network traffic between the components.

Typical traffic flow:

```text
Internet
   │
   │ HTTP :80
   ▼
ALB Security Group
   │
   │ HTTP :5000
   ▼
ECS/Fargate Security Group
```

The Fargate security group allows application traffic from the ALB rather than exposing the container port directly to the entire internet.

## 🔑 IAM and Security

IAM roles are used to provide AWS permissions without storing long-lived AWS access keys.

The ECS task uses an ECS task execution role for AWS service integration.

GitHub Actions uses a dedicated deployment role

The role is restricted to the GitHub repository used for this project.

## 🔐 GitHub OIDC

GitHub Actions authenticates to AWS using **OpenID Connect (OIDC)**.

No permanent AWS access keys are stored in GitHub.

Authentication flow:

```text
GitHub Actions
      │
      │ OIDC token
      ▼
AWS IAM
      │
      │ AssumeRoleWithWebIdentity
      ▼
GitHubActionsContainerDeploy
      │
      ├── Amazon ECR
      │
      └── Amazon ECS
```

The trust policy restricts the role to this repository:

The repository uses GitHub's immutable repository identity format:

This provides stronger repository-level identity control than relying only on repository names.

## 🔄 CI/CD Pipeline

GitHub Actions automates the application deployment using Workflow file

## Deployment workflow

```text
Developer
    │
    │ git push
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Checkout source
    │
    ├── Authenticate using OIDC
    │
    ├── Login to Amazon ECR
    │
    ├── Build Docker image
    │
    ├── Push image to ECR
    │
    ├── Retrieve ECS task definition
    │
    ├── Replace container image
    │
    ├── Register new task definition
    │
    ├── Update ECS service
    │
    └── Wait for service stability
    │
    ▼
AWS Fargate
```

## 🏷️ Immutable Image Tags

The CI/CD pipeline uses the GitHub commit SHA as the Docker image tag.

This provides a unique image version for each Git commit.

The deployment identifies the exact container image associated with the source-code revision.

This improves:

* Deployment traceability
* Version control
* Rollback capability
* Release auditing
* Reproducibility

---

### Application

Access the application through the Application Load Balancer DNS name.

---

# 📊 High Availability

The service is configured with two Fargate tasks:

```text
                Application Load Balancer
                         │
                ┌────────┴────────┐
                ▼                 ▼
          Fargate Task 1     Fargate Task 2
             Healthy            Healthy
```

If one task becomes unhealthy, the load balancer can stop routing traffic to that target while ECS maintains the desired service capacity.

This provides improved availability compared with running a single container.

---

# 🎯 Skills Demonstrated

This project demonstrates practical experience with:

### AWS

* Amazon VPC
* IAM
* Amazon ECR
* Amazon ECS
* AWS Fargate
* Application Load Balancer
* Target Groups
* Security Groups
* CloudWatch
* AWS CLI

### Containers

* Docker
* Dockerfile
* Container image creation
* Container registry
* ECS task definitions
* Fargate deployment

### DevOps

* Git
* GitHub
* GitHub Actions
* CI/CD
* OIDC authentication
* Immutable image tagging
* Automated deployments

### Networking

* VPC
* Subnets
* Security Groups
* Load balancing
* TCP/HTTP ports
* Health checks

---

# 📚 Key Learning Outcomes

Hands-on experience with the complete lifecycle of a containerized application:

```text
Source Code
    ↓
Docker
    ↓
Container Image
    ↓
Amazon ECR
    ↓
Amazon ECS
    ↓
AWS Fargate
    ↓
Application Load Balancer
    ↓
End User
```

I also implemented an automated CI/CD process:

```text
Git Push
   ↓
GitHub Actions
   ↓
OIDC
   ↓
AWS IAM
   ↓
ECR
   ↓
ECS
   ↓
Fargate
```

The project provided practical experience troubleshooting IAM, OIDC, Docker, ECS, security groups, health checks, and deployment automation.

---

# 🚀 Future Improvements

Potential future enhancements include:

* Infrastructure as Code using AWS CloudFormation
* Terraform implementation
* HTTPS using ACM
* Custom domain using Route 53
* CloudWatch dashboards
* Centralized application logging
* ECS autoscaling
* Blue/green deployments
* Automated rollback
* Container vulnerability scanning
* AWS Secrets Manager
* AWS WAF
* Private subnets with NAT Gateway
* Multi-AZ architecture
* Automated infrastructure deployment through CI/CD

---

# 👩‍💻 Author

**Thilini Herath**

Cloud / Infrastructure Engineering Portfolio

### Certifications & Areas of Study

* AWS Certified Solutions Architect – Associate
* AWS Certified Cloud Practitioner
* Microsoft Azure Fundamentals
* Red Hat Certified System Administrator
* Red Hat Certified Engineer
* Kubernetes / CKA preparation
* Linux Administration
* Cloud Infrastructure
* Networking
* DevOps & Automation

---

## ⭐ Project Status

**Project 3 — AWS Containerized Web Application**

Status:

```text
Infrastructure:       ✅ Completed
Docker:               ✅ Completed
ECR:                  ✅ Completed
ECS Fargate:          ✅ Completed
ALB:                  ✅ Completed
Health Checks:        ✅ Completed
GitHub OIDC:          ✅ Completed
CI/CD Pipeline:       ✅ Implemented
Immutable Images:     ✅ Validated
```

This project is part of an ongoing hands-on AWS cloud engineering portfolio.
