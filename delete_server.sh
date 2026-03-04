#!/bin/bash
# ВИДАЛИТИ сервер A11y Oracle (ОБЕРЕЖНО!)

ZONE="us-central1-a"
INSTANCE="a11y-server"

echo "⚠️  УВАГА! Це видалить сервер НАЗАВЖДИ!"
echo ""
echo "Всі дані на сервері будуть втрачені."
echo ""
echo "Продовжити? (yes/no)"
read answer

if [ "$answer" != "yes" ]; then
    echo "Скасовано."
    exit 0
fi

echo ""
echo "Ти впевнений? Напиши 'DELETE' великими літерами:"
read confirm

if [ "$confirm" != "DELETE" ]; then
    echo "Скасовано."
    exit 0
fi

echo ""
echo "🗑️  Видалення сервера..."
gcloud compute instances delete $INSTANCE --zone=$ZONE --quiet

echo ""
echo "✅ Сервер видалено"
echo ""
echo "Створити новий:"
echo "  ./create_server.sh"
