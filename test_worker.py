#!/usr/bin/env python3
"""
A11y Oracle Worker - WSL2 Test Version
Без браузера, тільки тестування логіки
"""

import asyncio
import httpx
import json
import sys

SERVER_URL = "http://34.58.51.76:8000"

async def test_connection():
    """Тест підключення"""
    print("🔍 Тестування підключення до сервера...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{SERVER_URL}/health")
            data = response.json()
            print(f"✅ Підключено!")
            print(f"   Черга: {data['queue_size']} завдань")
            print(f"   Виконано: {data['completed_jobs']} завдань")
            return True
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

async def get_queue():
    """Отримати чергу"""
    print("\n📋 Отримання черги...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{SERVER_URL}/api/v1/queue")
            data = response.json()
            
            print(f"   Всього завдань: {data['total']}")
            
            if data['total'] > 0:
                print("\n   Завдання:")
                for i, job in enumerate(data['jobs'][:5], 1):
                    print(f"   {i}. {job['url']}")
                    print(f"      Job ID: {job['job_id'][:8]}...")
                    print(f"      Створено: {job['created_at']}")
                    print()
                return data['jobs'][0] if data['jobs'] else None
            else:
                print("   Черга порожня")
                return None
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return None

async def submit_result(job_id: str, status: str):
    """Відправити результат"""
    print(f"\n📤 Відправка результату...")
    
    result = {
        "status": status,
        "score": 90 if status == "accessible" else 60,
        "issues": [] if status == "accessible" else ["test_issue"],
        "message": f"Тестовий результат: {status}"
    }
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{SERVER_URL}/api/v1/result/{job_id}",
                json=result
            )
            data = response.json()
            print(f"✅ Результат відправлено")
            print(f"   {data['message']}")
            return True
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

async def interactive_test():
    """Інтерактивний тест"""
    print("\n" + "="*60)
    print("🧪 A11y Oracle Worker - Тестовий режим")
    print("="*60)
    
    # Тест 1: Підключення
    if not await test_connection():
        return
    
    # Тест 2: Отримати завдання
    job = await get_queue()
    
    if not job:
        print("\n⚠️  Немає завдань для тестування")
        print("Створи завдання:")
        print('curl -X POST http://34.58.51.76:8000/api/v1/check \\')
        print('  -H "Content-Type: application/json" \\')
        print('  -d \'{"url": "https://google.com", "priority": 1}\'')
        return
    
    # Тест 3: Симуляція тестування
    print("\n" + "="*60)
    print("🎯 Симуляція тестування")
    print("="*60)
    print(f"URL: {job['url']}")
    print(f"Job ID: {job['job_id']}")
    print()
    print("В реальному режимі тут відкриється браузер")
    print("Ти тестуєш зі скрінрідером і натискаєш hotkey")
    print()
    print("Зараз симулюємо результат...")
    
    await asyncio.sleep(2)
    
    # Тест 4: Відправити результат
    success = await submit_result(job['job_id'], "accessible")
    
    if success:
        print("\n" + "="*60)
        print("✅ Тест пройдено успішно!")
        print("="*60)
        print()
        print("Наступні кроки:")
        print("1. Налаштувати GUI для WSL2 (якщо потрібно)")
        print("2. Запустити повний Worker: python3 worker.py")
        print("3. Тестувати реальні сайти")

async def main():
    try:
        await interactive_test()
    except KeyboardInterrupt:
        print("\n\n👋 Тест перервано")

if __name__ == "__main__":
    asyncio.run(main())
