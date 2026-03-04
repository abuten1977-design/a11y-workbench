#!/bin/bash
# Перезавантажити сервер A11y Oracle

ZONE="us-central1-a"
INSTANCE="a11y-server"

echo "🔄 Перезавантаження сервера..."
gcloud compute instances reset $INSTANCE --zone=$ZONE

echo ""
echo "⏳ Чекаємо поки сервер перезавантажиться (30 сек)..."
sleep 30

echo ""
echo "✅ Сервер перезавантажено"
echo ""
echo "Перевірити статус:"
echo "  ./status_server.sh"
