#!/usr/bin/env python3
"""
A11y Oracle Worker - WSL2 Version
Відкриває браузер у Windows, hotkeys в WSL терміналі
"""

import asyncio
import httpx
import subprocess
import sys
from datetime import datetime

SERVER_URL = "http://34.58.51.76:8000"
POLL_INTERVAL = 10

class WorkerWSL:
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
                    return data["jobs"][0]
                return None
        except Exception as e:
            print(f"❌ Помилка підключення: {e}")
            return None
    
    async def submit_result(self, job_id: str, result: dict):
        """Відправити результат"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{SERVER_URL}/api/v1/result/{job_id}",
                    json=result
                )
                return response.json()
        except Exception as e:
            print(f"❌ Помилка відправки: {e}")
            return None
    
    def open_browser_windows(self, url: str):
        """Відкрити браузер у Windows"""
        try:
            # Відкрити через Windows
            subprocess.run(
                ["cmd.exe", "/c", "start", url],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except Exception as e:
            print(f"❌ Помилка відкриття браузера: {e}")
            return False
    
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
        print(f"{'='*60}\n")
        
        # Відкрити браузер у Windows
        print(f"🌐 Відкриваю браузер у Windows...")
        if not self.open_browser_windows(url):
            print("⚠️  Не вдалося відкрити браузер")
            return
        
        print(f"✅ Браузер відкрито у Windows\n")
        
        self.waiting = True
        self.result = None
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📋 Тестуй у Windows браузері з NVDA")
        print("   Потім введи оцінку тут:")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("  1 = ✅ Добре (доступний)")
        print("  2 = ⚠️  Є проблеми")
        print("  3 = ❌ Критичні помилки")
        print("  0 = 🚫 Пропустити")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        start_time = datetime.now()
        
        # Чекати на введення
        while self.waiting:
            try:
                choice = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: input("Твоя оцінка (1/2/3/0): ").strip()
                )
                
                if choice == "1":
                    self.result = {
                        "status": "accessible",
                        "score": 90,
                        "issues": [],
                        "message": "Сайт доступний"
                    }
                    self.waiting = False
                    print("\n✅ Відмічено: ДОБРЕ")
                    
                elif choice == "2":
                    self.result = {
                        "status": "issues",
                        "score": 60,
                        "issues": ["keyboard_navigation", "focus_visible", "aria_labels"],
                        "message": "Є проблеми з доступністю"
                    }
                    self.waiting = False
                    print("\n⚠️  Відмічено: Є ПРОБЛЕМИ")
                    
                elif choice == "3":
                    self.result = {
                        "status": "critical",
                        "score": 30,
                        "issues": ["keyboard_navigation", "screen_reader", "color_contrast"],
                        "message": "Критичні проблеми"
                    }
                    self.waiting = False
                    print("\n❌ Відмічено: КРИТИЧНІ ПОМИЛКИ")
                    
                elif choice == "0":
                    self.result = {
                        "status": "skipped",
                        "score": 0,
                        "issues": [],
                        "message": "Пропущено"
                    }
                    self.waiting = False
                    print("\n🚫 Пропущено")
                    
                else:
                    print("⚠️  Невірний вибір. Спробуй ще раз (1/2/3/0)")
                    
            except Exception as e:
                print(f"❌ Помилка: {e}")
                break
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Відправити результат
        if self.result:
            print(f"\n📤 Відправка результату...")
            response = await self.submit_result(job_id, self.result)
            
            if response:
                self.jobs_completed += 1
                earned = 3.0
                self.total_earned += earned
                
                print(f"✅ Результат відправлено")
                print(f"💰 Заробив: ${earned:.2f}")
                print(f"📊 Всього: {self.jobs_completed} завдань, ${self.total_earned:.2f}")
                print(f"⏱️  Час: {duration:.0f} сек")
    
    async def run(self):
        """Основний цикл"""
        print("\n" + "="*60)
        print("🚀 A11y Oracle Worker (WSL2)")
        print("="*60)
        print(f"📡 Сервер: {SERVER_URL}")
        print(f"🌐 Браузер: Windows (Edge/Chrome)")
        print(f"⌨️  Введення: WSL термінал")
        print("="*60 + "\n")
        
        # Перевірка підключення
        print("🔍 Перевірка підключення...")
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{SERVER_URL}/health")
                data = response.json()
                print(f"✅ Підключено! Черга: {data['queue_size']} завдань\n")
        except Exception as e:
            print(f"❌ Не можу підключитись: {e}")
            return
        
        print("Ctrl+C для виходу\n")
        
        try:
            while True:
                job = await self.fetch_job()
                
                if job:
                    await self.process_job(job)
                    print(f"\n⏳ Чекаю наступне завдання...\n")
                else:
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
    worker = WorkerWSL()
    await worker.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 До побачення!")
        sys.exit(0)
