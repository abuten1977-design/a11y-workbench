#!/bin/bash
# Деплой dashboard на сервер

echo "🚀 Деплой A11y Oracle Dashboard v2"
echo "=================================="

# 1. Копируем новый api_server
echo "📤 Копирование api_server_v2.py..."
gcloud compute scp api_server_v2.py a11y-server:/tmp/api_server.py --zone=us-central1-a

# 2. Перемещаем на место старого
echo "📝 Обновление на сервере..."
gcloud compute ssh a11y-server --zone=us-central1-a --command="
    sudo mv /tmp/api_server.py /home/butenhome/api_server.py
    sudo chown butenhome:butenhome /home/butenhome/api_server.py
    sudo chmod +x /home/butenhome/api_server.py
"

# 3. Перезапускаем service
echo "🔄 Перезапуск сервиса..."
gcloud compute ssh a11y-server --zone=us-central1-a --command="
    sudo systemctl restart a11y-api
    sleep 2
    sudo systemctl status a11y-api --no-pager
"

# 4. Проверка
echo ""
echo "✅ Деплой завершен!"
echo ""
echo "🌐 Dashboard: http://34.58.51.76:8000/dashboard"
echo "📊 API: http://34.58.51.76:8000/"
echo ""
echo "Проверка здоровья:"
curl -s http://34.58.51.76:8000/health | python3 -m json.tool
