#!/bin/bash
# Очищення черги завдань

SERVER="http://34.58.51.76:8000"

echo "🗑️  Очищення черги"
echo ""

# Отримати всі job_id з черги
job_ids=$(curl -s $SERVER/api/v1/queue | python3 -c "
import sys, json
data = json.load(sys.stdin)
for job in data['jobs']:
    print(job['job_id'])
")

if [ -z "$job_ids" ]; then
    echo "✅ Черга вже порожня"
    exit 0
fi

# Видалити кожен job
count=0
for job_id in $job_ids; do
    echo "🗑️  Видаляю job: $job_id"
    curl -s -X DELETE $SERVER/api/v1/queue/$job_id > /dev/null
    ((count++))
done

echo ""
echo "✅ Видалено $count завдань"
echo ""

# Перевірити чергу
echo "📊 Поточна черга:"
curl -s $SERVER/api/v1/queue | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Всього: {data['total']} завдань\")
"
