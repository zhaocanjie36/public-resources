# Four.meme 智能交易 - OpenClaw Cron 任务

## ✅ 已配置

**任务类型：** OpenClaw Cron（真正的 AI Agent）

**执行频率：** 每 5 分钟

**执行方式：** 
- OpenClaw 每 5 分钟唤醒我（果果）
- 我用自己的智能分析市场
- 我决定是否交易
- 我执行交易（如果我认为合适）
- 我记录决策过程

## 🎯 我的任务

每次被唤醒时，我会：

1. **检查钱包余额**
   ```bash
   curl -s "https://api.bscscan.com/api?module=account&action=balance&address=0x334b920C32E32c3d8Dd14A05D50A36DB92cf534a&tag=latest"
   ```

2. **查看市场热门 token**
   ```bash
   cd /root/.openclaw/workspace/fourmeme-agent
   npx fourmeme token-rankings Hot --limit 10
   ```

3. **用我的智能分析**
   - 市值、流动性、持有人数
   - 价格趋势、交易量
   - 风险评估

4. **决定是否交易**
   - 如果发现好机会 → 交易
   - 如果没有好机会 → 等待
   - 如果需要止损 → 卖出

5. **记录决策**
   - 写入 `diary/2026-03-04.md`
   - 记录我的思考过程

## 🛡️ 风险控制

我会严格遵守：
- 单个 token ≤ 5% 总资金
- 总投入 ≤ 20% 总资金
- 止损线 50%
- 保留 ≥ 0.02 BNB gas

## 📊 查看任务

```bash
# 查看所有任务
openclaw cron list

# 查看执行历史
openclaw cron runs --id <job-id>

# 手动触发一次
openclaw cron run <job-id>
```

---

**这才是真正的 AI Agent！我在思考，我在决策，不是死代码！**
