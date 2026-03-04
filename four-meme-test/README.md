# Four.meme 监控系统使用指南

## 📊 监控系统已部署

**位置:** `/root/.openclaw/workspace/four-meme-test/`

### 文件说明

- `monitor.py` - 主监控脚本（单次运行）
- `continuous-monitor.sh` - 持续监控脚本（每5分钟）
- `status.py` - 快速查看当前状态
- `data/` - 数据存储目录
- `monitor.log` - 运行日志

---

## 🚀 使用方法

### 1. 单次运行监控
```bash
cd /root/.openclaw/workspace/four-meme-test
python3 monitor.py
```

### 2. 持续监控（后台运行）
```bash
cd /root/.openclaw/workspace/four-meme-test
nohup ./continuous-monitor.sh > continuous.log 2>&1 &
echo $! > monitor.pid
```

### 3. 查看当前状态
```bash
cd /root/.openclaw/workspace/four-meme-test
python3 status.py
```

### 4. 停止监控
```bash
kill $(cat /root/.openclaw/workspace/four-meme-test/monitor.pid)
```

### 5. 查看日志
```bash
tail -f /root/.openclaw/workspace/four-meme-test/monitor.log
```

---

## 📈 数据分析

### 查看收集的数据
```bash
ls -lh /root/.openclaw/workspace/four-meme-test/data/
```

### 分析热门 token 趋势
```bash
cd /root/.openclaw/workspace/four-meme-test/data
jq '.[:5] | .[] | {name, marketCapUsd, tradingUsd, holders}' hot_tokens_*.json | tail -20
```

---

## 🎯 下一步计划

### 今天（2026-03-04）
- ✅ 监控系统已部署
- ⏳ 收集 24 小时数据
- ⏳ 分析成功模式

### 明天（2026-03-05）
- 根据数据决定是否注册智能体钱包
- 如果数据显示机会，开始小规模测试

### 本周内
- 优化监控算法
- 开发 AI 评分系统
- 建立自动化交易策略（如果测试成功）

---

## 💰 预期成本

- **监控系统:** $0（只读操作）
- **注册智能体:** $1（如果决定注册）
- **测试交易:** $0.5-1 BNB（如果决定测试）

---

**部署时间:** 2026-03-04 05:35 EST  
**状态:** ✅ 运行正常
