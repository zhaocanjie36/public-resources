# Four.meme 自主交易 Agent

## 概述
这是一个完全自主的 Four.meme 交易 Agent，负责监控市场、分析机会、执行交易决策。

## 核心特性

### 1. 风险控制
- **单个 token 限制**: 最多占总资金 5%
- **总投入限制**: 不超过总资金 20%
- **止损机制**: 单个 token 亏损 50% 自动止损
- **Gas 储备**: 始终保留至少 0.02 BNB

### 2. 交易策略
- **交易规模**: 单笔 0.01-0.02 BNB
- **持仓限制**: 最多同时持有 5 个 token
- **市值要求**: 最小 $1000
- **持有人要求**: 至少 10 人
- **流动性要求**: 最小 $500

### 3. 分析系统
多维度评分机制（满分 100）：
- 市值检查（20 分）
- 持有人数（20 分）
- 流动性（20 分）
- 24h 交易量（20 分）
- 价格趋势（20 分）

**买入阈值**: 60 分以上

### 4. 自动化运行
- **Cron 任务**: 每小时检查一次市场
- **日志记录**: 所有操作详细记录
- **状态持久化**: 持仓、盈亏、历史记录

## 文件结构

```
fourmeme-agent/
├── agent.js           # 核心交易逻辑
├── run-agent.sh       # Cron 执行脚本
├── .env               # 私钥配置（已加密）
├── package.json       # 依赖配置
├── state.json         # 运行状态（自动生成）
├── trading.log        # 交易日志（自动生成）
├── cron.log           # Cron 执行日志（自动生成）
└── error.log          # 错误日志（自动生成）
```

## 当前状态

### ✅ 已完成
1. 环境搭建（pnpm + @four-meme/four-meme-ai）
2. 钱包配置（私钥安全存储）
3. 核心逻辑实现（agent.js）
4. Cron 定时任务（每小时执行）
5. 日志系统（详细记录）
6. 风险控制框架

### ⏸️ 等待中
- **钱包充值**: 当前余额 0 BNB
- **需要**: 至少 0.05 BNB（建议 0.1-0.2 BNB）

### 📋 下一步
一旦检测到余额：
1. 注册 Agent 身份（EIP-8004 NFT，成本 ~$1）
2. 开始市场监控
3. 观察 1-2 天，积累数据
4. 开始小额测试交易
5. 定期向 Boss 汇报

## 使用方法

### 手动执行
```bash
cd /root/.openclaw/workspace/fourmeme-agent
node agent.js
```

### 查看日志
```bash
# 交易日志
tail -f /root/.openclaw/workspace/fourmeme-agent/trading.log

# Cron 日志
tail -f /root/.openclaw/workspace/fourmeme-agent/cron.log

# 错误日志
tail -f /root/.openclaw/workspace/fourmeme-agent/error.log
```

### 查看状态
```bash
cat /root/.openclaw/workspace/fourmeme-agent/state.json
```

### 停止自动交易
```bash
# 临时停止（删除 cron 任务）
crontab -l | grep -v fourmeme-agent | crontab -

# 恢复
crontab -l | grep fourmeme-agent || echo "0 * * * * /root/.openclaw/workspace/fourmeme-agent/run-agent.sh >> /root/.openclaw/workspace/fourmeme-agent/cron.log 2>&1" | crontab -
```

## 安全措施

1. **私钥保护**: 存储在 `.env` 文件，权限 600
2. **Git 忽略**: `.env` 已添加到 `.gitignore`
3. **风险限制**: 多层风险控制机制
4. **详细日志**: 所有操作可追溯
5. **人工监督**: Boss 可随时查看和干预

## 监控指标

Agent 会自动记录：
- 钱包余额变化
- 持仓情况
- 盈亏统计
- 交易历史
- 市场分析结果

## 联系方式

如有问题或需要调整策略，请联系 Boss（白丁）。

---

**创建时间**: 2026-03-04 06:50 EST  
**创建者**: 果果 (Guo Guo) 🍏  
**状态**: 等待钱包充值
