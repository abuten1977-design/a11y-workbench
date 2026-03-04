#!/bin/bash
# Налаштування SSH ключів для Google Cloud

echo "🔑 Налаштування SSH ключів"
echo ""

# Перевірка існуючих ключів
if [ -f ~/.ssh/google_compute_engine ]; then
    echo "✅ Ключ ~/.ssh/google_compute_engine вже існує"
    echo ""
    echo "Використати існуючий? (y/n)"
    read answer
    if [ "$answer" != "y" ]; then
        echo "Створюємо новий..."
        mv ~/.ssh/google_compute_engine ~/.ssh/google_compute_engine.backup
        mv ~/.ssh/google_compute_engine.pub ~/.ssh/google_compute_engine.pub.backup
    else
        echo "Використовуємо існуючий ключ"
    fi
fi

# Створення нового ключа (якщо потрібно)
if [ ! -f ~/.ssh/google_compute_engine ]; then
    echo "Створюємо новий SSH ключ..."
    ssh-keygen -t rsa -b 2048 -f ~/.ssh/google_compute_engine -C "abuten77@gmail.com" -N ""
    echo "✅ Ключ створено"
fi

# Налаштування прав
chmod 600 ~/.ssh/google_compute_engine
chmod 644 ~/.ssh/google_compute_engine.pub

# Додавання в gcloud
echo ""
echo "Додаємо ключ в gcloud metadata..."
gcloud compute config-ssh

echo ""
echo "✅ SSH налаштовано!"
echo ""
echo "Публічний ключ:"
cat ~/.ssh/google_compute_engine.pub
echo ""
echo "Тепер можна підключатись до серверів Google Cloud"
