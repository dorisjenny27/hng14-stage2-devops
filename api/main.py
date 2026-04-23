import os
import uuid
import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/submit")
def create_job():
    job_id = str(uuid.uuid4())
    redis_client.hset(f"job:{job_id}", "status", "queued")
    redis_client.rpush("job_queue", job_id)
    return {"job_id": job_id}

@app.get("/status/{job_id}")
def get_job(job_id: str):
    data = redis_client.hgetall(f"job:{job_id}")
    if not data:
        return {"error": "not found"}
    return {"job_id": job_id, "status": data.get("status")}