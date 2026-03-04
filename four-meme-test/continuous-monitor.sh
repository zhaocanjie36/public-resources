#!/bin/bash
# 持续监控脚本 - 每 5 分钟运行一次

WORKSPACE="/root/.openclaw/workspace/four-meme-test"
INTERVAL=300  # 5 分钟

cd "$WORKSPACE"

echo "Starting continuous monitoring (every 5 minutes)..."
echo "Press Ctrl+C to stop"

while true; do
    echo ""
    echo "=== Running monitor cycle at $(date) ==="
    python3 monitor.py
    
    echo ""
    echo "Sleeping for $INTERVAL seconds..."
    sleep $INTERVAL
done
