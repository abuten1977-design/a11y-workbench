#!/usr/bin/env python3
"""
A11y Oracle Worker
Підключається до сервера, бере завдання, відкриває браузер для тестування
"""

import asyncio
import httpx
from pynput import keyboard
import json
import sys
import subprocess
from datetime import datetime

# Конфігурація
SERVER_URL = "http://34.58.51.76:8000"
POLL_INTERVAL = 10  # Перевіряти чергу кожні 10 секунд
MAX_WAIT_TIME = 300  # Максимум 5 хвилин на одне завдання

class Worker:
    def __init__(self):
        self.current_job = None
        self.result = None
        self.waiting = False
        self.total_earned = 0
        self.jobs_completed = 0
        
    async def fetch_job(self):
        """Отримати завдання з черги"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{SERVER_URL}/api/v1/queue")
                data = response.json()
                
                if data["total"] > 0:
                    job = data["jobs"][0]
                    # Перевірити чи це не той самий job що вже обробляємо
                    if self.current_job and job["job_id"] == self.current_job.get("job_id"):
                        print(f"⚠️  Job {job['job_id'][:8]}... вже обробляється, пропускаю")
                        return None
                    return job
                return None
        except Exception as e:
            print(f"❌ Помилка підключення до сервера: {e}")
            return None
    
    async def submit_result(self, job_id: str, result: dict):
        """Відправити результат на сервер"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{SERVER_URL}/api/v1/result/{job_id}",
                    json=result
                )
                return response.json()
        except Exception as e:
            print(f"❌ Помилка відправки результату: {e}")
            return None
    
    async def process_job(self, job: dict):
        """Обробити завдання"""
        self.current_job = job
        job_id = job["job_id"]
        url = job["url"]
        
        print(f"\n{'='*60}")
        print(f"🔍 Нове завдання #{self.jobs_completed + 1}")
        print(f"{'='*60}")
        print(f"URL: {url}")
        print(f"Job ID: {job_id}")
        print(f"Створено: {job['created_at']}")
        print(f"{'='*60}\n")
        
        self.waiting = True
        self.result = None
        
        # Відкрити браузер Chrome в Windows
        try:
            print(f"⏳ Відкриваю Chrome в Windows...")
            import subprocess
            
            # Шлях до Chrome в Windows
            chrome_paths = [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            ]
            
            # Спробувати знайти Chrome
            chrome_path = None
            for path in chrome_paths:
                # Конвертувати Windows шлях в WSL
                path_without_drive = path[3:]  # Видалити "C:\"
                wsl_path = f'/mnt/c/{path_without_drive.replace(chr(92), "/")}'  # chr(92) = backslash
                import os
                if os.path.exists(wsl_path):
                    chrome_path = path
                    break
            
            if chrome_path:
                # Запустити Chrome
                subprocess.Popen(['/mnt/c/Windows/System32/cmd.exe', '/c', 'start', 'chrome', url])
                print(f"✅ Chrome відкрито\n")
            else:
                # Fallback - відкрити дефолтний браузер
                subprocess.Popen(['/mnt/c/Windows/System32/cmd.exe', '/c', 'start', url])
                print(f"✅ Браузер відкрито (Chrome не знайдено, використано дефолтний)\n")
            
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("📋 Тестуй зі скрінрідером, потім натисни:")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("  Alt+Shift+1 = ✅ Добре (доступний)")
            print("  Alt+Shift+2 = ⚠️  Є проблеми")
            print("  Alt+Shift+3 = ❌ Критичні помилки")
            print("  Alt+Shift+0 = 🚫 Пропустити")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            
            # Чекати на hotkey
            start_time = datetime.now()
            
            while self.waiting:
                await asyncio.sleep(0.5)
                
                # Перевірка timeout
                elapsed = (datetime.now() - start_time).total_seconds()
                if elapsed > MAX_WAIT_TIME:
                    print(f"\n⏰ Timeout ({MAX_WAIT_TIME}s)! Автоматично пропускаю...")
                    self.result = {
                        "status": "timeout",
                        "score": 0,
                        "issues": [],
                        "message": f"Timeout після {MAX_WAIT_TIME}s"
                    }
                    self.waiting = False
                    break
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Відправити результат
            if self.result:
                print(f"\n📤 Відправка результату...")
                response = await self.submit_result(job_id, self.result)
                
                if response:
                    self.jobs_completed += 1
                    earned = 3.0  # $3 за перевірку
                    self.total_earned += earned
                    
                    print(f"✅ Результат відправлено")
                    print(f"💰 Заробив: ${earned:.2f}")
                    print(f"📊 Всього: {self.jobs_completed} завдань, ${self.total_earned:.2f}")
                    print(f"⏱️  Час: {duration:.0f} сек")
                    
                    # Очистити current_job після успішної відправки
                    self.current_job = None
            else:
                # Якщо результату немає (timeout або помилка)
                print(f"⚠️  Результат не отримано, пропускаю job")
                self.current_job = None
            
        except Exception as e:
            print(f"❌ Помилка: {e}")
            # Очистити current_job при помилці
            self.current_job = None
    
    def on_hotkey_good(self):
        """Alt+Shift+1 - Добре"""
        if self.waiting:
            self.result = {
                "status": "accessible",
                "score": 90,
                "issues": [],
                "message": "Сайт доступний, проблем не виявлено"
            }
            self.waiting = False
            print("\n✅ Відмічено: ДОБРЕ (доступний)")
    
    def on_hotkey_issues(self):
        """Alt+Shift+2 - Є проблеми"""
        if self.waiting:
            self.result = {
                "status": "issues",
                "score": 60,
                "issues": ["keyboard_navigation", "focus_visible", "aria_labels"],
                "message": "Виявлено проблеми з доступністю"
            }
            self.waiting = False
            print("\n⚠️  Відмічено: Є ПРОБЛЕМИ")
    
    def on_hotkey_critical(self):
        """Alt+Shift+3 - Критичні помилки"""
        if self.waiting:
            self.result = {
                "status": "critical",
                "score": 30,
                "issues": ["keyboard_navigation", "screen_reader", "color_contrast", "heading_structure"],
                "message": "Критичні проблеми з доступністю"
            }
            self.waiting = False
            print("\n❌ Відмічено: КРИТИЧНІ ПОМИЛКИ")
    
    def on_hotkey_skip(self):
        """Alt+Shift+0 - Пропустити"""
        if self.waiting:
            self.result = {
                "status": "skipped",
                "score": 0,
                "issues": [],
                "message": "Не вдалося перевірити"
            }
            self.waiting = False
            print("\n🚫 Пропущено")
    
    async def run(self):
        """Основний цикл worker'а"""
        print("\n" + "="*60)
        print("🚀 A11y Oracle Worker запущено")
        print("="*60)
        print(f"📡 Сервер: {SERVER_URL}")
        print(f"⏱️  Інтервал перевірки: {POLL_INTERVAL} сек")
        print("="*60 + "\n")
        
        # Перевірка підключення
        print("🔍 Перевірка підключення до сервера...")
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{SERVER_URL}/health")
                data = response.json()
                print(f"✅ Підключено! Черга: {data['queue_size']} завдань\n")
        except Exception as e:
            print(f"❌ Не можу підключитись до сервера: {e}")
            print(f"Перевір що сервер працює: {SERVER_URL}")
            return
        
        # Реєстрація hotkeys
        print("⌨️  Hotkeys зареєстровано")
        print("Ctrl+C для виходу\n")
        
        with keyboard.GlobalHotKeys({
            '<alt>+<shift>+1': self.on_hotkey_good,
            '<alt>+<shift>+2': self.on_hotkey_issues,
            '<alt>+<shift>+3': self.on_hotkey_critical,
            '<alt>+<shift>+0': self.on_hotkey_skip
        }) as h:
            try:
                while True:
                    # Отримати завдання
                    job = await self.fetch_job()
                    
                    if job:
                        await self.process_job(job)
                        print(f"\n⏳ Чекаю наступне завдання...\n")
                    else:
                        # Черга порожня
                        print(f"⏳ Черга порожня. Перевірю через {POLL_INTERVAL} сек...", end="\r")
                        await asyncio.sleep(POLL_INTERVAL)
                        
            except KeyboardInterrupt:
                print("\n\n" + "="*60)
                print("👋 Worker зупинено")
                print("="*60)
                print(f"📊 Статистика:")
                print(f"   Завдань виконано: {self.jobs_completed}")
                print(f"   Заробив: ${self.total_earned:.2f}")
                print("="*60 + "\n")

async def main():
    worker = Worker()
    await worker.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 До побачення!")
        sys.exit(0)
