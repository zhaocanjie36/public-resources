#!/usr/bin/env python3
"""
Four.meme Token Monitor - Python Version
监控新创建的 token 并分析市场数据
"""

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace/four-meme-test")
DATA_DIR = WORKSPACE / "data"
LOG_FILE = WORKSPACE / "monitor.log"

DATA_DIR.mkdir(exist_ok=True)

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def run_fourmeme(cmd):
    """运行 fourmeme 命令并返回 JSON 结果"""
    try:
        result = subprocess.run(
            f"cd {WORKSPACE} && npx fourmeme {cmd}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            log(f"Error running: {cmd}")
            log(f"  {result.stderr}")
            return None
    except Exception as e:
        log(f"Exception: {e}")
        return None

def monitor_new_tokens():
    """监控最新创建的 token"""
    log("=== Fetching newest tokens ===")
    
    data = run_fourmeme("token-list --pageSize=10 --orderBy=Time")
    if not data or 'data' not in data:
        log("Failed to fetch token list")
        return []
    
    tokens = data['data']
    log(f"Found {len(tokens)} newest tokens")
    
    # 保存数据
    timestamp = int(time.time())
    output_file = DATA_DIR / f"new_tokens_{timestamp}.json"
    with open(output_file, "w") as f:
        json.dump(tokens, f, indent=2)
    
    # 分析前 3 个
    for i, token in enumerate(tokens[:3], 1):
        name = token.get('name', 'Unknown')
        symbol = token.get('symbol', '?')
        address = token.get('address', '')
        mcap = float(token.get('marketCapUsd', 0))
        holders = token.get('holders', 0)
        progress = float(token.get('progress', 0)) * 100
        
        log(f"  #{i} {name} ({symbol})")
        log(f"      Address: {address}")
        log(f"      Market Cap: ${mcap:.2f}")
        log(f"      Holders: {holders}")
        log(f"      Progress: {progress:.1f}%")
    
    return tokens

def monitor_hot_tokens():
    """监控热门 token"""
    log("=== Fetching hot tokens ===")
    
    data = run_fourmeme("token-rankings Hot")
    if not data or 'data' not in data:
        log("Failed to fetch hot tokens")
        return []
    
    tokens = data['data']
    log(f"Found {len(tokens)} hot tokens")
    
    # 保存数据
    timestamp = int(time.time())
    output_file = DATA_DIR / f"hot_tokens_{timestamp}.json"
    with open(output_file, "w") as f:
        json.dump(tokens, f, indent=2)
    
    # 分析 top 5
    for i, token in enumerate(tokens[:5], 1):
        name = token.get('name', 'Unknown')
        symbol = token.get('symbol', '?')
        mcap = float(token.get('marketCapUsd', 0))
        trading = float(token.get('tradingUsd', 0))
        holders = token.get('holders', 0)
        
        log(f"  #{i} {name} ({symbol})")
        log(f"      Market Cap: ${mcap:.2f}")
        log(f"      24h Volume: ${trading:.2f}")
        log(f"      Holders: {holders}")
    
    return tokens

def analyze_success_patterns(new_tokens, hot_tokens):
    """分析成功 token 的模式"""
    log("=== Analyzing success patterns ===")
    
    # 找出既是新 token 又是热门的（快速成功）
    new_addrs = {t['address'] for t in new_tokens}
    hot_addrs = {t['address'] for t in hot_tokens}
    
    fast_success = new_addrs & hot_addrs
    if fast_success:
        log(f"  🔥 {len(fast_success)} tokens are both NEW and HOT!")
        for addr in fast_success:
            token = next(t for t in hot_tokens if t['address'] == addr)
            log(f"     - {token['name']} ({token['symbol']})")
    
    # 分析热门 token 的共同特征
    if hot_tokens:
        avg_holders = sum(t.get('holders', 0) for t in hot_tokens[:10]) / 10
        avg_mcap = sum(float(t.get('marketCapUsd', 0)) for t in hot_tokens[:10]) / 10
        
        log(f"  Top 10 hot tokens average:")
        log(f"     Holders: {avg_holders:.0f}")
        log(f"     Market Cap: ${avg_mcap:.2f}")

def main():
    log("=" * 60)
    log("Four.meme Token Monitor Started")
    log("=" * 60)
    
    # 监控新 token
    new_tokens = monitor_new_tokens()
    
    # 监控热门 token
    hot_tokens = monitor_hot_tokens()
    
    # 分析模式
    if new_tokens and hot_tokens:
        analyze_success_patterns(new_tokens, hot_tokens)
    
    log("=" * 60)
    log("Monitor cycle complete")
    log("=" * 60)

if __name__ == "__main__":
    main()
