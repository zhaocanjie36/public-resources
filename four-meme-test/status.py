#!/usr/bin/env python3
"""
快速查看监控状态
"""
import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("/root/.openclaw/workspace/four-meme-test/data")

# 获取最新的数据文件
hot_files = sorted(DATA_DIR.glob("hot_tokens_*.json"), reverse=True)
new_files = sorted(DATA_DIR.glob("new_tokens_*.json"), reverse=True)

if hot_files:
    with open(hot_files[0]) as f:
        hot_data = json.load(f)
    
    print("🔥 当前热门 Token Top 3:")
    for i, token in enumerate(hot_data[:3], 1):
        print(f"  {i}. {token['name']} ({token['symbol']})")
        print(f"     市值: ${float(token.get('marketCapUsd', 0)):.2f}")
        print(f"     24h交易量: ${float(token.get('tradingUsd', 0)):.2f}")
        print(f"     持有者: {token.get('holders', 0)}")
        print()

if new_files:
    with open(new_files[0]) as f:
        new_data = json.load(f)
    
    print("🆕 最新创建的 Token:")
    for i, token in enumerate(new_data[:3], 1):
        print(f"  {i}. {token['name']} ({token['symbol']})")
        print(f"     地址: {token['address']}")
        print(f"     持有者: {token.get('holders', 0)}")
        print()

print(f"📊 数据文件数量: {len(list(DATA_DIR.glob('*.json')))}")
print(f"📁 数据目录: {DATA_DIR}")
