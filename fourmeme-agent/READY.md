# Four.meme 自主交易 Agent - 系统就绪

## ✅ 完成状态

**时间:** 2026-03-04 06:55 EST

### 系统组件

**1. 环境配置 ✅**
- pnpm 包管理器：已安装
- @four-meme/four-meme-ai CLI：v1.0.4
- 区块链库：viem v2.46.3, ethers v6.16.0
- 配置文件：.env（私钥已加密存储）

**2. 钱包配置 ✅**
- 地址：`0x334b920C32E32c3d8Dd14A05D50A36DB92cf534a`
- 网络：BSC (BNB Smart Chain)
- 当前余额：0 BNB（等待充值）
- 私钥：安全存储在 `.secrets/evm-wallet.json`

**3. 核心逻辑 ✅**
- 文件：`fourmeme-agent/agent.js`（5800+ 字节）
- 余额检查：正常工作
- Agent 注册：已配置（GuoGuoTrader）
- 市场监控：已实现
- 风险控制：多层保护
- 状态管理：JSON 持久化

**4. 自动化任务 ✅**
- Cron 任务：每小时执行一次
- 执行脚本：`run-agent.sh`
- 日志系统：trading.log, cron.log, error.log
- 状态文件：state.json

**5. 监控集成 ✅**
- HEARTBEAT.md：已更新
- 监控频率：每天 1-2 次
- 报告机制：异常主动通知

---

## 🎯 风险控制参数

| 参数 | 值 | 说明 |
|------|------|------|
| 单个 token 占比 | 5% | 单个投资不超过总资金 5% |
| 总投入占比 | 20% | 最多投入总资金的 20% |
| 止损线 | 50% | 单个 token 亏损 50% 自动止损 |
| Gas 储备 | 0.02 BNB | 始终保留 gas fee |
| 单笔交易 | 0.01-0.02 BNB | 小额测试 |
| 最大持仓 | 5 个 token | 分散风险 |

---

## 📊 交易策略

**市场筛选标准：**
- 最小市值：$1000
- 最少持有人：10 人
- 最小流动性：$500

**评分系统（满分 100）：**
- 市值检查：20 分
- 持有人数：20 分
- 流动性：20 分
- 24h 交易量：20 分
- 价格趋势：20 分

**买入阈值：60 分以上**

---

## 🚀 启动流程

**当前状态：等待充值**

**充值后自动执行：**
1. ✅ 系统每小时自动检查余额
2. ⏳ 检测到余额后立即注册 Agent 身份（EIP-8004 NFT，成本 ~$1）
3. ⏳ 开始市场监控和分析
4. ⏳ 观察 1-2 天积累数据
5. ⏳ 开始小额测试交易（0.01-0.02 BNB）
6. ⏳ 通过 HEARTBEAT 定期向 Boss 汇报

---

## 💰 充值信息

**钱包地址：**
```
0x334b920C32E32c3d8Dd14A05D50A36DB92cf534a
```

**网络：** BSC (BNB Smart Chain)

**建议金额：**
- 最少：0.05 BNB（约 $30）
- 推荐：0.1-0.2 BNB（约 $60-120）

---

## 📁 文件位置

**核心文件：**
- `/root/.openclaw/workspace/fourmeme-agent/agent.js` - 交易逻辑
- `/root/.openclaw/workspace/fourmeme-agent/run-agent.sh` - Cron 脚本
- `/root/.openclaw/workspace/fourmeme-agent/.env` - 配置文件
- `/root/.openclaw/workspace/.secrets/evm-wallet.json` - 钱包信息

**日志文件（自动生成）：**
- `trading.log` - 交易决策日志
- `cron.log` - 定时任务日志
- `error.log` - 错误记录
- `state.json` - 运行状态

---

## 🔍 监控命令

**查看日志：**
```bash
# 交易日志
tail -f /root/.openclaw/workspace/fourmeme-agent/trading.log

# Cron 日志
tail -f /root/.openclaw/workspace/fourmeme-agent/cron.log

# 手动执行
cd /root/.openclaw/workspace/fourmeme-agent && node agent.js
```

**查看 Cron 任务：**
```bash
crontab -l | grep fourmeme
```

---

## ⚠️ 重要提醒

**风险声明：**
- 90% 的 memecoin 会归零
- 这是高风险投机交易
- 可能会亏损资金
- 我会尽力保护本金，但不保证盈利

**我的承诺：**
- 严格遵守风险控制规则
- 详细记录每笔交易
- 定期向 Boss 汇报
- 如有重大问题，立即暂停

---

**创建时间:** 2026-03-04 06:55 EST  
**创建者:** 果果 (Guo Guo) 🍏  
**状态:** ✅ 系统完全就绪，等待钱包充值后自动启动
