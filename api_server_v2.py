#!/usr/bin/env python3
"""
A11y Oracle API Server v2 - with Dashboard
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import json
import uuid
from datetime import datetime
from pathlib import Path

app = FastAPI(
    title="A11y Oracle API",
    description="Human-validated accessibility testing",
    version="0.2.0"
)

# File-based storage
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
    rating: str  # "good", "issues", "critical", "skipped"

# ============= DASHBOARD =============

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A11y Oracle Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: #1a1a1a;
            color: #fff;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { margin-bottom: 30px; }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: #2a2a2a;
            padding: 20px;
            border-radius: 8px;
        }
        .stat-value { font-size: 32px; font-weight: bold; color: #4a9eff; }
        .stat-label { font-size: 14px; opacity: 0.7; margin-top: 5px; }
        
        .section {
            background: #2a2a2a;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .section h2 { margin-bottom: 20px; font-size: 20px; }
        
        .job-list { display: flex; flex-direction: column; gap: 10px; }
        .job-item {
            background: #333;
            padding: 15px;
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .job-url { color: #4a9eff; font-size: 16px; }
        .job-meta { font-size: 12px; opacity: 0.6; margin-top: 5px; }
        
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: transform 0.1s;
        }
        button:hover { transform: scale(1.05); }
        button:active { transform: scale(0.95); }
        
        .btn-take { background: #4a9eff; color: white; }
        .btn-rating {
            padding: 30px 40px;
            font-size: 20px;
            margin: 10px;
        }
        .btn-good { background: #28a745; color: white; }
        .btn-issues { background: #ffc107; color: black; }
        .btn-critical { background: #dc3545; color: white; }
        .btn-skip { background: #6c757d; color: white; }
        
        .current-job {
            background: #2a4a2a;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .current-job-url { font-size: 24px; color: #4a9eff; margin-bottom: 20px; }
        .rating-buttons { display: flex; gap: 15px; flex-wrap: wrap; }
        
        .hidden { display: none; }
        .empty { text-align: center; opacity: 0.5; padding: 40px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 A11y Oracle Dashboard</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value" id="stat-queue">0</div>
                <div class="stat-label">В очереди</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="stat-completed">0</div>
                <div class="stat-label">Выполнено</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="stat-earned">$0</div>
                <div class="stat-label">Заработано</div>
            </div>
        </div>
        
        <div id="current-job-section" class="current-job hidden">
            <h2>🎯 Текущее задание</h2>
            <div class="current-job-url" id="current-url"></div>
            <p>Задание открыто в новой вкладке. Протестируйте с NVDA и оцените:</p>
            <div class="rating-buttons">
                <button class="btn-rating btn-good" data-rating="good" aria-label="Оценка: Хорошо, Alt+1">
                    ✅ Хорошо<br><small>Alt+1</small>
                </button>
                <button class="btn-rating btn-issues" data-rating="issues" aria-label="Оценка: Есть проблемы, Alt+2">
                    ⚠️ Проблемы<br><small>Alt+2</small>
                </button>
                <button class="btn-rating btn-critical" data-rating="critical" aria-label="Оценка: Критично, Alt+3">
                    ❌ Критично<br><small>Alt+3</small>
                </button>
                <button class="btn-rating btn-skip" data-rating="skipped" aria-label="Пропустить, Alt+0">
                    ⏭️ Пропустить<br><small>Alt+0</small>
                </button>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 Очередь заданий</h2>
            <div id="job-list" class="job-list">
                <div class="empty">Загрузка...</div>
            </div>
        </div>
    </div>

    <script>
        let currentJobId = null;
        let completedCount = 0;
        
        // Загрузка очереди
        async function loadQueue() {
            try {
                const res = await fetch('/api/v1/queue');
                const data = await res.json();
                
                document.getElementById('stat-queue').textContent = data.total;
                
                const jobList = document.getElementById('job-list');
                if (data.jobs.length === 0) {
                    jobList.innerHTML = '<div class="empty">Очередь пуста</div>';
                } else {
                    jobList.innerHTML = data.jobs.map(job => `
                        <div class="job-item">
                            <div>
                                <div class="job-url">${job.url}</div>
                                <div class="job-meta">Приоритет: ${job.priority} | ${new Date(job.created_at).toLocaleString()}</div>
                            </div>
                            <button class="btn-take" onclick="takeJob('${job.job_id}', '${job.url}')">
                                Взять задание
                            </button>
                        </div>
                    `).join('');
                }
            } catch (err) {
                console.error('Ошибка загрузки:', err);
            }
        }
        
        // Взять задание
        async function takeJob(jobId, url) {
            currentJobId = jobId;
            
            // Показать панель оценки
            document.getElementById('current-job-section').classList.remove('hidden');
            document.getElementById('current-url').textContent = url;
            
            // Открыть сайт в новой вкладке
            window.open(url, '_blank');
            
            // Обновить очередь
            loadQueue();
        }
        
        // Отправить оценку
        async function submitRating(rating) {
            if (!currentJobId) return;
            
            try {
                const res = await fetch(`/api/v1/result/${currentJobId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ rating })
                });
                
                if (res.ok) {
                    // Платимо тільки за реальні тести, не за skip
                    if (rating !== 'skipped') {
                        completedCount++;
                        document.getElementById('stat-completed').textContent = completedCount;
                        document.getElementById('stat-earned').textContent = '$' + (completedCount * 5);
                    }
                    
                    // Скрыть панель
                    document.getElementById('current-job-section').classList.add('hidden');
                    currentJobId = null;
                    
                    // Обновить очередь
                    loadQueue();
                    
                    alert('✅ Результат отправлен!');
                }
            } catch (err) {
                alert('❌ Ошибка: ' + err.message);
            }
        }
        
        // Обработка кликов на кнопки оценки
        document.querySelectorAll('.btn-rating').forEach(btn => {
            btn.addEventListener('click', () => submitRating(btn.dataset.rating));
        });
        
        // Hotkeys
        document.addEventListener('keydown', (e) => {
            if (!currentJobId) return;
            
            if (e.altKey) {
                e.preventDefault();
                if (e.key === '1') submitRating('good');
                else if (e.key === '2') submitRating('issues');
                else if (e.key === '3') submitRating('critical');
                else if (e.key === '0') submitRating('skipped');
            }
        });
        
        // Загрузка при старте
        loadQueue();
        
        // Автообновление каждые 10 сек
        setInterval(loadQueue, 10000);
    </script>
</body>
</html>
"""

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Dashboard для тестировщиков"""
    return DASHBOARD_HTML

# ============= API ENDPOINTS =============

@app.get("/")
async def root():
    return {
        "service": "A11y Oracle",
        "version": "0.2.0",
        "status": "running",
        "dashboard": "/dashboard",
        "endpoints": {
            "GET /dashboard": "Testing dashboard",
            "POST /api/v1/check": "Create check",
            "GET /api/v1/queue": "Get queue",
            "POST /api/v1/result/{job_id}": "Submit result"
        }
    }

@app.get("/health")
async def health():
    queue = load_queue()
    results = load_results()
    return {
        "status": "ok",
        "queue_size": len(queue),
        "completed_jobs": len(results)
    }

@app.post("/api/v1/check")
async def create_check(request: CheckRequest):
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
    queue.sort(key=lambda x: x["priority"], reverse=True)
    save_queue(queue)
    
    return {
        "job_id": job_id,
        "status": "pending",
        "message": "Job added to queue"
    }

@app.get("/api/v1/check/{job_id}")
async def get_check_status(job_id: str):
    results = load_results()
    
    if job_id in results:
        return results[job_id]
    
    queue = load_queue()
    for job in queue:
        if job["job_id"] == job_id:
            return {
                "job_id": job_id,
                "status": "pending",
                "url": job["url"]
            }
    
    raise HTTPException(status_code=404, detail="Job not found")

@app.get("/api/v1/queue")
async def get_queue():
    queue = load_queue()
    return {
        "total": len(queue),
        "jobs": queue[:10]
    }

@app.post("/api/v1/result/{job_id}")
async def submit_result(job_id: str, result: CheckResult):
    queue = load_queue()
    
    job = next((j for j in queue if j["job_id"] == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Удалить из очереди
    queue = [j for j in queue if j["job_id"] != job_id]
    save_queue(queue)
    
    # Сохранить результат
    results = load_results()
    results[job_id] = {
        "job_id": job_id,
        "url": job["url"],
        "status": "completed",
        "rating": result.rating,
        "completed_at": datetime.now().isoformat()
    }
    save_results(results)
    
    return {"message": "Result submitted", "job_id": job_id}

@app.delete("/api/v1/queue/{job_id}")
async def cancel_job(job_id: str):
    queue = load_queue()
    original_len = len(queue)
    queue = [j for j in queue if j["job_id"] != job_id]
    
    if len(queue) == original_len:
        raise HTTPException(status_code=404, detail="Job not found")
    
    save_queue(queue)
    return {"message": "Job cancelled"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
