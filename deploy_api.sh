#!/bin/bash
# Розгортання FastAPI на сервері

set -e  # Вийти при помилці

ZONE="us-central1-a"
INSTANCE="a11y-server"
REMOTE_DIR="/home/butenhome/a11y-api"

echo "🚀 Розгортання A11y Oracle API"
echo ""

# Крок 1: Копіювання файлів на сервер
echo "📦 Крок 1: Копіювання файлів..."
gcloud compute scp api_server.py $INSTANCE:~/ --zone=$ZONE
gcloud compute scp requirements.txt $INSTANCE:~/ --zone=$ZONE
gcloud compute scp a11y-api.service $INSTANCE:~/ --zone=$ZONE

# Крок 2: Налаштування на сервері
echo "⚙️  Крок 2: Налаштування на сервері..."
gcloud compute ssh $INSTANCE --zone=$ZONE --command="
set -e

# Створити директорію
mkdir -p $REMOTE_DIR
mv ~/api_server.py $REMOTE_DIR/
mv ~/requirements.txt $REMOTE_DIR/

# Створити venv
cd $REMOTE_DIR
python3 -m venv venv

# Встановити залежності
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo '✅ Python пакети встановлено'
"

# Крок 3: Налаштування systemd service
echo "🔧 Крок 3: Налаштування автозапуску..."
gcloud compute ssh $INSTANCE --zone=$ZONE --command="
set -e

# Копіювати service файл
sudo mv ~/a11y-api.service /etc/systemd/system/

# Перезавантажити systemd
sudo systemctl daemon-reload

# Увімкнути і запустити сервіс
sudo systemctl enable a11y-api
sudo systemctl start a11y-api

# Перевірити статус
sleep 3
sudo systemctl status a11y-api --no-pager

echo '✅ Сервіс запущено'
"

# Крок 4: Перевірка
echo ""
echo "🧪 Крок 4: Тестування API..."
sleep 5

SERVER_IP=\$(gcloud compute instances describe $INSTANCE --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo ""
echo "Тестуємо http://\$SERVER_IP:8000"
curl -s http://\$SERVER_IP:8000 | python3 -m json.tool || echo "⚠️  API ще не відповідає, чекай 10-20 сек"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Розгортання завершено!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "API доступний:"
echo "  http://\$SERVER_IP:8000"
echo ""
echo "Документація:"
echo "  http://\$SERVER_IP:8000/docs"
echo ""
echo "Перевірити статус на сервері:"
echo "  gcloud compute ssh $INSTANCE --zone=$ZONE --command='sudo systemctl status a11y-api'"
echo ""
echo "Логи:"
echo "  gcloud compute ssh $INSTANCE --zone=$ZONE --command='sudo journalctl -u a11y-api -f'"
