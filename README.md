# A11y Oracle - Швидкий старт

## Сервер створено ✅

**IP:** 34.58.51.76
**Тип:** e2-micro (Free Tier)
**Вартість:** $0/міс

---

## Швидкі команди

### Статус сервера
```bash
cd ~/aiwork
./status_server.sh
```

### Підключитись по SSH
```bash
gcloud compute ssh a11y-server --zone=us-central1-a
```

### Управління
```bash
./stop_server.sh      # Зупинити
./start_server.sh     # Запустити
./restart_server.sh   # Перезавантажити
```

---

## Файли в ~/aiwork/

**Документація:**
- `server_report.md` - Повний звіт про сервер
- `why_server_needed.md` - Навіщо потрібен сервер
- `plan_4_weeks.md` - План на 4 тижні
- `analiz_rynka_realnost.md` - Аналіз ринку
- `day1_instructions.md` - Інструкції День 1

**Скрипти управління:**
- `status_server.sh` - Статус
- `start_server.sh` - Запустити
- `stop_server.sh` - Зупинити
- `restart_server.sh` - Перезавантажити
- `delete_server.sh` - Видалити (обережно!)

**Налаштування:**
- `setup_ssh.sh` - Налаштування SSH
- `create_server.sh` - Створення сервера

---

## Наступні кроки

1. ✅ Сервер створено
2. ✅ FastAPI розгорнуто
3. ⏳ Створити worker
4. ⏳ Тестування
5. ⏳ Платежі
6. ⏳ Маркетинг

---

## API працює! 🎉

**URL:** http://34.58.51.76:8000

**Документація (Swagger):** http://34.58.51.76:8000/docs

**Endpoints:**
- `GET /` - API info
- `GET /health` - Health check
- `POST /api/v1/check` - Створити завдання
- `GET /api/v1/check/{job_id}` - Статус завдання
- `GET /api/v1/queue` - Черга (для worker)
- `POST /api/v1/result/{job_id}` - Відправити результат

**Управління сервісом:**
```bash
# Статус
gcloud compute ssh a11y-server --zone=us-central1-a --command="sudo systemctl status a11y-api"

# Перезапустити
gcloud compute ssh a11y-server --zone=us-central1-a --command="sudo systemctl restart a11y-api"

# Логи
gcloud compute ssh a11y-server --zone=us-central1-a --command="sudo journalctl -u a11y-api -f"
```

**Детальний план:** `plan_4_weeks.md`

---

## Питання?

Читай `server_report.md` - там все детально описано.
