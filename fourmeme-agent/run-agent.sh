#!/bin/bash
# Four.meme Agent 监控脚本
# 每小时检查一次市场并执行交易决策

export PNPM_HOME="/root/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"

cd /root/.openclaw/workspace/fourmeme-agent

echo "=== $(date) ==="
node agent.js

# 如果有错误，记录到日志
if [ $? -ne 0 ]; then
    echo "Agent execution failed at $(date)" >> error.log
fi
