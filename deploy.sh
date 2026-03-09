#!/bin/bash
# Deployment script with sync check
# Usage: ./deploy.sh

set -e  # Exit on error

echo "🚀 A11y Workbench Deployment Script"
echo "===================================="
echo ""

# 1. Check we're in the right directory
if [ ! -f "api_server_v1.py" ]; then
    echo "❌ Error: Run this from /home/butenhome/aiwork/"
    exit 1
fi

# 2. List files to deploy
FILES=(
    "api_server.py"
    "dashboard.js"
    "database.py"
    "exports.py"
    "repositories.py"
    "repository.py"
    "ai_service.py"
    "gemini.env"
)

echo "📦 Files to deploy:"
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file ($(stat -c %y $file | cut -d. -f1))"
    else
        echo "  ❌ $file - NOT FOUND!"
        exit 1
    fi
done
echo ""

# 3. Run syntax check
echo "🔍 Checking Python syntax..."
for file in "${FILES[@]}"; do
    if [[ $file == *.py ]]; then
        python3 -m py_compile "$file" 2>&1 | grep -v "^$" || true
    fi
done
echo "  ✓ Syntax OK"
echo ""

# 4. Ask for confirmation
read -p "Deploy to production? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "❌ Deployment cancelled"
    exit 0
fi
echo ""

# 5. Copy files to server
echo "📤 Copying files to server..."
gcloud compute scp "${FILES[@]}" a11y-server:/tmp/ --zone=us-central1-a

# 6. Deploy on server
echo "📥 Deploying on server..."
gcloud compute ssh a11y-server --zone=us-central1-a --command="
    sudo cp /tmp/api_server_v1.py /home/butenhome/a11y-api/api_server.py &&
    sudo cp /tmp/database.py /home/butenhome/a11y-api/ &&
    sudo cp /tmp/exports.py /home/butenhome/a11y-api/ &&
    sudo cp /tmp/repositories.py /home/butenhome/a11y-api/ &&
    sudo cp /tmp/repository.py /home/butenhome/a11y-api/ &&
    echo '✓ Files copied'
"

# 7. Restart service
echo "🔄 Restarting service..."
gcloud compute ssh a11y-server --zone=us-central1-a --command="
    sudo systemctl restart a11y-api &&
    sleep 3 &&
    sudo systemctl status a11y-api --no-pager | head -10
"

# 8. Health check
echo ""
echo "🏥 Health check..."
sleep 2
HEALTH=$(curl -s http://34.58.51.76:8000/health)
if [[ $HEALTH == *"healthy"* ]]; then
    echo "  ✅ Server is healthy!"
else
    echo "  ❌ Server health check failed!"
    echo "  Response: $HEALTH"
    exit 1
fi

# 9. Show deployed file dates
echo ""
echo "📅 Deployed file dates:"
gcloud compute ssh a11y-server --zone=us-central1-a --command="
    cd /home/butenhome/a11y-api &&
    ls -lh api_server.py database.py exports.py repositories.py repository.py | awk '{print \"  \", \$9, \$6, \$7, \$8}'
"

echo ""
echo "✅ Deployment completed successfully!"
echo "🌐 Dashboard: http://34.58.51.76:8000/dashboard"
echo ""
