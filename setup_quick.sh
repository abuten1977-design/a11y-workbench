#!/bin/bash
# Швидке налаштування для проекту a11y-oracle-1772565307

PROJECT_ID="a11y-oracle-1772565307"

echo "📦 Проект: $PROJECT_ID"
echo "👤 Акаунт: abuten77@gmail.com"
echo ""

# Крок 1: Перевірка billing
echo "🔍 Перевірка billing..."
BILLING_ENABLED=$(gcloud beta billing projects describe $PROJECT_ID --format="value(billingEnabled)" 2>/dev/null)

if [ "$BILLING_ENABLED" != "True" ]; then
    echo ""
    echo "⚠️  Потрібно активувати billing (Free Tier - безкоштовно)"
    echo ""
    echo "Відкрий це посилання в браузері:"
    echo "https://console.cloud.google.com/billing/linkedaccount?project=$PROJECT_ID"
    echo ""
    echo "Кроки:"
    echo "1. Натисни 'Link a billing account'"
    echo "2. Створи новий billing account (якщо немає)"
    echo "3. Введи дані карти (НЕ знімуть гроші, тільки для верифікації)"
    echo "4. Активуй Free Tier"
    echo ""
    echo "Після активації натисни Enter..."
    read
fi

# Крок 2: Активація Compute Engine API
echo "🔌 Активація Compute Engine API..."
gcloud services enable compute.googleapis.com

# Крок 3: SSH ключі
if [ ! -f ~/.ssh/google_compute_engine ]; then
    echo "🔑 Створення SSH ключів..."
    ssh-keygen -t rsa -f ~/.ssh/google_compute_engine -C "abuten77@gmail.com" -N ""
else
    echo "✅ SSH ключі вже є"
fi

# Крок 4: Створення f1-micro instance
echo "💻 Створення сервера (f1-micro, Free Tier)..."
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
apt-get install -y python3-pip python3-venv git
' 2>&1

# Крок 5: Firewall
echo "🔥 Налаштування firewall..."
gcloud compute firewall-rules create allow-a11y-api \
    --allow tcp:80,tcp:8000,tcp:443 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server 2>&1 || echo "Firewall rule вже існує"

# Крок 6: Отримання IP
echo ""
echo "✅ Готово!"
echo ""
SERVER_IP=$(gcloud compute instances describe a11y-server \
    --zone=us-central1-a \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "📍 IP адреса сервера: $SERVER_IP"
echo ""
echo "Зберігаємо в ~/.bashrc..."
echo "export A11Y_SERVER_IP=$SERVER_IP" >> ~/.bashrc
echo "export A11Y_PROJECT_ID=$PROJECT_ID" >> ~/.bashrc

echo ""
echo "🎉 Все готово!"
echo ""
echo "Підключитись до сервера:"
echo "  gcloud compute ssh a11y-server --zone=us-central1-a"
echo ""
echo "Або через звичайний SSH:"
echo "  ssh -i ~/.ssh/google_compute_engine $(whoami)@$SERVER_IP"
