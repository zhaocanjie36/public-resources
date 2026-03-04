# Four.meme 快速参考卡

**版本:** 1.0 | **链:** BSC Only | **工具:** @four-meme/four-meme-ai

---

## 🚀 快速开始

```bash
# 安装
npm install -g @four-meme/four-meme-ai@latest

# 配置
export PRIVATE_KEY=你的私钥
export BSC_RPC_URL=https://bsc-dataseed.binance.org
```

---

## 📊 常用查询

```bash
# 热门 token
fourmeme token-rankings Hot | jq '.data[:5]'

# 最新 token
fourmeme token-list --orderBy=Time --pageSize=10

# Token 详情
fourmeme token-get <地址>

# 链上信息
fourmeme token-info <地址>

# 买入估算（花 0.1 BNB）
fourmeme quote-buy <地址> 0 100000000000000000

# 卖出估算
fourmeme quote-sell <地址> <数量wei>
```

---

## 🔑 关键合约

| 合约 | 地址 |
|------|------|
| TokenManager2 | `0x5c952063c7fc8610FFDB798152D69F0B9550762b` |
| Helper3 | `0xF251F83e40a78868FcfA3FA4599Dad6494E46034` |
| AgentIdentifier | `0x09B44A633de9F9EBF6FB9Bdd5b5629d3DD2cef13` |
| EIP-8004 NFT | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |

---

## 💰 交易操作

```bash
# 买入（花 0.05 BNB）
fourmeme buy <地址> funds 50000000000000000 <最少token>

# 卖出
fourmeme sell <地址> <数量wei> <最少BNB>

# 转账
fourmeme send <接收地址> <数量wei> [token地址]
```

---

## 🤖 Agent 操作

```bash
# 注册 Agent
fourmeme 8004-register "名称" "图片URL" "描述"

# 查询 Agent 身份
fourmeme 8004-balance <地址>

# 验证（返回 balance > 0 表示是 Agent）
```

---

## 🎨 创建 Token

```bash
# 普通 token
fourmeme create-api ./logo.png "名称" "符号" "描述" "Meme" \
  | fourmeme create-chain --

# 税收 token（需要 tax.json）
fourmeme create-api ./logo.png "名称" "符号" "描述" "Meme" tax.json \
  | fourmeme create-chain --
```

---

## 📡 事件监听

```bash
# 获取最新区块
LATEST=$(curl -s https://bsc-dataseed.binance.org \
  -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  | jq -r '.result' | xargs printf "%d")

# 监听最近 100 个区块
fourmeme events $((LATEST - 100)) $LATEST
```

---

## 🔢 单位转换

```bash
# BNB 转 wei
echo "0.1 * 10^18" | bc  # 100000000000000000

# wei 转 BNB
echo "100000000000000000 / 10^18" | bc -l  # 0.1

# Token 转 wei（假设 18 decimals）
echo "1000000 * 10^18" | bc  # 1000000000000000000000000
```

---

## ⚠️ 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| GW | 金额未对齐 GWEI | 使用 GWEI 的倍数 |
| Slippage | 滑点过大 | 增加 maxFunds 或减少 amount |
| More BNB | BNB 不足 | 充值 BNB |
| SO | 订单太小 | 增加交易金额 |

---

## 📝 实用脚本

### 监控新 Token
```bash
#!/bin/bash
while true; do
  LATEST=$(curl -s https://bsc-dataseed.binance.org \
    -X POST -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
    | jq -r '.result' | xargs printf "%d")
  
  fourmeme events $((LATEST - 10)) $LATEST | \
    jq '.[] | select(.eventName == "TokenCreate") | .args'
  
  sleep 30
done
```

### 批量查询
```bash
#!/bin/bash
for addr in $(cat token_list.txt); do
  echo "=== $addr ==="
  fourmeme token-get $addr | jq '{name, symbol, marketCapUsd, holders}'
done
```

---

## 🎯 成功 Token 特征

- ✅ 持有者: 100-300+
- ✅ 交易量/市值: 20-50x
- ✅ Top 10 持有率: <20%
- ✅ 进度: 20-80%
- ✅ 有趣的名称和图片
- ✅ Agent 创建（可选）

---

## 📚 完整文档

详细文档: `/root/.openclaw/workspace/skills/four-meme-skill.md`

---

**创建时间:** 2026-03-04 06:15 EST
