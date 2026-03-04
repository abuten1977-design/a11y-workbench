# День 1: Реєстрація + Google Cloud Setup

## Частина А: Google Cloud (30-40 хв)

### Швидкий старт:

```bash
cd ~/aiwork
./setup_gcloud.sh
```

**Що робить скрипт:**
1. Створює нову конфігурацію gcloud
2. Логін (відкриє браузер)
3. Створює новий проект
4. Просить активувати billing (Free Tier - безкоштовно)
5. Створює f1-micro сервер (Free Tier)
6. Налаштовує firewall
7. Виводить IP адресу

**Якщо щось піде не так:**

```bash
# Перевірити існуючі проекти
gcloud projects list

# Перевірити існуючі сервери
gcloud compute instances list

# Видалити старий сервер (якщо треба)
gcloud compute instances delete a11y-server --zone=us-central1-a
```

### Після створення сервера:

**Підключитись:**
```bash
gcloud compute ssh a11y-server --zone=us-central1-a
```

**На сервері виконати:**
```bash
# Перевірка
python3 --version  # Має бути 3.10+
pip3 --version

# Створити директорію
mkdir ~/a11y-api
cd ~/a11y-api

# Створити venv
python3 -m venv venv
source venv/bin/activate

# Встановити базові пакети
pip install fastapi uvicorn pydantic

# Тест
python3 -c "import fastapi; print('FastAPI OK')"
```

**Вийти з сервера:**
```bash
exit
```

---

## Частина Б: Реєстрація на платформах (30-40 хв)

### 1. Fable (makeitfable.com) - ПРІОРИТЕТ #1

**Чому Fable:**
- Спеціалізуються на accessibility
- Платять $50-75/год
- Шукають саме screen reader users

**Кроки:**

1. **Відкрити:** https://makeitfable.com/become-an-assistant

2. **Заповнити форму:**
   - Name: [твоє ім'я]
   - Email: [твій email]
   - Location: Ukraine (або де ти)
   - Disability: Blind / Low Vision
   - Assistive Technology: 
     ```
     NVDA (primary), JAWS (familiar)
     Keyboard navigation expert
     ```
   - Experience:
     ```
     - Completed Deque University accessibility training
     - 5+ years using screen readers daily
     - Web developer with accessibility focus
     - Familiar with WCAG 2.1/2.2 standards
     ```

3. **Пройти тестове завдання:**
   - Вони дадуть тестовий сайт
   - Треба знайти accessibility проблеми
   - Написати короткий звіт

4. **Очікування:** Відповідь через 3-7 днів

**Шаблон звіту (для тесту):**
```
Accessibility Issues Found:

1. Keyboard Navigation
   - Issue: [опис]
   - WCAG: 2.1.1 Keyboard (Level A)
   - Impact: High

2. Screen Reader Compatibility
   - Issue: [опис]
   - WCAG: 4.1.2 Name, Role, Value (Level A)
   - Impact: Critical

3. Focus Management
   - Issue: [опис]
   - WCAG: 2.4.7 Focus Visible (Level AA)
   - Impact: Medium

Positive Aspects:
- [що добре зроблено]

Recommendations:
- [конкретні поради]
```

---

### 2. UserTesting (usertesting.com)

**Чому UserTesting:**
- Більше завдань (не тільки accessibility)
- $30-60/тест
- Швидша реєстрація

**Кроки:**

1. **Відкрити:** https://www.usertesting.com/be-a-user-tester

2. **Sign Up:**
   - Email, пароль
   - Demographics (вік, стать, освіта)

3. **Profile:**
   - Devices: Desktop (Linux), Mobile (якщо є)
   - Special Skills:
     ```
     ✓ Accessibility Testing
     ✓ Screen Reader User (NVDA)
     ✓ Web Development
     ✓ WCAG Knowledge
     ```

4. **Practice Test:**
   - Дадуть тестовий сайт
   - Треба говорити вголос (або писати) що робиш
   - 10-15 хвилин

5. **Очікування:** Перший тест через 1-3 дні

**Поради для тестів:**
- Говори чітко, що бачиш/чуєш від скрінрідера
- Пояснюй, чому щось незручно
- Згадуй WCAG критерії (це +бали)

---

### 3. Applause (applause.com) - BACKUP

**Тільки якщо є час:**

1. **Відкрити:** https://www.applause.com/become-a-tester

2. **Sign Up** → заповнити профіль

3. **Вказати:** Accessibility Testing як спеціалізацію

---

## Частина В: Локальне середовище (20-30 хв)

**Поки чекаємо відповіді від платформ, готуємо інструменти:**

```bash
cd ~/aiwork

# Створити venv
python3 -m venv venv
source venv/bin/activate

# Встановити пакети
pip install playwright pynput httpx fastapi uvicorn pydantic

# Встановити браузер для Playwright
playwright install chromium

# Перевірка
python3 << 'EOF'
import playwright
import pynput
import httpx
print("✅ Всі пакети встановлені")
EOF
```

**Створити тестовий скрипт:**

```bash
cat > ~/aiwork/test_browser.py << 'EOF'
#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.google.com")
        print("✅ Браузер відкрито")
        await asyncio.sleep(3)
        await browser.close()
        print("✅ Тест пройдено")

asyncio.run(test())
EOF

chmod +x ~/aiwork/test_browser.py
python3 ~/aiwork/test_browser.py
```

**Має відкритись браузер з Google на 3 секунди.**

---

## Частина Г: SSH ключі для Google Cloud

**Якщо у тебе вже є система управління ключами:**

```bash
# Перевірити існуючі ключі
ls -la ~/.ssh/

# Якщо є google_compute_engine - добре
# Якщо немає - створити:
ssh-keygen -t rsa -f ~/.ssh/google_compute_engine -C "$(whoami)" -N ""

# Додати публічний ключ в gcloud
gcloud compute config-ssh
```

**Тепер можна підключатись:**
```bash
# Через gcloud (рекомендовано)
gcloud compute ssh a11y-server --zone=us-central1-a

# Або через звичайний ssh
ssh -i ~/.ssh/google_compute_engine [username]@[SERVER_IP]
```

---

## Чеклист Дня 1:

### Google Cloud:
- [ ] Запустив `setup_gcloud.sh`
- [ ] Активував billing (Free Tier)
- [ ] Сервер створено
- [ ] Отримав IP адресу
- [ ] Підключився по SSH
- [ ] Встановив Python пакети на сервері

### Платформи:
- [ ] Зареєструвався на Fable
- [ ] Заповнив профіль з Deque досвідом
- [ ] Зареєструвався на UserTesting
- [ ] Пройшов practice test

### Локально:
- [ ] Встановив Python пакети
- [ ] Playwright працює
- [ ] Тестовий скрипт відкриває браузер

---

## Очікуваний результат:

**Після Дня 1 у тебе є:**
1. ✅ Сервер у Google Cloud (працює 24/7)
2. ✅ Профілі на 2 платформах (чекаємо схвалення)
3. ✅ Локальне середовище готове
4. ✅ SSH доступ налаштований

**Час:** 1.5-2 години

**Наступний крок:** День 2-3 - створення першого робочого прототипу

---

## Troubleshooting

**Проблема: gcloud auth login не відкриває браузер**
```bash
# Альтернатива
gcloud auth login --no-launch-browser
# Скопіюй URL в браузер вручну
```

**Проблема: billing не активується**
```bash
# Перевірити статус
gcloud beta billing accounts list

# Прив'язати вручну через консоль
# https://console.cloud.google.com/billing
```

**Проблема: f1-micro занадто слабкий**
```bash
# Поки що це нормально
# Ми використовуємо його тільки для API
# Браузер буде на твоєму ноутбуці
```

**Проблема: Playwright не встановлює браузер**
```bash
# Вручну
playwright install chromium --with-deps
```

---

**Готовий? Запускай `./setup_gcloud.sh` і пиши, якщо щось не так!**
