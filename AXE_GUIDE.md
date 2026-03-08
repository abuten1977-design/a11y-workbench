# Инструкция по использованию axe-core

## 🎯 Что установлено:

1. **axe-core CLI** - автоматическое тестирование доступности
2. **Puppeteer** - headless браузер для запуска тестов
3. **Парсер результатов** - преобразует JSON в читаемый формат

---

## 📝 Как использовать:

### Шаг 1: Запусти тест на сайте

```bash
cd /home/butenhome/aiwork
node axe_runner.js <URL>
```

**Пример:**
```bash
node axe_runner.js https://example.com
node axe_runner.js https://www.dr.dk
node axe_runner.js https://www.coop.dk
```

**Результат:**
- Создается файл `axe_results.json` с полными результатами
- В консоли показывается краткая сводка

---

### Шаг 2: Посмотри детальный отчет

```bash
python3 parse_axe.py axe_results.json
```

**Что покажет:**
- Все проблемы сгруппированные по severity (critical/serious/moderate/minor)
- Для каждой проблемы:
  - Заголовок
  - WCAG критерий
  - Описание
  - Пример HTML кода
  - Как исправить (ссылка)
  - Сколько элементов затронуто

---

### Шаг 3: Скопируй в A11y Workbench

В конце отчета будет секция **"READY FOR A11Y WORKBENCH"**

Пример:
```
Title: Document should have one main landmark
Severity: moderate
WCAG: 
Description: Ensure the document has a main landmark
Affected: 1 elements
Help: https://dequeuniversity.com/rules/axe/4.11/landmark-one-main
```

Скопируй эти данные в систему через Quick Capture или Add Issue.

---

## 🔄 Рабочий процесс:

### Вариант A: Автомат → Ручное тестирование

```
1. node axe_runner.js https://example.com
2. python3 parse_axe.py axe_results.json
3. Скопируй проблемы в A11y Workbench (Quick Capture)
4. Открой сайт с NVDA
5. Проверь каждую проблему вручную
6. Добавь evidence (screen reader output, код)
7. Найди дополнительные проблемы (которые axe не нашел)
8. Экспортируй отчет
```

### Вариант B: Ручное → Автомат для проверки

```
1. Открой сайт с NVDA
2. Тестируй вручную, записывай проблемы
3. node axe_runner.js https://example.com
4. Сравни - что нашел ты vs что нашел axe
5. Добавь пропущенные проблемы
6. Экспортируй отчет
```

---

## 📊 Что axe находит хорошо:

✅ **Автоматически детектируемые проблемы:**
- Отсутствующие alt текст на изображениях
- Проблемы с контрастом цветов
- Неправильные ARIA атрибуты
- Отсутствующие labels на формах
- Проблемы с HTML структурой
- Дублирующиеся ID
- Проблемы с landmarks

---

## ⚠️ Что axe НЕ находит:

❌ **Требует ручного тестирования:**
- Логический порядок табуляции
- Качество alt текстов (есть ли, но бессмысленный)
- Keyboard traps
- Focus management в модальных окнах
- Screen reader announcements
- Динамический контент (live regions)
- Сложные интерактивные компоненты
- Контекстуальные проблемы

**Поэтому твое ручное тестирование критически важно!**

---

## 💡 Советы:

1. **Используй axe как отправную точку** - быстро найди очевидные проблемы
2. **Не доверяй слепо** - проверяй каждую проблему вручную
3. **Добавляй контекст** - axe дает техническое описание, ты добавляешь user impact
4. **Ищи больше** - axe находит ~30%, ты найдешь остальные 70%
5. **Документируй разницу** - покажи работодателю что ты нашел vs что нашел автомат

---

## 🎯 Пример для портфолио:

**Отчет может содержать:**

```markdown
# Accessibility Audit: Example Site

## Methodology
- Automated testing: axe-core 4.11.1
- Manual testing: NVDA 2024.1 + Chrome 120
- Standards: WCAG 2.2 Level AA

## Findings Summary
- Total issues: 23
  - Automated (axe): 8 issues
  - Manual testing: 15 additional issues
  
## Critical Issues (Manual Testing Only)
1. Keyboard trap in modal dialog
2. Submit button not keyboard accessible
3. Form errors not announced to screen readers

## Serious Issues
4. [axe] Missing alt text on 5 images
5. [Manual] Alt text present but not descriptive
...
```

**Это показывает:**
- Ты умеешь работать с автоматическими инструментами
- Но главное - ты находишь проблемы, которые автоматика пропускает
- Твоя ценность как специалиста

---

## 📁 Файлы:

- `axe_runner.js` - запускает тест
- `parse_axe.py` - парсит результаты
- `axe_results.json` - результаты последнего теста (перезаписывается)

---

## 🆘 Проблемы:

**Ошибка "Cannot find module":**
```bash
cd /home/butenhome/aiwork
npm install
```

**Браузер не запускается:**
```bash
# Проверь установку
node -e "require('puppeteer').launch().then(b => b.close())"
```

**Долго работает:**
- Это нормально, axe анализирует всю страницу
- Обычно 10-30 секунд на страницу

---

**Готово к использованию!** 🚀
