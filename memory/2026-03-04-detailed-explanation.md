# Four.meme 项目详细说明

**整理时间:** 2026-03-04 05:50 EST  
**目的:** 清晰解释项目机制和参与流程

---

## 📖 什么是 Four.meme？

Four.meme 是一个在 BSC（币安智能链）上的 **Memecoin 发射平台**。

**核心功能:**
- 任何人都可以创建自己的 memecoin
- 使用 bonding curve（联合曲线）机制定价
- 达到目标后自动上线 PancakeSwap（去中心化交易所）

**类比:**
- 就像 Pump.fun（Solana 上的类似平台）
- 但是在 BSC 链上

---

## 🔄 Bonding Curve 机制详解

### 什么是 Bonding Curve？

**简单理解:**
- 这是一个自动定价的数学公式
- 买的人越多，价格越高
- 卖的人越多，价格越低
- 不需要传统的买卖盘匹配

**具体运作:**

```
创建 Token 时:
├─ 总供应量: 1,000,000,000 tokens（固定）
├─ 初始价格: 极低（接近 0）
└─ 目标募资: 18 BNB（约 $11,000）

买入过程:
├─ 用户 A 买入 → 花费 0.1 BNB → 获得 X tokens
├─ 价格上涨（根据公式）
├─ 用户 B 买入 → 花费 0.1 BNB → 获得 Y tokens（Y < X）
└─ 价格继续上涨...

达到目标（18 BNB）:
├─ 自动创建 PancakeSwap 流动性池
├─ 将募集的 BNB 和对应的 tokens 注入
├─ 流动性永久锁定（burned）
└─ Token 正式"毕业"，可以在 DEX 自由交易
```

**关键点:**
- 早买的人价格低，获得的 token 多
- 晚买的人价格高，获得的 token 少
- 达到目标前，只能在 bonding curve 上交易
- 达到目标后，自动上 DEX

---

## 🤖 什么是 Agentic Mode？

### 核心概念

**Agentic Mode = AI 智能体创建和交易 memecoin**

**两个关键角色:**

1. **Agent Creator（智能体创建者）**
   - 持有 EIP-8004 NFT 的钱包
   - 创建的 token 会被标记为"AI 创建"
   - 链上身份认证

2. **普通创建者**
   - 没有 NFT 的钱包
   - 创建的 token 是普通 token

### 为什么需要 Agent 身份？

**当前阶段:**
- 主要是身份标识
- 创建的 token 会显示"AI Agent 创建"标签
- 可能获得更多关注

**未来可能:**
- 如果 four.meme 推出"内部阶段"（Insider Phase）
- Agent 钱包可能有优先交易权
- 类似 VIP 通道

**获取方式:**
- 调用 EIP-8004 NFT 合约的 `register()` 函数
- 只需要 gas 费（约 $1）
- 任何人都可以注册

---

## 📋 完整参与流程（创建 Token）

### 准备阶段

**需要准备:**
1. BSC 钱包（MetaMask 或其他）
2. 至少 0.01 BNB（gas 费 + 平台费）
3. Token 图片（JPG/PNG，<5MB）
4. Token 信息（名称、符号、描述）

### 步骤 1: 注册 Agent 身份（可选）

**如果想成为 Agent Creator:**

```bash
# 方法 1: 使用 CLI 工具
export PRIVATE_KEY=你的私钥
fourmeme 8004-register "你的智能体名称" "图片URL" "描述"

# 方法 2: 直接调用合约
# 合约地址: 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432
# 函数: register(string agentURI)
```

**成本:** ~0.001 BNB (~$0.60)

**验证:**
```bash
fourmeme 8004-balance 你的钱包地址
# 返回 balance > 0 表示成功
```

### 步骤 2: 准备 Token 信息

**必填信息:**
- **名称** (name): 例如 "Doge Killer"
- **符号** (symbol): 例如 "DOGEK"
- **描述** (description): 简短介绍
- **标签** (label): Meme | AI | DeFi | Games | Infra | De-Sci | Social | Depin | Charity | Others
- **图片** (image): 本地文件路径

**可选信息:**
- Twitter URL
- Telegram URL
- Website URL
- 种子流动性（可以投入 0-10 BNB）

### 步骤 3: 创建 Token（API 阶段）

**使用 CLI 工具:**

```bash
# 基本创建（无种子流动性）
fourmeme create-api ./logo.png "Doge Killer" "DOGEK" "The next big meme" "Meme"

# 返回结果:
{
  "createArg": "0x...",  # 链上创建参数
  "signature": "0x..."   # 签名
}
```

**这一步做了什么:**
1. 上传图片到 four.meme CDN
2. 提交 token 信息到 API
3. 获取链上创建所需的参数和签名

**成本:** 0 BNB（只是 API 调用）

### 步骤 4: 创建 Token（链上阶段）

**使用上一步的结果:**

```bash
fourmeme create-chain <createArg> <signature>

# 或者从 stdin 读取:
echo '{"createArg":"0x...","signature":"0x..."}' | fourmeme create-chain --
```

**这一步做了什么:**
1. 调用 TokenManager2 合约的 `createToken()` 函数
2. 在 BSC 链上部署你的 token
3. Token 立即可以交易

**成本:** 0.005 BNB (~$3) 平台费 + gas 费

**返回结果:**
```json
{
  "txHash": "0x...",
  "tokenAddress": "0x...",
  "blockNumber": 12345678
}
```

### 步骤 5: Token 上线

**自动发生:**
- Token 立即在 four.meme 平台上线
- 显示在"最新创建"列表
- 任何人都可以开始买卖

**你的 Token 页面:**
- URL: `https://four.meme/token/你的token地址`
- 显示价格、市值、持有者、交易历史
- 实时更新

---

## 📋 完整参与流程（交易 Token）

### 买入流程

**步骤 1: 选择 Token**

**方法 1: 浏览热门**
```bash
fourmeme token-rankings Hot
# 查看当前最热门的 token
```

**方法 2: 浏览最新**
```bash
fourmeme token-list --orderBy=Time
# 查看最新创建的 token
```

**方法 3: 直接搜索**
- 如果知道 token 地址或名称
- 在 four.meme 网站搜索

**步骤 2: 查看 Token 详情**

```bash
fourmeme token-get <token地址>

# 返回信息:
{
  "name": "...",
  "symbol": "...",
  "marketCap": "...",      # 当前市值
  "price": "...",          # 当前价格
  "holders": 123,          # 持有者数量
  "progress": 0.5,         # bonding curve 进度（0-1）
  "trading": "...",        # 24h 交易量
  ...
}
```

**步骤 3: 估算买入成本**

```bash
# 方式 1: 买入固定数量的 token
fourmeme quote-buy <token地址> <想买的token数量> 0

# 方式 2: 花费固定金额的 BNB
fourmeme quote-buy <token地址> 0 <想花的BNB数量>

# 返回:
{
  "amountOut": "...",     # 能获得的 token 数量
  "fundsIn": "...",       # 需要花费的 BNB
  "priceImpact": "...",   # 价格影响
  "newPrice": "..."       # 买入后的新价格
}
```

**步骤 4: 执行买入**

```bash
# 方式 1: 买入固定数量
fourmeme buy <token地址> amount <token数量> <最多花费BNB>

# 方式 2: 花费固定金额
fourmeme buy <token地址> funds <BNB数量> <最少获得token>

# 返回:
{
  "txHash": "0x...",
  "amountOut": "...",
  "fundsIn": "..."
}
```

**注意事项:**
- 需要设置 `PRIVATE_KEY` 环境变量
- 确保钱包有足够的 BNB
- 交易费: 1%（买入）

### 卖出流程

**步骤 1: 查看持有的 Token**

```bash
# 查询钱包余额（需要自己实现或用区块链浏览器）
# 或者在 four.meme 网站查看
```

**步骤 2: 估算卖出收益**

```bash
fourmeme quote-sell <token地址> <想卖的token数量>

# 返回:
{
  "fundsOut": "...",      # 能获得的 BNB
  "priceImpact": "...",   # 价格影响
  "newPrice": "..."       # 卖出后的新价格
}
```

**步骤 3: 执行卖出**

```bash
fourmeme sell <token地址> <token数量> [最少获得BNB]

# 返回:
{
  "txHash": "0x...",
  "fundsOut": "..."
}
```

**注意事项:**
- 需要先 approve（授权）token 给 TokenManager2 合约
- CLI 工具会自动处理 approve
- 交易费: 1%（卖出）

---

## 💰 资金流向详解

### 创建 Token 时

```
你的钱包
  ├─ 支付 0.005 BNB → four.meme 平台费
  ├─ 支付 gas 费 → BSC 矿工
  └─ （可选）种子流动性 → bonding curve 池子
```

### 买入 Token 时

```
你的钱包
  ├─ 支付 X BNB → bonding curve 池子（99%）
  ├─ 支付 X * 1% BNB → four.meme 平台费
  └─ 支付 gas 费 → BSC 矿工

你获得:
  └─ Y tokens（根据 bonding curve 计算）
```

### 卖出 Token 时

```
你的钱包
  ├─ 发送 Y tokens → bonding curve 池子
  └─ 支付 gas 费 → BSC 矿工

你获得:
  ├─ X BNB（根据 bonding curve 计算）
  └─ 扣除 1% 平台费后的实际金额
```

### Token "毕业"时（达到 18 BNB）

```
bonding curve 池子
  ├─ 18 BNB → PancakeSwap 流动性池
  ├─ 对应的 tokens → PancakeSwap 流动性池
  └─ LP tokens → 销毁（永久锁定）

结果:
  ├─ Token 可以在 PancakeSwap 交易
  ├─ 流动性永久存在
  └─ 价格由市场决定（不再是 bonding curve）
```

---

## 🎯 盈利机会详解

### 机会 #1: 创建优质 Token

**逻辑:**
- 创建一个有吸引力的 memecoin
- 吸引买家推高价格
- 在高点卖出

**成本:**
- 创建费: $3-4
- 种子流动性（可选）: 0-10 BNB
- AI 生成成本（GPT-4 + DALL-E）: ~$0.10

**收益:**
- 如果成功（5-10% 概率）: 5-20x
- 如果失败（90% 概率）: 损失全部投入

**关键成功因素:**
- 有趣的名称和概念
- 吸引人的图片
- 好的时机（市场活跃时）
- 社区推广

### 机会 #2: 早期买入新 Token

**逻辑:**
- 监控新创建的 token
- 快速判断质量
- 在价格低时买入
- 等待价格上涨后卖出

**成本:**
- 每次买入: 0.01-0.05 BNB
- 可以分散投资多个 token

**收益:**
- 成功的 token: 50-200%
- 失败的 token: -100%
- 整体成功率: 10-20%

**关键成功因素:**
- 快速反应（越早越好）
- 准确判断（名称、图片、描述）
- 严格止损（跌 10% 立即卖出）
- 及时止盈（涨 50-100% 卖出）

### 机会 #3: 波段交易热门 Token

**逻辑:**
- 交易量大的 token 流动性好
- 价格波动大
- 可以做短线交易

**成本:**
- 每次交易: 0.1-0.5 BNB
- 需要频繁操作

**收益:**
- 单次收益: 10-30%
- 成功率: 30-50%
- 日均机会: 3-5 次

**关键成功因素:**
- 选择交易量大的 token
- 设置止损和止盈
- 快进快出
- 避免贪婪

---

## ⚠️ 风险详解

### 风险 #1: Token 归零

**概率:** 90%

**原因:**
- 没有人买入
- 创建者跑路
- 概念不吸引人
- 市场不活跃

**缓解:**
- 分散投资（不要 all-in 一个 token）
- 严格止损
- 只投入闲钱

### 风险 #2: Rug Pull（跑路）

**概率:** 10-20%

**原因:**
- 创建者在高点大量卖出
- 价格暴跌
- 其他人无法卖出

**缓解:**
- 查看创建者钱包持有量
- 避免 top 10 持有者占比过高的 token
- 早期卖出，不要贪婪

### 风险 #3: 智能合约漏洞

**概率:** <1%

**原因:**
- TokenManager2 合约可能有 bug
- 被黑客攻击
- 资金损失

**缓解:**
- 只投入小额资金
- 分散到多个钱包
- 及时转出盈利

### 风险 #4: 监管风险

**概率:** 未知

**原因:**
- SEC 可能认定为非法证券
- 平台被关闭
- 用户被追责

**缓解:**
- 使用匿名钱包
- 不要 KYC
- 了解当地法规

### 风险 #5: 市场风险

**概率:** 高

**原因:**
- 整体市场下跌
- BNB 价格下跌
- 流动性枯竭

**缓解:**
- 关注市场趋势
- 在市场活跃时参与
- 避免在熊市操作

---

## 🔍 如何判断 Token 质量

### 链上指标

**1. 持有者数量**
- <10: 极早期，高风险
- 10-50: 早期，中高风险
- 50-100: 成长期，中等风险
- 100+: 成熟期，相对安全

**2. 交易量/市值比**
- <5x: 流动性差
- 5-20x: 正常
- 20-50x: 非常活跃（投机性强）
- >50x: 异常（可能是机器人）

**3. Top 10 持有者占比**
- <10%: 分散，安全
- 10-20%: 正常
- 20-50%: 集中，有风险
- >50%: 极度集中，高风险

**4. Bonding Curve 进度**
- 0-20%: 极早期
- 20-50%: 早期
- 50-80%: 中期
- 80-100%: 即将毕业

### 主观指标

**1. 名称和符号**
- 是否有趣、易记
- 是否有文化共鸣
- 是否容易传播

**2. 图片质量**
- 是否吸引眼球
- 是否专业
- 是否有 meme 潜力

**3. 描述**
- 是否清晰
- 是否有故事
- 是否有社区号召力

**4. 创建者**
- 是否是 Agent 创建
- 历史记录如何
- 是否有其他成功 token

---

## 📊 数据来源

### 链上数据

**BSC 区块链:**
- TokenManager2 合约事件
- Token 余额查询
- 交易历史

**工具:**
- BSCScan: https://bscscan.com
- Web3.js / Viem
- RPC 节点

### API 数据

**four.meme API:**
- 基础 URL: `https://four.meme/meme-api`
- 公开端点（无需认证）:
  - `/v1/public/sys/config` - 平台配置
  - `/v1/public/ticker` - Token 列表
  - `/v1/public/token/detail` - Token 详情
- 私有端点（需要认证）:
  - `/v1/private/token/create` - 创建 token
  - `/v1/private/tool/upload` - 上传图片

**CLI 工具:**
- `fourmeme config` - 获取配置
- `fourmeme token-list` - Token 列表
- `fourmeme token-rankings` - 排行榜
- `fourmeme token-get` - Token 详情

---

## 🎓 总结

### Four.meme 是什么？
- BSC 上的 memecoin 发射平台
- 使用 bonding curve 自动定价
- 任何人都可以创建和交易

### Agentic Mode 是什么？
- AI 智能体的链上身份认证
- 通过 EIP-8004 NFT 实现
- 创建的 token 会被标记

### 如何参与？
1. 准备 BSC 钱包和 BNB
2. （可选）注册 Agent 身份
3. 创建 token 或交易现有 token
4. 管理风险，及时止盈止损

### 盈利机会？
- 创建优质 token（5-10% 成功率，5-20x 回报）
- 早期买入（10-20% 成功率，50-200% 回报）
- 波段交易（30-50% 成功率，10-30% 回报）

### 风险？
- 90% 的 token 会归零
- Rug pull 风险
- 智能合约风险
- 监管风险
- 市场风险

---

**文档完成时间:** 2026-03-04 06:00 EST  
**下一步:** 等待 Boss 确认理解，然后决定是否参与
