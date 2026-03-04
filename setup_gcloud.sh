#!/bin/bash
# Налаштування Google Cloud для A11y Oracle

echo "🚀 Налаштування Google Cloud"
echo ""

# Крок 1: Створення нової конфігурації
echo "📝 Крок 1: Створення конфігурації"
gcloud config configurations create a11y-oracle

# Крок 2: Логін (відкриє браузер)
echo "🔐 Крок 2: Авторизація"
echo "Зараз відкриється браузер для логіну..."
gcloud auth login

# Крок 3: Створення проекту
echo "📦 Крок 3: Створення проекту"
PROJECT_ID="a11y-oracle-$(date +%s)"
echo "Project ID: $PROJECT_ID"

gcloud projects create $PROJECT_ID --name="A11y Oracle"
gcloud config set project $PROJECT_ID

# Крок 4: Активація billing (потрібно вручну)
echo ""
echo "⚠️  ВАЖЛИВО: Потрібно активувати billing"
echo "Відкрий: https://console.cloud.google.com/billing/linkedaccount?project=$PROJECT_ID"
echo ""
echo "Після активації натисни Enter..."
read

# Крок 5: Активація API
echo "🔌 Крок 5: Активація Compute Engine API"
gcloud services enable compute.googleapis.com

# Крок 6: Створення SSH ключів (якщо немає)
if [ ! -f ~/.ssh/google_compute_engine ]; then
    echo "🔑 Крок 6: Створення SSH ключів"
    ssh-keygen -t rsa -f ~/.ssh/google_compute_engine -C "$(whoami)" -N ""
else
    echo "✅ SSH ключі вже існують"
fi

# Крок 7: Створення f1-micro instance (Free Tier)
echo "💻 Крок 7: Створення сервера"
gcloud compute instances create a11y-server \
    --zone=us-central1-a \
    --machine-type=f1-micro \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=30GB \
    --boot-disk-type=pd-standard \
    --tags=http-server,https-server \
    --metadata=startup-script='#!/bin/bash
apt-get update
apt-get install -y python3-pip python3-venv
'

# Крок 8: Налаштування firewall
echo "🔥 Крок 8: Налаштування firewall"
gcloud compute firewall-rules create allow-http \
    --allow tcp:80,tcp:8000 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server

# Крок 9: Отримання IP
echo ""
echo "✅ Готово!"
echo ""
SERVER_IP=$(gcloud compute instances describe a11y-server \
    --zone=us-central1-a \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "📍 IP адреса сервера: $SERVER_IP"
echo ""
echo "Збережи цей IP:"
echo "export A11Y_SERVER_IP=$SERVER_IP" >> ~/.bashrc
echo "export A11Y_SERVER_IP=$SERVER_IP"
echo ""
echo "Підключення:"
echo "gcloud compute ssh a11y-server --zone=us-central1-a"
