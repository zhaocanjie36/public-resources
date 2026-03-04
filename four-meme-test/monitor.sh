#!/bin/bash
# Four.meme Token Monitor
# 监控新创建的 token 并分析

set -e

WORKSPACE="/root/.openclaw/workspace/four-meme-test"
DATA_DIR="$WORKSPACE/data"
LOG_FILE="$WORKSPACE/monitor.log"

mkdir -p "$DATA_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Four.meme Monitor Started ==="

# 获取最新区块号
LATEST_BLOCK=$(curl -s https://bsc-dataseed.binance.org \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  | jq -r '.result' | xargs printf "%d")

log "Latest block: $LATEST_BLOCK"

# 监控最近 100 个区块的事件
FROM_BLOCK=$((LATEST_BLOCK - 100))
log "Fetching events from block $FROM_BLOCK to $LATEST_BLOCK"

# 获取事件
fourmeme events $FROM_BLOCK $LATEST_BLOCK > "$DATA_DIR/events_$(date +%s).json"

log "Events saved to $DATA_DIR/events_$(date +%s).json"

# 分析 TokenCreate 事件
TOKEN_CREATES=$(cat "$DATA_DIR/events_$(date +%s).json" | jq '[.[] | select(.eventName == "TokenCreate")]')
TOKEN_COUNT=$(echo "$TOKEN_CREATES" | jq 'length')

log "Found $TOKEN_COUNT new tokens created"

# 如果有新 token，获取详情
if [ "$TOKEN_COUNT" -gt 0 ]; then
    echo "$TOKEN_CREATES" | jq -c '.[]' | while read -r token; do
        TOKEN_ADDR=$(echo "$token" | jq -r '.args.token')
        CREATOR=$(echo "$token" | jq -r '.args.creator')
        
        log "New token: $TOKEN_ADDR by $CREATOR"
        
        # 获取 token 详情
        fourmeme token-get "$TOKEN_ADDR" > "$DATA_DIR/token_${TOKEN_ADDR}.json" 2>/dev/null || true
        
        # 检查是否是 Agent 创建
        IS_AGENT=$(fourmeme 8004-balance "$CREATOR" 2>/dev/null | jq -r '.balance')
        if [ "$IS_AGENT" != "0" ]; then
            log "  ⚠️  Created by AGENT wallet!"
        fi
    done
fi

# 获取当前热门 token
log "Fetching hot tokens..."
fourmeme token-rankings Hot > "$DATA_DIR/hot_tokens_$(date +%s).json"

HOT_COUNT=$(cat "$DATA_DIR/hot_tokens_$(date +%s).json" | jq '.data | length')
log "Hot tokens: $HOT_COUNT"

# 分析 top 3
cat "$DATA_DIR/hot_tokens_$(date +%s).json" | jq -r '.data[:3] | .[] | 
  "  \(.name) (\(.symbol)): $\(.marketCapUsd | tonumber | floor) market cap, \(.holders) holders"' | while read -r line; do
    log "$line"
done

log "=== Monitor cycle complete ==="
