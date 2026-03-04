#!/bin/bash
# Статус сервера A11y Oracle

ZONE="us-central1-a"
INSTANCE="a11y-server"

echo "📊 Статус сервера A11y Oracle"
echo ""

STATUS=$(gcloud compute instances describe $INSTANCE --zone=$ZONE --format="value(status)")
IP=$(gcloud compute instances describe $INSTANCE --zone=$ZONE --format="value(networkInterfaces[0].accessConfigs[0].natIP)")

echo "Назва: $INSTANCE"
echo "Зона: $ZONE"
echo "IP: $IP"
echo "Статус: $STATUS"
echo ""

if [ "$STATUS" = "RUNNING" ]; then
    echo "✅ Сервер працює"
    echo ""
    echo "Підключитись:"
    echo "  gcloud compute ssh $INSTANCE --zone=$ZONE"
    echo "  ssh -i ~/.ssh/google_compute_engine $(whoami)@$IP"
elif [ "$STATUS" = "TERMINATED" ]; then
    echo "⏸️  Сервер зупинено"
    echo ""
    echo "Запустити:"
    echo "  ./start_server.sh"
else
    echo "⚠️  Статус: $STATUS"
fi
