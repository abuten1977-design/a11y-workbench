#!/bin/bash
# Створення оптимального сервера для A11y Oracle

PROJECT_ID="a11y-oracle-1772565307"
ZONE="us-central1-a"
INSTANCE_NAME="a11y-server"

echo "🚀 Створення сервера для A11y Oracle"
echo ""
echo "Параметри:"
echo "  Тип: f1-micro (Free Tier)"
echo "  CPU: 1 vCPU (shared)"
echo "  RAM: 0.6 GB"
echo "  Disk: 30 GB SSD"
echo "  OS: Ubuntu 22.04 LTS"
echo "  Ціна: $0/міс"
echo ""

# Перевірка чи вже існує
EXISTING=$(gcloud compute instances list --filter="name=$INSTANCE_NAME" --format="value(name)" 2>/dev/null)

if [ ! -z "$EXISTING" ]; then
    echo "⚠️  Сервер $INSTANCE_NAME вже існує"
    echo ""
    echo "Видалити і створити новий? (y/n)"
    read answer
    if [ "$answer" = "y" ]; then
        echo "Видаляємо старий сервер..."
        gcloud compute instances delete $INSTANCE_NAME --zone=$ZONE --quiet
    else
        echo "Виходимо..."
        exit 0
    fi
fi

# Активація API
echo "🔌 Активація Compute Engine API..."
gcloud services enable compute.googleapis.com

# Створення сервера
echo "💻 Створення сервера..."
gcloud compute instances create $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --machine-type=f1-micro \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --tags=http-server,https-server \
    --create-disk=auto-delete=yes,boot=yes,device-name=$INSTANCE_NAME,image=projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20250131,mode=rw,size=30,type=pd-standard \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=project=a11y-oracle,env=production \
    --reservation-affinity=any \
    --metadata=startup-script='#!/bin/bash
# Startup script для автоматичного налаштування

# Оновлення системи
apt-get update
apt-get upgrade -y

# Встановлення базових пакетів
apt-get install -y \
    python3-pip \
    python3-venv \
    git \
    curl \
    htop \
    redis-server \
    nginx

# Налаштування Redis
systemctl enable redis-server
systemctl start redis-server

# Створення користувача для додатку
useradd -m -s /bin/bash a11y || true

# Створення директорії
mkdir -p /opt/a11y-api
chown a11y:a11y /opt/a11y-api

echo "✅ Startup script completed" > /var/log/startup-script.log
'

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Сервер створено!"
    echo ""
    
    # Firewall
    echo "🔥 Налаштування firewall..."
    gcloud compute firewall-rules create allow-a11y-http \
        --project=$PROJECT_ID \
        --allow tcp:80,tcp:8000,tcp:443 \
        --source-ranges 0.0.0.0/0 \
        --target-tags http-server \
        --description="Allow HTTP/HTTPS for A11y API" 2>&1 | grep -v "already exists" || true
    
    # Отримання IP
    echo ""
    echo "⏳ Чекаємо поки сервер запуститься (30 сек)..."
    sleep 30
    
    SERVER_IP=$(gcloud compute instances describe $INSTANCE_NAME \
        --zone=$ZONE \
        --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎉 ВСЕ ГОТОВО!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📍 IP адреса: $SERVER_IP"
    echo "🔑 SSH підключення:"
    echo ""
    echo "   gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
    echo ""
    echo "Або:"
    echo "   ssh -i ~/.ssh/google_compute_engine $(whoami)@$SERVER_IP"
    echo ""
    echo "Зберігаємо змінні..."
    echo "export A11Y_SERVER_IP=$SERVER_IP" >> ~/.bashrc
    echo "export A11Y_PROJECT_ID=$PROJECT_ID" >> ~/.bashrc
    echo "export A11Y_ZONE=$ZONE" >> ~/.bashrc
    
    echo ""
    echo "📊 Моніторинг:"
    echo "   https://console.cloud.google.com/compute/instances?project=$PROJECT_ID"
    echo ""
    echo "💰 Вартість: $0/міс (Free Tier)"
    echo ""
    
else
    echo ""
    echo "❌ Помилка при створенні сервера"
    echo "Перевір billing: https://console.cloud.google.com/billing?project=$PROJECT_ID"
fi
