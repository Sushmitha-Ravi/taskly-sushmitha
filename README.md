# Taskly

<p align="center">
  <img src="docs/taskly-banner.svg" alt="Taskly — Production-Ready Task Management API" width="100%">
</p>

<p align="center">
  <strong>Production-ready Task Management API evolving from local development to AWS cloud infrastructure.</strong>
</p>

<p align="center">
  <img alt="Python 3.12" src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.111.0-009688?style=flat-square&logo=fastapi&logoColor=white">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-RDS-4169E1?style=flat-square&logo=postgresql&logoColor=white">
  <img alt="Redis" src="https://img.shields.io/badge/Redis-ElastiCache-DC382D?style=flat-square&logo=redis&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-Production-2496ED?style=flat-square&logo=docker&logoColor=white">
  <img alt="Terraform" src="https://img.shields.io/badge/Terraform-IaC-7B42BC?style=flat-square&logo=terraform&logoColor=white">
  <img alt="AWS" src="https://img.shields.io/badge/AWS-us--east--1-FF9900?style=flat-square&logo=amazonaws&logoColor=white">
</p>

---

## About

Taskly is a production-oriented task management API built with **FastAPI**. The project progressively applies backend engineering, containerization, observability, and AWS infrastructure practices.

The project is currently completed through **Stage 4 — AWS Infrastructure with Terraform**.

### Current architecture

```text
                        Taskly API
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      PostgreSQL                    Redis Cache
      Amazon RDS                 Amazon ElastiCache

              AWS infrastructure managed by
                     Terraform
```

> Stage 5 will deploy the existing production image to the existing Amazon EKS cluster. It is intentionally not included as completed work yet.

---

## Project Progress

| Stage | Area | Status |
|---|---|---|
| **Stage 1** | Application Setup & Understanding | ✅ Complete |
| **Stage 2** | Application Production Upgrade | ✅ Complete |
| **Stage 3** | Docker & Local Production Stack | ✅ Complete |
| **Stage 4** | AWS Infrastructure with Terraform | ✅ Complete |
| **Stage 5** | Kubernetes / EKS Deployment | ⏳ Next |

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| API | FastAPI |
| Validation | Pydantic |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Cache | Redis |
| Metrics | Prometheus |
| Logging | Structured JSON logging |
| Containerization | Docker |
| Local orchestration | Docker Compose |
| Infrastructure as Code | Terraform |
| Cloud | AWS |
| Kubernetes | Amazon EKS |
| Container Registry | Amazon ECR |
| Managed database | Amazon RDS PostgreSQL |
| Managed cache | Amazon ElastiCache Redis |

---

## Key Features

### API

- Task CRUD operations
- Pydantic request/response models
- `/health` health endpoint
- `/metrics` Prometheus endpoint

### Performance

- Redis caching for task-list reads
- Cache invalidation after task creation and mutations
- PostgreSQL persistence

### Observability

- Prometheus HTTP request counter
- HTTP request duration histogram
- `tasks_created_total` counter
- Structured JSON logging
- Per-request `X-Request-ID`

### Containerization

- Production Dockerfile
- Python 3.12 slim base image
- Non-root `taskly` container user
- Docker Compose application stack
- PostgreSQL persistence
- Redis service

---

# Stage 1 — Application Setup & Understanding

The original FastAPI application provides the foundation for the Taskly API.

Core API capabilities include:

```text
GET    /health
GET    /metrics
GET    /tasks
POST   /tasks
GET    /tasks/{task_id}
PATCH  /tasks/{task_id}
DELETE /tasks/{task_id}
```

The API uses Pydantic models for request/response validation and SQLAlchemy for database access.

---

# Stage 2 — Application Production Upgrade

The application was upgraded from a basic bootcamp API into a more production-oriented service.

### Improvements

- PostgreSQL database integration
- SQLAlchemy models and sessions
- Redis integration
- Redis caching
- Cache invalidation
- Structured logging
- Request ID generation
- Prometheus metrics
- Health endpoint
- Production-oriented configuration
- Dependency separation

### Observability flow

```text
HTTP Request
     │
     ├── X-Request-ID
     │
     ├── Request counter
     │
     ├── Request duration
     │
     └── Structured JSON log
```

---

# Stage 3 — Docker & Local Production Stack

Taskly was containerized and tested as a multi-service production-style local stack.

```text
                    Docker Compose
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
     Taskly API     PostgreSQL        Redis
       :8000
```

### Completed

- Production Dockerfile
- `.dockerignore`
- Non-root container user
- Environment variables
- Docker Compose
- Docker networking
- PostgreSQL persistence
- Redis caching and invalidation
- Prometheus `/metrics`
- `tasks_created_total`
- JSON logging
- Request ID
- End-to-end API verification
- Docker Compose cleanup

The production image is configured to run Uvicorn on port `8000` as the non-root `taskly` user.

---

# Stage 4 — AWS Infrastructure with Terraform

The AWS infrastructure was provisioned with Terraform and verified independently before moving to Kubernetes deployment.

### AWS Region

```text
us-east-1
```

### Infrastructure

```text
                         AWS VPC
                           │
             ┌─────────────┴─────────────┐
             │                           │
       Public Subnets              Private Subnets
             │                           │
      Internet Gateway             NAT Gateway
                                         │
                         ┌───────────────┼───────────────┐
                         │               │               │
                        EKS             RDS          ElastiCache
                      Cluster        PostgreSQL          Redis
```

### Terraform-managed resources

- VPC
- Public subnets
- Private subnets
- Internet Gateway
- NAT Gateway
- Public/private route tables
- EKS subnet tags
- EKS IAM roles
- Amazon EKS cluster
- EKS managed node group
- Amazon ECR repository
- Amazon RDS PostgreSQL
- Amazon ElastiCache Redis
- Terraform outputs

### Verified AWS resources

| Resource | Identifier |
|---|---|
| Region | `us-east-1` |
| EKS cluster | `taskly-sushmitha-eks` |
| ECR repository | `taskly-sushmitha-api` |
| RDS PostgreSQL | `taskly-sushmitha-postgres` |
| ElastiCache Redis | `taskly-sushmitha-redis` |
| VPC | `vpc-0c533ed5bdd9c8e2f` |

### EKS verification

- 2 worker nodes
- Both nodes `Ready`
- Kubernetes version `v1.36.2-eks-254016e`
- `kubectl` connectivity verified

### RDS verification

- Status: `available`
- PostgreSQL port: `5432`

### Redis verification

- Status: `available`

### ECR verification

- Repository created
- Image scanning on push enabled
- Repository ready for the Stage 5 application image

---

# Infrastructure as Code

Terraform configuration is stored under:

```text
terraform/
├── main.tf
├── providers.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
├── terraform.tfstate
├── terraform.tfstate.backup
└── .terraform.lock.hcl
```

Terraform state and sensitive configuration are protected through `.gitignore` and are **not intended to be committed to the public repository**.

---

# Repository Structure

```text
bootcamp-tasks-api/
│
├── main.py
├── database.py
├── models.py
├── redis_client.py
├── logging_config.py
├── requirements.txt
│
├── Dockerfile
├── .dockerignore
├── compose.yaml
├── .gitignore
│
├── terraform/
│   ├── main.tf
│   ├── providers.tf
│   ├── variables.tf
│   └── outputs.tf
│
└── README.md
```

> Kubernetes manifests will be added in Stage 5.

---

# Local Development

Create the Python environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API locally:

```bash
uvicorn main:app --reload
```

API documentation:

```text
http://localhost:8000/docs
```

Health endpoint:

```text
http://localhost:8000/health
```

Metrics:

```text
http://localhost:8000/metrics
```

---

# Docker Development

Build and start the local production-style stack:

```bash
docker compose up --build
```

The stack provides:

```text
Taskly API
    │
    ├── PostgreSQL
    │
    └── Redis
```

---

# Security Practices

The project applies several production-oriented practices:

- Non-root Docker container user
- Separate application/database/cache configuration
- Private AWS subnets
- IAM roles for AWS services
- Security groups
- Terraform state protection
- Sensitive Terraform configuration excluded from Git
- Secrets kept outside application source

No credentials, database passwords, or Redis authentication values belong in this README.

---

# Project Roadmap

```text
Application Setup
       │
       ▼
Production Upgrade
       │
       ▼
Docker & Local Production
       │
       ▼
AWS Infrastructure
       │
       ▼
EKS Deployment             ← NEXT
       │
       ▼
CI/CD
       │
       ▼
Monitoring & Logging
       │
       ▼
Security Hardening
       │
       ▼
Production-Ready Taskly
```

---

## Next Stage

### Stage 5 — Deploy Taskly to Amazon EKS

The next stage will use the **existing Stage 4 infrastructure** to:

1. Push the production Docker image to ECR
2. Prepare Kubernetes manifests
3. Configure Secrets and ConfigMaps
4. Deploy Taskly API to EKS
5. Connect the application to RDS PostgreSQL
6. Connect the application to ElastiCache Redis
7. Configure Kubernetes Service
8. Configure health checks and resources
9. Verify logs, request IDs, metrics, PostgreSQL, and Redis
10. Expose and test the API

**Stage 5 has not started in this repository documentation yet.**

---

## Author

**Sushmitha Ravi**

GitHub: [Sushmitha-Ravi](https://github.com/Sushmitha-Ravi)

---

## License

This project is developed as part of a DevOps & Cloud Computing bootcamp and as a portfolio project demonstrating application development, containerization, Infrastructure as Code, and AWS cloud engineering.
