# Управління чергою завдань

## 📊 Перевірити чергу

```bash
curl http://34.58.51.76:8000/api/v1/queue | python3 -m json.tool
```

Або:
```bash
curl -s http://34.58.51.76:8000/api/v1/queue | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'Всього: {data[\"total\"]} завдань')
for i, job in enumerate(data['jobs'], 1):
    print(f'{i}. {job[\"url\"]}')
"
```

---

## ➕ Створити завдання

### Одне завдання:
```bash
curl -X POST http://34.58.51.76:8000/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com", "priority": 1}'
```

### Кілька тестових завдань:
```bash
cd ~/aiwork
./create_test_jobs.sh
```

Створить 5 завдань:
- GitHub
- Wikipedia
- StackOverflow
- Reddit
- Twitter

---

## 🗑️ Видалити завдання

### Одне завдання:
```bash
curl -X DELETE http://34.58.51.76:8000/api/v1/queue/{job_id}
```

### Очистити всю чергу:
```bash
cd ~/aiwork
./clear_queue.sh
```

---

## 📈 Перевірити результати

```bash
curl http://34.58.51.76:8000/api/v1/check/{job_id} | python3 -m json.tool
```

---

## 🔄 Типовий workflow

### 1. Очистити стару чергу
```bash
./clear_queue.sh
```

### 2. Створити тестові завдання
```bash
./create_test_jobs.sh
```

### 3. Запустити worker
```bash
python3 worker.py
```

### 4. Тестувати
- Worker відкриває браузер
- Ти тестуєш зі скрінрідером
- Натискаєш Ctrl+Alt+1/2/3
- Worker переходить до наступного

### 5. Перевірити статистику
Worker показує:
```
📊 Всього: 5 завдань, $15.00
⏱️ Середній час: 2.5 хв
```

---

## 🐛 Troubleshooting

### Worker відкриває один сайт багато разів

**Причина:** В черзі тільки одне завдання, яке не видаляється

**Рішення:**
1. Зупини worker (Ctrl+C)
2. Очисти чергу: `./clear_queue.sh`
3. Створи нові завдання: `./create_test_jobs.sh`
4. Запусти worker знову

### Черга порожня

```bash
# Створити тестові завдання
./create_test_jobs.sh
```

### Worker не відповідає

```bash
# Перевірити що сервер працює
curl http://34.58.51.76:8000/health

# Якщо не працює
cd ~/aiwork
./status_server.sh
```

---

## 📝 Корисні команди

```bash
# Статус сервера
./status_server.sh

# Перевірити API
curl http://34.58.51.76:8000/health

# Перевірити чергу
curl http://34.58.51.76:8000/api/v1/queue

# Створити тестові завдання
./create_test_jobs.sh

# Очистити чергу
./clear_queue.sh

# Запустити worker
python3 worker.py
```

---

## ✅ Зараз в черзі

```
1. https://github.com/
2. https://wikipedia.org/
3. https://stackoverflow.com/
```

**Готово до тестування!**

Запускай: `python3 worker.py`
