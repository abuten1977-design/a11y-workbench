#!/bin/bash
# Створення тестових завдань для worker

SERVER="http://34.58.51.76:8000"

echo "🧪 Створення тестових завдань"
echo ""

# Масив тестових URL
urls=(
    "https://github.com"
    "https://wikipedia.org"
    "https://stackoverflow.com"
    "https://reddit.com"
    "https://twitter.com"
)

# Створити завдання для кожного URL
for url in "${urls[@]}"; do
    echo "📝 Створюю завдання: $url"
    
    job_id=$(curl -s -X POST $SERVER/api/v1/check \
        -H "Content-Type: application/json" \
        -d "{\"url\": \"$url\", \"priority\": 1}" \
        | python3 -c "import sys, json; print(json.load(sys.stdin)['job_id'])")
    
    echo "   ✅ Job ID: $job_id"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Створено ${#urls[@]} завдань"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Показати чергу
echo "📊 Поточна черга:"
curl -s $SERVER/api/v1/queue | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Всього: {data['total']} завдань\")
print()
for i, job in enumerate(data['jobs'], 1):
    print(f\"{i}. {job['url']}\")
    print(f\"   Job ID: {job['job_id']}\")
    print()
"

echo ""
echo "🚀 Тепер запусти worker:"
echo "   python3 worker.py"
