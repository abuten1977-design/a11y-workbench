#!/bin/bash
# Запустити сервер A11y Oracle

ZONE="us-central1-a"
INSTANCE="a11y-server"

echo "▶️  Запуск сервера..."
gcloud compute instances start $INSTANCE --zone=$ZONE

echo ""
echo "⏳ Чекаємо поки сервер запуститься (15 сек)..."
sleep 15

IP=$(gcloud compute instances describe $INSTANCE --zone=$ZONE --format="value(networkInterfaces[0].accessConfigs[0].natIP)")

echo ""
echo "✅ Сервер запущено"
echo ""
echo "IP: $IP"
echo ""
echo "Підключитись:"
echo "  gcloud compute ssh $INSTANCE --zone=$ZONE"
