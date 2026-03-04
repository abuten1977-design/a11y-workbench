#!/bin/bash
# Зупинити сервер A11y Oracle

ZONE="us-central1-a"
INSTANCE="a11y-server"

echo "⏸️  Зупинка сервера..."
gcloud compute instances stop $INSTANCE --zone=$ZONE

echo ""
echo "✅ Сервер зупинено"
echo ""
echo "💰 Вартість зупиненого сервера: ~$0.80/міс (тільки диск)"
echo ""
echo "Запустити знову:"
echo "  ./start_server.sh"
