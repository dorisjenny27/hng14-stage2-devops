# HNG Stage 2: Containerized Job Processing System

A microservices application with a frontend, API, worker, and Redis queue; fully containerized with Docker and automated with CI/CD.

## Prerequisites
- Docker Desktop installed
- Docker Compose installed
- Git

## How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/dorisjenny27/hng14-stage2-devops.git
cd hng14-stage2-devops
```

### 2. Set up environment
```bash
cp .env.example .env
```

### 3. Start all services
```bash
docker compose up --build
```

### 4. What successful startup looks like
You should see:
- redis started and healthy
- api started on port 8000
- worker started and waiting for jobs
- frontend started on port 3000

Open browser at: http://localhost:3000

## Services & Endpoints

### Frontend (port 3000)
- `GET /` — Job dashboard UI

### API (port 8000)
- `GET /health` — Health check → `{"status": "healthy"}`
- `POST /submit` — Submit a job → `{"job_id": "uuid"}`
- `GET /status/{job_id}` — Get job status → `{"job_id": "...", "status": "queued|processing|completed"}`

## CI/CD Pipeline
GitHub Actions runs: lint → test → build → security scan → integration test → deploy
