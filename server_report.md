# Звіт: Створення Google Cloud сервера

**Дата:** 03.03.2026, 20:40
**Проект:** A11y Oracle

---

## Що створено

### 1. Google Cloud проект
- **Project ID:** a11y-oracle-1772565307
- **Акаунт:** abuten77@gmail.com
- **Billing:** 01FF2A-B159D4-EA98A9 (підключено)
- **API:** Compute Engine (активовано)

### 2. Сервер (VM Instance)
- **Назва:** a11y-server
- **IP адреса:** 34.58.51.76
- **Зона:** us-central1-a
- **Статус:** RUNNING

---

## Параметри сервера

### Апаратні характеристики:
- **Тип:** e2-micro
- **CPU:** 2 vCPU (shared)
- **RAM:** 1 GB
- **Disk:** 30 GB SSD (pd-standard)
- **Network:** 1 Gbps

### Програмне забезпечення:
- **OS:** Ubuntu 22.04 LTS (Jammy)
- **Python:** 3.10.12
- **Встановлюється автоматично:**
  - python3-pip
  - python3-venv
  - git
  - curl
  - htop
  - redis-server
  - nginx

### Мережа:
- **Внутрішній IP:** 10.128.0.2
- **Зовнішній IP:** 34.58.51.76
- **Firewall:** allow-a11y-http
  - Порт 80 (HTTP)
  - Порт 443 (HTTPS)
  - Порт 8000 (FastAPI)

---

## Вартість (💰 ВАЖЛИВО!)

### Free Tier (безкоштовно):

**e2-micro включений в Free Tier:**
- ✅ 1 e2-micro instance (744 години/місяць)
- ✅ 30 GB HDD
- ✅ 1 GB network egress (US regions)
- ✅ Snapshot storage (перші 5 GB)

**Що це означає:**
- Якщо використовуєш ТІЛЬКИ 1 e2-micro → **$0/міс**
- Якщо не перевищуєш 1 GB трафіку/міс → **$0/міс**

### Що може коштувати:

**Якщо перевищиш ліміти:**
- Network egress >1 GB: ~$0.12/GB
- Додаткові snapshot: ~$0.026/GB/міс
- Якщо створиш 2+ сервери: ~$7/міс за кожен додатковий

**Наш випадок:**
- 1 сервер e2-micro ✅
- API трафік мінімальний (<100 MB/міс) ✅
- Без snapshot поки що ✅

**Очікувана вартість: $0/міс** 🎉

### Моніторинг витрат:

```bash
# Перевірити поточні витрати
gcloud billing accounts list
```

Або в браузері:
https://console.cloud.google.com/billing?project=a11y-oracle-1772565307

**Рекомендація:** Встанови billing alert на $5/міс для безпеки.

---

## SSH підключення

### Варіант 1: Через gcloud (рекомендовано)

```bash
# Підключитись
gcloud compute ssh a11y-server --zone=us-central1-a

# Виконати команду без входу
gcloud compute ssh a11y-server --zone=us-central1-a --command="ls -la"

# Скопіювати файл на сервер
gcloud compute scp local_file.txt a11y-server:~/remote_file.txt --zone=us-central1-a

# Скопіювати файл з сервера
gcloud compute scp a11y-server:~/remote_file.txt ./local_file.txt --zone=us-central1-a
```

### Варіант 2: Через звичайний SSH

```bash
# Підключитись
ssh -i ~/.ssh/google_compute_engine butenhome@34.58.51.76

# З конфігом (зручніше)
# Додай в ~/.ssh/config:
Host a11y-server
    HostName 34.58.51.76
    User butenhome
    IdentityFile ~/.ssh/google_compute_engine

# Тоді просто:
ssh a11y-server
```

### SSH ключі:

**Приватний ключ:** ~/.ssh/google_compute_engine
**Публічний ключ:** ~/.ssh/google_compute_engine.pub

**Fingerprint:** SHA256:g5XT7JXz2eiSEw3A6T4QGhCT21mz7uNQGZMiuQtAOlQ

---

## Управління сервером

### Запуск/Зупинка/Перезавантаження

Створено скрипти в ~/aiwork/:

**start_server.sh** - Запустити сервер
**stop_server.sh** - Зупинити сервер
**restart_server.sh** - Перезавантажити сервер
**status_server.sh** - Статус сервера
**delete_server.sh** - Видалити сервер (обережно!)

### Використання:

```bash
cd ~/aiwork

# Статус
./status_server.sh

# Зупинити (не платиш за CPU/RAM, тільки за диск ~$0.80/міс)
./stop_server.sh

# Запустити
./start_server.sh

# Перезавантажити
./restart_server.sh
```

### Вручну:

```bash
# Статус
gcloud compute instances describe a11y-server --zone=us-central1-a --format="value(status)"

# Зупинити
gcloud compute instances stop a11y-server --zone=us-central1-a

# Запустити
gcloud compute instances start a11y-server --zone=us-central1-a

# Перезавантажити
gcloud compute instances reset a11y-server --zone=us-central1-a

# Видалити (ОБЕРЕЖНО!)
gcloud compute instances delete a11y-server --zone=us-central1-a
```

---

## Чи можу я (AI) виконувати команди на сервері?

### ✅ ТАК, я можу:

Через `execute_bash` я можу виконувати:

```bash
# Підключитись і виконати команду
gcloud compute ssh a11y-server --zone=us-central1-a --command="твоя_команда"
```

**Приклади:**

```bash
# Перевірити Python
gcloud compute ssh a11y-server --zone=us-central1-a --command="python3 --version"

# Встановити пакет
gcloud compute ssh a11y-server --zone=us-central1-a --command="sudo apt install -y htop"

# Створити файл
gcloud compute ssh a11y-server --zone=us-central1-a --command="echo 'test' > ~/test.txt"

# Запустити скрипт
gcloud compute ssh a11y-server --zone=us-central1-a --command="cd ~/a11y-api && python3 server.py"
```

**Обмеження:**
- ❌ Не можу інтерактивні команди (nano, vim)
- ❌ Не можу довгі процеси (>30 сек timeout)
- ✅ Можу створювати файли через heredoc
- ✅ Можу запускати фонові процеси

**Для складних речей:**
1. Я створюю скрипт локально
2. Копіюю на сервер через `gcloud compute scp`
3. Запускаю на сервері

---

## Змінні середовища

Збережено в ~/.bashrc:

```bash
export A11Y_SERVER_IP=34.58.51.76
export A11Y_PROJECT_ID=a11y-oracle-1772565307
export A11Y_ZONE=us-central1-a
```

**Використання:**

```bash
# Перезавантажити змінні
source ~/.bashrc

# Використати
ssh -i ~/.ssh/google_compute_engine $(whoami)@$A11Y_SERVER_IP
gcloud compute ssh a11y-server --zone=$A11Y_ZONE
```

---

## Моніторинг

### Через gcloud:

```bash
# CPU/RAM використання
gcloud compute instances describe a11y-server --zone=us-central1-a

# Логи
gcloud compute instances get-serial-port-output a11y-server --zone=us-central1-a
```

### Через SSH:

```bash
# Підключитись
gcloud compute ssh a11y-server --zone=us-central1-a

# На сервері:
htop              # CPU/RAM в реальному часі
df -h             # Диск
free -h           # RAM
systemctl status  # Сервіси
journalctl -f     # Логи в реальному часі
```

### Через веб-консоль:

https://console.cloud.google.com/compute/instances?project=a11y-oracle-1772565307

---

## Безпека

### Firewall:
- ✅ Тільки порти 80, 443, 8000 відкриті
- ✅ SSH (порт 22) автоматично захищений Google
- ✅ Тільки твій SSH ключ має доступ

### Рекомендації:
1. Не публікуй SSH ключ (~/.ssh/google_compute_engine)
2. Не запускай сервіси від root
3. Регулярно оновлюй систему: `sudo apt update && sudo apt upgrade`
4. Використовуй firewall для обмеження доступу

---

## Backup

### Створити snapshot (резервна копія):

```bash
# Створити
gcloud compute disks snapshot a11y-server \
  --zone=us-central1-a \
  --snapshot-names=a11y-backup-$(date +%Y%m%d)

# Список snapshot
gcloud compute snapshots list

# Відновити з snapshot (якщо щось зламалось)
gcloud compute disks create a11y-server-restored \
  --source-snapshot=a11y-backup-20260303 \
  --zone=us-central1-a
```

**Вартість snapshot:** ~$0.026/GB/міс (30 GB = ~$0.78/міс)

**Рекомендація:** Робити snapshot раз на тиждень після важливих змін.

---

## Наступні кроки

1. ✅ Сервер створено
2. ✅ SSH налаштовано
3. ⏳ Розгорнути FastAPI на сервері
4. ⏳ Створити worker на ноутбуці
5. ⏳ Протестувати систему
6. ⏳ Підключити платежі
7. ⏳ Маркетинг

---

## Корисні посилання

**Google Cloud Console:**
- Проект: https://console.cloud.google.com/home/dashboard?project=a11y-oracle-1772565307
- Compute Engine: https://console.cloud.google.com/compute/instances?project=a11y-oracle-1772565307
- Billing: https://console.cloud.google.com/billing?project=a11y-oracle-1772565307

**Документація:**
- Free Tier: https://cloud.google.com/free
- Compute Engine: https://cloud.google.com/compute/docs

---

## Troubleshooting

**Проблема: Не можу підключитись по SSH**
```bash
# Перевірити статус
gcloud compute instances describe a11y-server --zone=us-central1-a

# Перезапустити SSH metadata
gcloud compute config-ssh --force-key-file-overwrite
```

**Проблема: Сервер не відповідає**
```bash
# Перезавантажити
gcloud compute instances reset a11y-server --zone=us-central1-a
```

**Проблема: Забув IP**
```bash
# Отримати IP
gcloud compute instances describe a11y-server \
  --zone=us-central1-a \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

**Проблема: Витрати зростають**
```bash
# Перевірити що працює
gcloud compute instances list

# Зупинити все крім a11y-server
gcloud compute instances stop [інший_сервер] --zone=[зона]
```

---

**Створено:** 03.03.2026
**Автор:** Kiro AI Assistant
**Проект:** A11y Oracle - Human-validated accessibility testing
