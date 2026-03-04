#!/usr/bin/env python3
"""
A11y Oracle Worker v2 - з Flask панеллю керування
"""
import httpx
import time
import subprocess
import os
from threading import Thread
from flask import Flask, render_template_string

# Конфігурація
SERVER_URL = "http://34.58.51.76:8000"
POLL_INTERVAL = 10
CONTROL_PORT = 5000

# Flask app для панелі керування
app = Flask(__name__)
current_rating = None
current_job = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A11y Oracle - Панель керування</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: #1a1a1a;
            color: #fff;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
            text-align: center;
        }
        .job-info {
            background: #2a2a2a;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .job-url {
            font-size: 18px;
            color: #4a9eff;
            word-break: break-all;
        }
        .buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        button {
            padding: 40px 20px;
            font-size: 24px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.1s;
        }
        button:hover { transform: scale(1.05); }
        button:active { transform: scale(0.95); }
        .btn-good { background: #28a745; color: white; }
        .btn-issues { background: #ffc107; color: black; }
        .btn-critical { background: #dc3545; color: white; }
        .btn-skip { background: #6c757d; color: white; }
        .hotkey {
            display: block;
            font-size: 14px;
            opacity: 0.8;
            margin-top: 5px;
        }
        .status {
            text-align: center;
            margin-top: 20px;
            font-size: 18px;
            color: #4a9eff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 A11y Oracle - Панель керування</h1>
        
        <div class="job-info">
            <div>Тестуємо:</div>
            <div class="job-url">{{ url }}</div>
        </div>

        <div class="buttons">
            <button class="btn-good" data-rating="1" aria-label="Оцінка 1 - Добре, Alt+1">
                ✅ Добре
                <span class="hotkey">Alt+1</span>
            </button>
            <button class="btn-issues" data-rating="2" aria-label="Оцінка 2 - Є проблеми, Alt+2">
                ⚠️ Проблеми
                <span class="hotkey">Alt+2</span>
            </button>
            <button class="btn-critical" data-rating="3" aria-label="Оцінка 3 - Критично, Alt+3">
                ❌ Критично
                <span class="hotkey">Alt+3</span>
            </button>
            <button class="btn-skip" data-rating="0" aria-label="Пропустити, Alt+0">
                ⏭️ Пропустити
                <span class="hotkey">Alt+0</span>
            </button>
        </div>

        <div class="status" id="status"></div>
    </div>

    <script>
        // Обробка кліків
        document.querySelectorAll('button[data-rating]').forEach(btn => {
            btn.addEventListener('click', () => submitRating(btn.dataset.rating));
        });

        // Обробка hotkeys
        document.addEventListener('keydown', (e) => {
            if (e.altKey && ['1', '2', '3', '0'].includes(e.key)) {
                e.preventDefault();
                submitRating(e.key);
            }
        });

        function submitRating(rating) {
            fetch(`/rate/${rating}`)
                .then(r => r.json())
                .then(data => {
                    document.getElementById('status').textContent = '✅ Оцінку відправлено! Закриваємо браузер...';
                    setTimeout(() => window.close(), 1000);
                })
                .catch(err => {
                    document.getElementById('status').textContent = '❌ Помилка: ' + err;
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    url = current_job['url'] if current_job else 'Очікування завдання...'
    return render_template_string(HTML_TEMPLATE, url=url)

@app.route('/rate/<int:rating>')
def rate(rating):
    global current_rating
    current_rating = rating
    return {'status': 'ok', 'rating': rating}

def run_flask():
    """Запуск Flask в окремому потоці"""
    app.run(host='0.0.0.0', port=CONTROL_PORT, debug=False, use_reloader=False)

def open_browser(url):
    """Відкриває 2 вкладки: тестовий сайт + панель керування"""
    chrome_paths = [
        '/mnt/c/Program Files/Google/Chrome/Application/chrome.exe',
        '/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    ]
    
    chrome = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome = path
            break
    
    if not chrome:
        print("❌ Chrome не знайдено")
        return False
    
    # Вкладка 1: тестовий сайт
    subprocess.Popen([chrome, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    
    # Вкладка 2: панель керування
    subprocess.Popen([chrome, f'http://localhost:{CONTROL_PORT}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    return True

def close_browsers():
    """Закриває всі браузери"""
    os.system('taskkill.exe /F /IM chrome.exe 2>/dev/null')
    os.system('taskkill.exe /F /IM msedge.exe 2>/dev/null')

def submit_result(job_id, rating):
    """Відправляє результат на сервер"""
    rating_map = {1: "good", 2: "issues", 3: "critical", 0: "skipped"}
    
    try:
        with httpx.Client(timeout=10) as client:
            response = client.post(
                f"{SERVER_URL}/api/v1/result/{job_id}",
                json={"rating": rating_map[rating]}
            )
            return response.status_code == 200
    except Exception as e:
        print(f"❌ Помилка відправки: {e}")
        return False

def worker_loop():
    """Основний цикл worker"""
    global current_rating, current_job
    
    print("🚀 A11y Oracle Worker v2 запущено")
    print(f"📡 Сервер: {SERVER_URL}")
    print(f"🎛️  Панель: http://localhost:{CONTROL_PORT}")
    print("=" * 50)
    
    stats = {"completed": 0, "earnings": 0}
    
    while True:
        try:
            # Отримуємо завдання з черги
            with httpx.Client(timeout=10) as client:
                response = client.get(f"{SERVER_URL}/api/v1/queue")
                data = response.json()
                
                if data['total'] == 0:
                    print(f"⏳ Черга порожня. Очікування... (перевірка кожні {POLL_INTERVAL}с)")
                    time.sleep(POLL_INTERVAL)
                    continue
                
                job = data['jobs'][0]
                current_job = job
                current_rating = None
                
                print(f"\n📋 Нове завдання:")
                print(f"   URL: {job['url']}")
                print(f"   ID: {job['id']}")
                
                # Відкриваємо браузер
                if not open_browser(job['url']):
                    print("❌ Не вдалося відкрити браузер")
                    time.sleep(5)
                    continue
                
                print("🌐 Браузер відкрито. Очікування оцінки...")
                print("   Перейди на вкладку панелі керування")
                print("   Натисни Alt+1/2/3/0")
                
                # Чекаємо оцінку (макс 5 хв)
                timeout = 300
                elapsed = 0
                while current_rating is None and elapsed < timeout:
                    time.sleep(1)
                    elapsed += 1
                
                # Закриваємо браузери
                close_browsers()
                
                if current_rating is None:
                    print("⏱️  Timeout - пропускаємо завдання")
                    current_rating = 0
                
                # Відправляємо результат
                print(f"📤 Відправка результату: {current_rating}")
                if submit_result(job['id'], current_rating):
                    stats['completed'] += 1
                    stats['earnings'] += 5
                    print(f"✅ Результат відправлено")
                    print(f"📊 Статистика: {stats['completed']} завдань, ${stats['earnings']}")
                else:
                    print("❌ Помилка відправки результату")
                
                # Пауза перед наступним
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n\n👋 Зупинка worker...")
            close_browsers()
            break
        except Exception as e:
            print(f"❌ Помилка: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # Запускаємо Flask в окремому потоці
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Даємо Flask час запуститись
    time.sleep(2)
    
    # Запускаємо worker
    worker_loop()
