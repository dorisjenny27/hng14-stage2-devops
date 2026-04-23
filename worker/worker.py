import os
import time
import redis

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)


def process_job(job_id):
    print(f"Processing job {job_id}")
    redis_client.hset(f"job:{job_id}", "status", "processing")
    time.sleep(2)
    redis_client.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


def main():
    print("Worker started, waiting for jobs...")
    while True:
        try:
            result = redis_client.blpop("job_queue", timeout=5)
            if result:
                _, job_id = result
                process_job(job_id)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()
