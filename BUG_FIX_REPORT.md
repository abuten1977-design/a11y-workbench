# Виправлення бага Worker - Зациклення

## 🐛 Проблема

Worker зациклювався і відкривав один і той самий сайт нескінченно.

## 🔍 Причина

1. Worker бере завдання з черги: `GET /api/v1/queue` → повертає job
2. Відкриває браузер, ти тестуєш
3. Відправляє результат: `POST /api/v1/result/{job_id}`
4. **Сервер видаляє job з черги**
5. Але worker **не знає** що job видалено
6. Знову запитує чергу → **отримує той самий job** (якщо сервер не встиг видалити)
7. Повторює нескінченно

**Технічна причина:**
- Worker не зберігав `current_job`
- Не перевіряв чи це той самий job
- Не було timeout на випадок зависання

## ✅ Виправлення

### 1. Перевірка дублікатів
```python
async def fetch_job(self):
    job = data["jobs"][0]
    # Перевірити чи це не той самий job
    if self.current_job and job["job_id"] == self.current_job.get("job_id"):
        print(f"⚠️  Job вже обробляється, пропускаю")
        return None
    return job
```

### 2. Очищення current_job після обробки
```python
# Після успішної відправки
self.current_job = None

# При помилці
except Exception as e:
    self.current_job = None
```

### 3. Timeout (5 хвилин)
```python
MAX_WAIT_TIME = 300  # 5 хвилин

while self.waiting:
    elapsed = (datetime.now() - start_time).total_seconds()
    if elapsed > MAX_WAIT_TIME:
        print("⏰ Timeout! Автоматично пропускаю...")
        self.result = {"status": "timeout", ...}
        break
```

## 📊 Що змінилось

**До:**
```
1. Бере job → Відкриває браузер → Відправляє результат
2. Бере job → Відкриває браузер → Відправляє результат (той самий!)
3. Бере job → Відкриває браузер → Відправляє результат (той самий!)
∞ Нескінченно...
```

**Після:**
```
1. Бере job_1 → Зберігає в current_job → Обробляє → Очищає current_job
2. Бере job_2 → Перевіряє чи не дублікат → Обробляє → Очищає
3. Якщо черга порожня → Чекає 10 сек
4. Якщо timeout (5 хв) → Автоматично пропускає
```

## 🧪 Тестування

### Тест 1: Нормальна робота
```bash
# Створити 2 завдання
curl -X POST http://34.58.51.76:8000/api/v1/check \
  -d '{"url": "https://google.com", "priority": 1}'

curl -X POST http://34.58.51.76:8000/api/v1/check \
  -d '{"url": "https://github.com", "priority": 1}'

# Запустити worker
python3 worker.py

# Очікування:
# 1. Відкриє google.com
# 2. Після hotkey → відкриє github.com
# 3. Після hotkey → чекає нові завдання
```

### Тест 2: Timeout
```bash
# Створити завдання
curl -X POST http://34.58.51.76:8000/api/v1/check \
  -d '{"url": "https://google.com", "priority": 1}'

# Запустити worker
python3 worker.py

# НЕ натискати hotkey 5 хвилин

# Очікування:
# Через 5 хв → "⏰ Timeout! Автоматично пропускаю..."
# Job відмічено як "timeout"
# Worker переходить до наступного
```

### Тест 3: Помилка завантаження
```bash
# Створити завдання з неіснуючим сайтом
curl -X POST http://34.58.51.76:8000/api/v1/check \
  -d '{"url": "https://nonexistent-site-12345.com", "priority": 1}'

# Запустити worker
python3 worker.py

# Очікування:
# "❌ Помилка: ..."
# current_job очищено
# Worker переходить до наступного
```

## 🚀 Як використовувати виправлений worker

```bash
cd ~/aiwork
python3 worker.py
```

**Що побачиш:**
```
🚀 A11y Oracle Worker запущено
✅ Підключено! Черга: 2 завдань

🔍 Нове завдання #1
URL: https://google.com
[Браузер відкривається]

[Ти тестуєш, натискаєш Ctrl+Alt+1]

✅ Результат відправлено
💰 Заробив: $3.00

🔍 Нове завдання #2
URL: https://github.com
[Браузер відкривається]

[Ти тестуєш, натискаєш Ctrl+Alt+2]

✅ Результат відправлено
💰 Заробив: $3.00
📊 Всього: 2 завдань, $6.00

⏳ Черга порожня. Перевірю через 10 сек...
```

## 📝 Додаткові покращення

### Hotkey для екстреної зупинки
Можна додати `Ctrl+Alt+9` для негайної зупинки worker без Ctrl+C:

```python
def on_hotkey_emergency_stop(self):
    print("\n🛑 Екстрена зупинка!")
    self.waiting = False
    sys.exit(0)

# В run():
with keyboard.GlobalHotKeys({
    '<ctrl>+<alt>+1': self.on_hotkey_good,
    '<ctrl>+<alt>+2': self.on_hotkey_issues,
    '<ctrl>+<alt>+3': self.on_hotkey_critical,
    '<ctrl>+<alt>+0': self.on_hotkey_skip,
    '<ctrl>+<alt>+9': self.on_hotkey_emergency_stop  # Нова
}) as h:
```

### Логування в файл
Для дебагу можна додати логування:

```python
import logging

logging.basicConfig(
    filename='worker.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# В коді:
logging.info(f"Обробка job {job_id}")
logging.info(f"Результат: {self.result}")
```

## ✅ Статус

- ✅ Баг виправлено
- ✅ Додано перевірку дублікатів
- ✅ Додано timeout (5 хв)
- ✅ Додано очищення current_job
- ✅ Готово до тестування

**Файл:** `/home/butenhome/aiwork/worker.py`

**Тестуй!**
