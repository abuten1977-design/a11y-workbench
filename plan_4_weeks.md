# План на 4 тижні: Від нуля до перших грошей

## Ваш профіль
- План: А (безпечний)
- Час: 20-30 год/тиждень
- Ризик: Середній
- Навички: Python (середній), Linux/SSH (впевнений), Deque University
- Унікальна перевага: Доступ до Deque документації + таблиць WCAG

---

## ТИЖДЕНЬ 1: Швидкий старт (5-7 днів)

### Мета: Перша реєстрація + базовий прототип

#### День 1: Реєстрація на платформах

**Завдання:**
1. Fable (makeitfable.com)
   - Зареєструватись як tester
   - Вказати: NVDA/JAWS user, Deque training
   - Пройти onboarding тест

2. UserTesting (usertesting.com)
   - Профіль: accessibility specialist
   - Пройти practice test

3. Applause (applause.com)
   - Backup платформа

**Очікування:** Перше завдання через 3-7 днів

---

#### День 2-3: Налаштування локального середовища

**Встановлення інструментів:**

```bash
# 1. Python середовище
python3 -m venv ~/aiwork/venv
source ~/aiwork/venv/bin/activate

# 2. Базові бібліотеки
pip install fastapi uvicorn pydantic playwright pynput

# 3. Playwright браузер
playwright install chromium

# 4. MCP SDK (якщо доступний)
pip install mcp anthropic-mcp
```

**Перевірка:**
```bash
python3 --version  # 3.10+
which playwright
```

---

#### День 4-5: Перший прототип (локальний)

**Створюємо мінімальний accessibility checker:**

Файл: `~/aiwork/a11y_checker.py`

```python
#!/usr/bin/env python3
"""
Мінімальний accessibility checker
Версія 1: Локальна (без MCP)
"""

import asyncio
from playwright.async_api import async_playwright
from pynput import keyboard
import json
from datetime import datetime

class A11yChecker:
    def __init__(self):
        self.current_url = None
        self.result = None
        self.waiting = False
        
    async def check_url(self, url: str):
        """Відкриває URL і чекає на hotkey"""
        print(f"\n🔍 Перевірка: {url}")
        self.current_url = url
        self.waiting = True
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            
            try:
                await page.goto(url, timeout=30000)
                print("✅ Сайт відкрито")
                print("\n📋 Інструкції:")
                print("  Ctrl+Alt+1 = Добре (доступний)")
                print("  Ctrl+Alt+2 = Проблеми (недоступний)")
                print("  Ctrl+Alt+3 = Критичні помилки")
                
                # Чекаємо на hotkey
                while self.waiting:
                    await asyncio.sleep(0.5)
                
                await browser.close()
                return self.result
                
            except Exception as e:
                await browser.close()
                return {"error": str(e)}
    
    def on_hotkey_good(self):
        """Ctrl+Alt+1"""
        if self.waiting:
            self.result = {
                "url": self.current_url,
                "status": "accessible",
                "score": 90,
                "timestamp": datetime.now().isoformat()
            }
            self.waiting = False
            print("\n✅ Відмічено як доступний")
    
    def on_hotkey_issues(self):
        """Ctrl+Alt+2"""
        if self.waiting:
            self.result = {
                "url": self.current_url,
                "status": "issues",
                "score": 60,
                "timestamp": datetime.now().isoformat()
            }
            self.waiting = False
            print("\n⚠️ Відмічено як проблемний")
    
    def on_hotkey_critical(self):
        """Ctrl+Alt+3"""
        if self.waiting:
            self.result = {
                "url": self.current_url,
                "status": "critical",
                "score": 30,
                "timestamp": datetime.now().isoformat()
            }
            self.waiting = False
            print("\n❌ Відмічено як критичний")

async def main():
    checker = A11yChecker()
    
    # Реєструємо hotkeys
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+1': checker.on_hotkey_good,
        '<ctrl>+<alt>+2': checker.on_hotkey_issues,
        '<ctrl>+<alt>+3': checker.on_hotkey_critical
    }) as h:
        # Тестові URL
        test_urls = [
            "https://www.google.com",
            "https://github.com",
            "https://www.wikipedia.org"
        ]
        
        for url in test_urls:
            result = await checker.check_url(url)
            print(f"\n📊 Результат: {json.dumps(result, indent=2)}")
            print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
```

**Тестування:**
```bash
python3 ~/aiwork/a11y_checker.py
```

**Що має статись:**
1. Відкриється браузер з Google
2. Ви тестуєте зі скрінрідером
3. Натискаєте Ctrl+Alt+1/2/3
4. Скрипт виводить результат
5. Переходить до наступного сайту

---

#### День 6-7: Інтеграція з Deque базою знань

**Створюємо structured output з WCAG критеріями:**

Файл: `~/aiwork/deque_knowledge.py`

```python
"""
База знань з Deque University
Структуровані WCAG критерії
"""

WCAG_CRITERIA = {
    "keyboard_navigation": {
        "criterion": "2.1.1 Keyboard",
        "level": "A",
        "description": "Вся функціональність доступна з клавіатури",
        "deque_link": "https://dequeuniversity.com/rules/axe/4.4/keyboard"
    },
    "focus_visible": {
        "criterion": "2.4.7 Focus Visible",
        "level": "AA",
        "description": "Видимий індикатор фокусу",
        "deque_link": "https://dequeuniversity.com/rules/axe/4.4/focus-visible"
    },
    "alt_text": {
        "criterion": "1.1.1 Non-text Content",
        "level": "A",
        "description": "Альтернативний текст для зображень",
        "deque_link": "https://dequeuniversity.com/rules/axe/4.4/image-alt"
    },
    "heading_structure": {
        "criterion": "1.3.1 Info and Relationships",
        "level": "A",
        "description": "Логічна структура заголовків",
        "deque_link": "https://dequeuniversity.com/rules/axe/4.4/heading-order"
    },
    "color_contrast": {
        "criterion": "1.4.3 Contrast (Minimum)",
        "level": "AA",
        "description": "Достатній контраст тексту",
        "deque_link": "https://dequeuniversity.com/rules/axe/4.4/color-contrast"
    },
    "aria_labels": {
        "criterion": "4.1.2 Name, Role, Value",
        "level": "A",
        "description": "Коректні ARIA атрибути",
        "deque_link": "https://dequeuniversity.com/rules/axe/4.4/aria-valid-attr"
    }
}

def generate_report(url: str, issues: list) -> dict:
    """
    Генерує детальний звіт з посиланнями на Deque
    
    Args:
        url: URL сайту
        issues: Список проблем (ключі з WCAG_CRITERIA)
    
    Returns:
        Структурований звіт
    """
    report = {
        "url": url,
        "tested_by": "human_validator",
        "issues": []
    }
    
    for issue_key in issues:
        if issue_key in WCAG_CRITERIA:
            criterion = WCAG_CRITERIA[issue_key]
            report["issues"].append({
                "type": issue_key,
                "wcag": criterion["criterion"],
                "level": criterion["level"],
                "description": criterion["description"],
                "learn_more": criterion["deque_link"]
            })
    
    return report

# Приклад використання
if __name__ == "__main__":
    report = generate_report(
        url="https://example.com",
        issues=["keyboard_navigation", "alt_text", "color_contrast"]
    )
    
    import json
    print(json.dumps(report, indent=2, ensure_ascii=False))
```

**Результат буде виглядати так:**
```json
{
  "url": "https://example.com",
  "tested_by": "human_validator",
  "issues": [
    {
      "type": "keyboard_navigation",
      "wcag": "2.1.1 Keyboard",
      "level": "A",
      "description": "Вся функціональність доступна з клавіатури",
      "learn_more": "https://dequeuniversity.com/rules/axe/4.4/keyboard"
    }
  ]
}
```

**Це ваша конкурентна перевага:** AI-агенти отримують не просто "погано", а детальний звіт з посиланнями на документацію.

---

### Підсумок Тижня 1:
- ✅ Зареєстровані на платформах
- ✅ Локальний прототип працює
- ✅ Інтеграція з Deque базою знань
- ✅ Розумієте, як це працює

**Час:** ~15-20 годин

---

## ТИЖДЕНЬ 2: Google Cloud + API

### Мета: Сервер у хмарі, який приймає запити

#### День 8-9: Налаштування Google Cloud

**Крок 1: Створення проекту**

```bash
# Встановлення gcloud CLI (якщо немає)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Створення проекту
gcloud projects create a11y-oracle-001 --name="A11y Oracle"
gcloud config set project a11y-oracle-001

# Активація Free Tier
gcloud compute instances create a11y-server \
  --zone=us-central1-a \
  --machine-type=f1-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=30GB \
  --tags=http-server,https-server
```

**Крок 2: Підключення по SSH**

```bash
# Отримати IP
gcloud compute instances describe a11y-server \
  --zone=us-central1-a \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)'

# Підключитись
gcloud compute ssh a11y-server --zone=us-central1-a
```

---

#### День 10-11: Розгортання API на сервері

**На сервері (через SSH):**

```bash
# Оновлення системи
sudo apt update && sudo apt upgrade -y

# Python + pip
sudo apt install python3-pip python3-venv -y

# Створення проекту
mkdir ~/a11y-api
cd ~/a11y-api
python3 -m venv venv
source venv/bin/activate

# Встановлення залежностей
pip install fastapi uvicorn pydantic redis
```

**Файл: `~/a11y-api/server.py`**

```python
#!/usr/bin/env python3
"""
A11y Oracle API Server
Приймає запити від AI-агентів, додає в чергу
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional
import redis
import json
import uuid
from datetime import datetime

app = FastAPI(title="A11y Oracle API")

# Redis для черги (встановимо пізніше)
# Поки що in-memory
queue = []
results = {}

class CheckRequest(BaseModel):
    url: HttpUrl
    callback_url: Optional[HttpUrl] = None
    priority: int = 1

class CheckResult(BaseModel):
    job_id: str
    status: str  # pending, processing, completed, failed
    url: str
    result: Optional[dict] = None

@app.post("/api/v1/check")
async def create_check(request: CheckRequest):
    """
    AI-агент відправляє запит на перевірку
    """
    job_id = str(uuid.uuid4())
    
    job = {
        "job_id": job_id,
        "url": str(request.url),
        "callback_url": str(request.callback_url) if request.callback_url else None,
        "priority": request.priority,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    queue.append(job)
    results[job_id] = job
    
    return {
        "job_id": job_id,
        "status": "pending",
        "message": "Job added to queue",
        "queue_position": len(queue)
    }

@app.get("/api/v1/check/{job_id}")
async def get_check_status(job_id: str):
    """
    Перевірка статусу завдання
    """
    if job_id not in results:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return results[job_id]

@app.get("/api/v1/queue")
async def get_queue():
    """
    Отримати чергу завдань (для вашого worker'а)
    """
    return {
        "total": len(queue),
        "jobs": queue[:10]  # Перші 10
    }

@app.post("/api/v1/result/{job_id}")
async def submit_result(job_id: str, result: dict):
    """
    Ви відправляєте результат після перевірки
    """
    if job_id not in results:
        raise HTTPException(status_code=404, detail="Job not found")
    
    results[job_id]["status"] = "completed"
    results[job_id]["result"] = result
    results[job_id]["completed_at"] = datetime.now().isoformat()
    
    # Видаляємо з черги
    global queue
    queue = [j for j in queue if j["job_id"] != job_id]
    
    return {"message": "Result submitted", "job_id": job_id}

@app.get("/health")
async def health():
    return {"status": "ok", "queue_size": len(queue)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Запуск:**
```bash
python3 server.py
```

**Тестування (з вашого ноутбука):**
```bash
# Отримати IP сервера
SERVER_IP="<ваш_IP>"

# Створити завдання
curl -X POST http://$SERVER_IP:8000/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com", "priority": 1}'

# Перевірити чергу
curl http://$SERVER_IP:8000/api/v1/queue
```

---

#### День 12-14: Worker на вашому ноутбуці

**Файл: `~/aiwork/worker.py`**

```python
#!/usr/bin/env python3
"""
Worker: підключається до API, бере завдання, відкриває браузер
"""

import asyncio
import httpx
from playwright.async_api import async_playwright
from pynput import keyboard
import json

SERVER_URL = "http://<ваш_сервер_IP>:8000"

class Worker:
    def __init__(self):
        self.current_job = None
        self.result = None
        self.waiting = False
    
    async def fetch_job(self):
        """Отримати завдання з черги"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SERVER_URL}/api/v1/queue")
            data = response.json()
            
            if data["total"] > 0:
                return data["jobs"][0]
            return None
    
    async def submit_result(self, job_id: str, result: dict):
        """Відправити результат"""
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{SERVER_URL}/api/v1/result/{job_id}",
                json=result
            )
    
    async def process_job(self, job: dict):
        """Обробити завдання"""
        print(f"\n🔍 Нове завдання: {job['url']}")
        self.current_job = job
        self.waiting = True
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            
            await page.goto(job["url"])
            print("✅ Сайт відкрито. Тестуйте зі скрінрідером.")
            print("Ctrl+Alt+1/2/3 для оцінки")
            
            while self.waiting:
                await asyncio.sleep(0.5)
            
            await browser.close()
        
        # Відправити результат
        await self.submit_result(job["job_id"], self.result)
        print(f"✅ Результат відправлено: {self.result['status']}")
    
    def on_hotkey_good(self):
        if self.waiting:
            self.result = {"status": "accessible", "score": 90}
            self.waiting = False
    
    def on_hotkey_issues(self):
        if self.waiting:
            self.result = {"status": "issues", "score": 60}
            self.waiting = False
    
    def on_hotkey_critical(self):
        if self.waiting:
            self.result = {"status": "critical", "score": 30}
            self.waiting = False
    
    async def run(self):
        """Основний цикл"""
        print("🚀 Worker запущено. Чекаю завдань...")
        
        with keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+1': self.on_hotkey_good,
            '<ctrl>+<alt>+2': self.on_hotkey_issues,
            '<ctrl>+<alt>+3': self.on_hotkey_critical
        }) as h:
            while True:
                job = await self.fetch_job()
                
                if job:
                    await self.process_job(job)
                else:
                    print("⏳ Черга порожня. Чекаю 10 сек...")
                    await asyncio.sleep(10)

if __name__ == "__main__":
    worker = Worker()
    asyncio.run(worker.run())
```

**Запуск:**
```bash
python3 ~/aiwork/worker.py
```

**Що відбувається:**
1. Worker підключається до API на Google Cloud
2. Бере перше завдання з черги
3. Відкриває сайт у браузері
4. Ви тестуєте
5. Натискаєте hotkey
6. Worker відправляє результат на сервер
7. Повторює

---

### Підсумок Тижня 2:
- ✅ Сервер у Google Cloud (Free Tier)
- ✅ API приймає запити
- ✅ Worker на ноутбуці обробляє завдання
- ✅ Базова архітектура працює

**Час:** ~15-20 годин

---

## ТИЖДЕНЬ 3: MCP інтеграція

### Мета: AI-агенти можуть викликати ваш сервіс

#### День 15-17: MCP сервер

**Файл: `~/a11y-api/mcp_server.py`**

```python
#!/usr/bin/env python3
"""
MCP Server для A11y Oracle
AI-агенти можуть викликати через MCP
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx

server = Server("a11y-oracle")

@server.tool()
async def check_accessibility(url: str, priority: int = 1) -> dict:
    """
    Check website accessibility with human validator
    
    Args:
        url: Website URL to check
        priority: 1-5 (5 = urgent)
    
    Returns:
        Job ID and status
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/check",
            json={"url": url, "priority": priority}
        )
        return response.json()

@server.tool()
async def get_result(job_id: str) -> dict:
    """
    Get accessibility check result
    
    Args:
        job_id: Job ID from check_accessibility
    
    Returns:
        Result with WCAG violations
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://localhost:8000/api/v1/check/{job_id}"
        )
        return response.json()

if __name__ == "__main__":
    server.run()
```

**Публікація в MCP registry:**
```bash
# Створити mcp.json
cat > ~/a11y-api/mcp.json << 'EOF'
{
  "name": "a11y-oracle",
  "version": "0.1.0",
  "description": "Human-validated accessibility testing",
  "author": "Your Name",
  "tools": [
    {
      "name": "check_accessibility",
      "description": "Check website with real screen reader user"
    }
  ],
  "pricing": {
    "model": "per_check",
    "price_usd": 3.0
  }
}
EOF
```

---

#### День 18-21: Тестування + перші клієнти

**Тестування з Claude/ChatGPT:**

Якщо у вас є доступ до Claude Desktop або подібного:

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "a11y-oracle": {
      "command": "python",
      "args": ["/home/butenhome/a11y-api/mcp_server.py"]
    }
  }
}
```

**Або тестування через curl:**
```bash
# Симуляція AI-агента
curl -X POST http://$SERVER_IP:8000/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "priority": 3}'

# Отримати job_id, потім перевірити результат
curl http://$SERVER_IP:8000/api/v1/check/<job_id>
```

---

### Підсумок Тижня 3:
- ✅ MCP сервер працює
- ✅ AI-агенти можуть викликати ваш сервіс
- ✅ Базове тестування пройдено

**Час:** ~15-20 годин

---

## ТИЖДЕНЬ 4: Платежі + маркетинг

### Мета: Прийом оплати + перші клієнти

#### День 22-24: Lightning Network інтеграція

**Використаємо Strike API або BTCPay Server**

Базова інтеграція (спрощена):

```python
# Додати до server.py
from strike_api import create_invoice  # Приклад

@app.post("/api/v1/check")
async def create_check(request: CheckRequest):
    # Створити інвойс
    invoice = create_invoice(amount_usd=3.0)
    
    job = {
        "job_id": str(uuid.uuid4()),
        "url": str(request.url),
        "invoice": invoice["payment_request"],
        "status": "awaiting_payment"
    }
    
    return job
```

---

#### День 25-28: Маркетинг + перші клієнти

**Де шукати клієнтів:**

1. **Twitter/X:**
   ```
   🚀 Launched A11y Oracle - first MCP server with REAL screen reader validation
   
   Not just automated tools. Human expert with @dequesystems training.
   
   AI agents: check_accessibility("your-url") → detailed WCAG report
   
   #accessibility #AI #MCP
   ```

2. **Farcaster/Warpcast:**
   - Пости в /ai-agents канал
   - Пости в /accessibility канал

3. **GitHub:**
   - Створити repo з документацією
   - Додати в awesome-mcp-servers

4. **Discord/Telegram:**
   - AI agents communities
   - Web3 dev communities

---

### Підсумок Тижня 4:
- ✅ Платежі працюють
- ✅ Перші пости в соцмережах
- ✅ Документація готова
- ✅ Чекаємо перших клієнтів

**Час:** ~15-20 годин

---

## Загальний підсумок (4 тижні)

**Що ви матимете:**
1. ✅ Профілі на Fable/UserTesting (стабільний дохід)
2. ✅ Робочий MCP-сервер на Google Cloud
3. ✅ Worker на ноутбуці
4. ✅ Інтеграція з Deque базою знань
5. ✅ Прийом платежів через Lightning
6. ✅ Перші пости/маркетинг

**Очікуваний результат:**
- Перші $100-300 з платформ (тиждень 2-3)
- Перші 1-3 MCP клієнти (тиждень 4-5)
- База для масштабування

**Загальний час:** 60-80 годин (20 год/тиждень × 4 тижні)

---

## Наступні кроки після 4 тижнів

1. **Масштабування:** Найняти інших screen reader users
2. **Автоматизація:** Більше structured reports з Deque
3. **Ціноутворення:** A/B тестування $2-5 за перевірку
4. **Партнерства:** Інтеграція з Vercel, Netlify (CI/CD accessibility checks)

---

**Готовий почати? Скажи "так", і я створю перший скрипт для тестування.**
