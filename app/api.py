"""FastAPI service: async job submission + polling, with rate limiting.
Run: uvicorn app.api:app --host 0.0.0.0 --port 8000
NOTE: JOBS is in-memory. Swap for Redis/Postgres + a worker queue for real production.
For multiple uvicorn workers, give slowapi a shared backend: Limiter(..., storage_uri="redis://...")."""
import os
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.runner import run_pipeline

MAX_WORKERS = int(os.getenv("MAX_CONCURRENT_JOBS", "2"))
MAX_PENDING = int(os.getenv("MAX_PENDING_JOBS", "10"))       # queued + running
SUBMIT_LIMIT = os.getenv("SUBMIT_RATE_LIMIT", "5/minute")    # per client IP

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Autonomous Research Platform")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)
JOBS: dict[str, dict] = {}


class ResearchRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=300)
    max_revisions: int = Field(default=2, ge=0, le=3)


def _pending() -> int:
    return sum(1 for j in JOBS.values() if j["status"] in ("queued", "running"))


def _work(job_id: str, req: ResearchRequest) -> None:
    JOBS[job_id]["status"] = "running"
    try:
        res = run_pipeline(req.topic, req.max_revisions)
        JOBS[job_id].update(
            status="done",
            verdict=res.verdict,
            attempts=res.attempts,
            report=res.report,
            finished_at=datetime.now(timezone.utc).isoformat(),
        )
    except Exception as e:  # noqa: BLE001
        JOBS[job_id].update(status="failed", error=str(e), trace=traceback.format_exc())


@app.post("/research", status_code=202)
@limiter.limit(SUBMIT_LIMIT)
def submit(req: ResearchRequest):
    if _pending() >= MAX_PENDING:
        raise HTTPException(429, "Server busy: too many pending jobs. Retry later.",
                            headers={"Retry-After": "60"})
    job_id = uuid.uuid4().hex
    JOBS[job_id] = {
        "id": job_id,
        "topic": req.topic,
        "status": "queued",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    pool.submit(_work, job_id, req)
    return {"job_id": job_id}


@app.get("/research/{job_id}")
def status(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(404, "job not found")
    return job


@app.get("/healthz")
def health():
    return {"ok": True}
