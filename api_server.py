#!/usr/bin/env python3
"""
A11y Oracle API Server
Приймає запити від AI-агентів, зберігає в черзі
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import json
import uuid
from datetime import datetime
from pathlib import Path

app = FastAPI(
    title="A11y Oracle API",
    description="Human-validated accessibility testing",
    version="0.1.0"
)

# Простий file-based storage (поки без Redis)
QUEUE_FILE = Path("/tmp/a11y_queue.json")
RESULTS_FILE = Path("/tmp/a11y_results.json")

def load_queue():
    if QUEUE_FILE.exists():
        return json.loads(QUEUE_FILE.read_text())
    return []

def save_queue(queue):
    QUEUE_FILE.write_text(json.dumps(queue, indent=2))

def load_results():
    if RESULTS_FILE.exists():
        return json.loads(RESULTS_FILE.read_text())
    return {}

def save_results(results):
    RESULTS_FILE.write_text(json.dumps(results, indent=2))

class CheckRequest(BaseModel):
    url: HttpUrl
    priority: int = 1
    callback_url: Optional[HttpUrl] = None

class CheckResult(BaseModel):
    status: str
    score: Optional[int] = None
    issues: Optional[List[str]] = None
    message: Optional[str] = None

@app.get("/")
async def root():
    """API info"""
    return {
        "service": "A11y Oracle",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "POST /api/v1/check": "Create accessibility check",
            "GET /api/v1/check/{job_id}": "Get check result",
            "GET /api/v1/queue": "Get queue (for workers)",
            "POST /api/v1/result/{job_id}": "Submit result (for workers)"
        }
    }

@app.get("/health")
async def health():
    """Health check"""
    queue = load_queue()
    results = load_results()
    return {
        "status": "ok",
        "queue_size": len(queue),
        "completed_jobs": len(results)
    }

@app.post("/api/v1/check")
async def create_check(request: CheckRequest):
    """AI-агент створює запит на перевірку"""
    job_id = str(uuid.uuid4())
    
    job = {
        "job_id": job_id,
        "url": str(request.url),
        "priority": request.priority,
        "callback_url": str(request.callback_url) if request.callback_url else None,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    queue = load_queue()
    queue.append(job)
    # Сортуємо по пріоритету (5 = найвищий)
    queue.sort(key=lambda x: x["priority"], reverse=True)
    save_queue(queue)
    
    return {
        "job_id": job_id,
        "status": "pending",
        "message": "Job added to queue",
        "queue_position": next((i for i, j in enumerate(queue) if j["job_id"] == job_id), -1) + 1
    }

@app.get("/api/v1/check/{job_id}")
async def get_check_status(job_id: str):
    """Перевірка статусу завдання"""
    results = load_results()
    
    if job_id in results:
        return results[job_id]
    
    # Перевірити чи в черзі
    queue = load_queue()
    for job in queue:
        if job["job_id"] == job_id:
            return {
                "job_id": job_id,
                "status": "pending",
                "url": job["url"],
                "created_at": job["created_at"]
            }
    
    raise HTTPException(status_code=404, detail="Job not found")

@app.get("/api/v1/queue")
async def get_queue():
    """Отримати чергу завдань (для worker'а)"""
    queue = load_queue()
    return {
        "total": len(queue),
        "jobs": queue[:10]  # Перші 10
    }

@app.post("/api/v1/result/{job_id}")
async def submit_result(job_id: str, result: CheckResult):
    """Worker відправляє результат"""
    queue = load_queue()
    
    # Знайти job в черзі
    job = next((j for j in queue if j["job_id"] == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Видалити з черги
    queue = [j for j in queue if j["job_id"] != job_id]
    save_queue(queue)
    
    # Зберегти результат
    results = load_results()
    results[job_id] = {
        "job_id": job_id,
        "url": job["url"],
        "status": "completed",
        "result": result.dict(),
        "completed_at": datetime.now().isoformat(),
        "created_at": job["created_at"]
    }
    save_results(results)
    
    return {
        "message": "Result submitted",
        "job_id": job_id
    }

@app.delete("/api/v1/queue/{job_id}")
async def cancel_job(job_id: str):
    """Скасувати завдання"""
    queue = load_queue()
    original_len = len(queue)
    queue = [j for j in queue if j["job_id"] != job_id]
    
    if len(queue) == original_len:
        raise HTTPException(status_code=404, detail="Job not found")
    
    save_queue(queue)
    return {"message": "Job cancelled", "job_id": job_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
