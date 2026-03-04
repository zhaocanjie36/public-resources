# Four.meme 自主交易 Agent - 完整系统

## 🎯 系统状态：就绪，等待充值

### 当前配置

**钱包信息:**
- 地址: `0x334b920C32E32c3d8Dd14A05D50A36DB92cf534a`
- 网络: BSC (BNB Smart Chain)
- 当前余额: **0 BNB** ⚠️
- 需要充值: 0.1-0.2 BNB（建议）

**自动化任务:**
- ✅ Cron 已配置（每小时执行）
- ✅ 日志系统已就绪
- ✅ 风险控制已启用
- ✅ 监控集成到 HEARTBEAT

---

## 📊 交易策略

### 风险控制
| 参数 | 限制 |
|------|------|
| 单个 token 占比 | 最多 5% |
| 总投入占比 | 最多 20% |
| 止损线 | 亏损 50% |
| Gas 储备 | 至少 0.02 BNB |

### 交易规则
| 参数 | 值 |
|------|------|
| 单笔交易 | 0.01-0.02 BNB |
| 最大持仓 | 5 个 token |
| 最小市值 | $1000 |
| 最少持有人 | 10 人 |
| 最小流动性 | $500 |

### 评分系统
- 市值检查：20 分
- 持有人数：20 分
- 流动性：20 分
- 24h 交易量：20 分
- 价格趋势：20 分
- **买入阈值：60 分**

---

## 🚀 充值后自动流程

1. **检测余额** → 系统每小时自动检查
2. **注册身份** → EIP-8004 NFT（成本 ~$1）
3. **市场监控** → 分析热门 token
4. **观察学习** → 1-2 天数据积累
5. **开始交易** → 小额测试（0.01-0.02 BNB）
6. **定期汇报** → 通过 HEARTBEAT 向 Boss 报告

---

## 📁 文件结构

```
fourmeme-agent/
├── agent.js           # 核心交易逻辑
├── run-agent.sh       # Cron 执行脚本
├── .env               # 私钥配置（已加密）
├── package.json       # 依赖配置
├── state.json         # 运行状态（自动生成）
├── trading.log        # 交易日志（自动生成）
├── cron.log           # Cron 日志（自动生成）
└── error.log          # 错误日志（自动生成）
```

---

## 🔍 监控命令

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
# 运行状态
cat /root/.openclaw/workspace/fourmeme-agent/state.json

# 钱包余额
curl -s "https://api.bscscan.com/api?module=account&action=balance&address=0x334b920C32E32c3d8Dd14A05D50A36DB92cf534a&tag=latest" | jq
```

### 手动执行
```bash
cd /root/.openclaw/workspace/fourmeme-agent
node agent.js
```

---

## 🛡️ 安全措施

1. **私钥保护**: 存储在 `.env`，权限 600
2. **Git 忽略**: 敏感文件不会上传
3. **风险限制**: 多层风险控制机制
4. **详细日志**: 所有操作可追溯
5. **人工监督**: Boss 可随时查看和干预

---

## ⚠️ 重要提醒

**这是真实资金交易，存在风险：**
- 90% 的 memecoin 会归零
- 可能会亏损
- 我会尽力保护本金，但不保证盈利

**我的承诺：**
- 严格遵守风险控制规则
- 详细记录每笔交易
- 定期向 Boss 汇报
- 如有重大问题，立即暂停

---

## 📞 联系方式

如需调整策略或有任何问题，请随时联系 Boss（白丁）。

---

**创建时间**: 2026-03-04 06:55 EST  
**创建者**: 果果 (Guo Guo) 🍏  
**状态**: ✅ 系统就绪，等待钱包充值
