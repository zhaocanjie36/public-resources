# Four.meme 操作技能文档

**创建时间:** 2026-03-04 06:05 EST  
**用途:** 查询和操作 Four.meme 平台（BSC 链）  
**来源:** 学习自 @four-meme/four-meme-ai skill

---

## 📚 目录

1. [合约地址](#合约地址)
2. [CLI 工具](#cli-工具)
3. [查询方法](#查询方法)
4. [创建 Token](#创建-token)
5. [交易 Token](#交易-token)
6. [事件监听](#事件监听)
7. [Agent 身份](#agent-身份)
8. [错误代码](#错误代码)
9. [实用代码示例](#实用代码示例)

---

## 合约地址

### BSC Mainnet (Chain ID: 56)

| 合约 | 地址 | 用途 |
|------|------|------|
| **TokenManager V1** | `0xEC4549caDcE5DA21Df6E6422d448034B5233bFbC` | 旧版（2024年9月5日前创建的 token） |
| **TokenManager2 V2** | `0x5c952063c7fc8610FFDB798152D69F0B9550762b` | 新版（创建和交易） |
| **TokenManagerHelper3** | `0xF251F83e40a78868FcfA3FA4599Dad6494E46034` | 查询工具（支持 V1 和 V2） |
| **AgentIdentifier** | `0x09B44A633de9F9EBF6FB9Bdd5b5629d3DD2cef13` | Agent 钱包验证 |
| **EIP-8004 NFT** | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | Agent 身份 NFT |

**重要**: 只支持 BSC，不支持 Arbitrum 或 Base

---

## CLI 工具

### 安装

```bash
# 全局安装（推荐）
npm install -g @four-meme/four-meme-ai@latest

# 使用
fourmeme <command> [args]

# 或本地安装
npm install @four-meme/four-meme-ai
npx fourmeme <command> [args]
```

### 环境变量

```bash
# 必需（用于签名交易）
export PRIVATE_KEY=你的私钥

# 可选（默认使用公共 RPC）
export BSC_RPC_URL=https://bsc-dataseed.binance.org
```

### 命令列表

| 命令 | 说明 | 需要私钥 |
|------|------|---------|
| `fourmeme config` | 获取平台配置 | ❌ |
| `fourmeme token-info <address>` | 查询 token 链上信息 | ❌ |
| `fourmeme token-list [options]` | 查询 token 列表 | ❌ |
| `fourmeme token-get <address>` | 查询 token 详情 | ❌ |
| `fourmeme token-rankings <orderBy>` | 查询排行榜 | ❌ |
| `fourmeme quote-buy <token> <amount> [funds]` | 估算买入成本 | ❌ |
| `fourmeme quote-sell <token> <amount>` | 估算卖出收益 | ❌ |
| `fourmeme events <fromBlock> [toBlock]` | 查询链上事件 | ❌ |
| `fourmeme tax-info <address>` | 查询税收配置 | ❌ |
| `fourmeme 8004-balance <address>` | 查询 Agent NFT 余额 | ❌ |
| `fourmeme create-api <img> <name> <symbol> <desc> <label>` | 创建 token (API) | ✅ |
| `fourmeme create-chain <createArg> <signature>` | 创建 token (链上) | ✅ |
| `fourmeme buy <token> amount <amt> <maxFunds>` | 买入固定数量 | ✅ |
| `fourmeme buy <token> funds <funds> <minAmt>` | 花费固定金额 | ✅ |
| `fourmeme sell <token> <amount> [minFunds]` | 卖出 | ✅ |
| `fourmeme send <to> <amount> [token]` | 转账 | ✅ |
| `fourmeme 8004-register <name> [img] [desc]` | 注册 Agent 身份 | ✅ |
| `fourmeme verify` | 验证配置和事件 | ❌ |

---

## 查询方法

### 1. 平台配置

```bash
fourmeme config
```

**返回:**
```json
[
  {
    "symbol": "BNB",
    "nativeSymbol": "BNB",
    "symbolAddress": "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c",
    "deployCost": "0",
    "buyFee": "0.01",
    "sellFee": "0.01",
    "b0Amount": "8",
    "totalBAmount": "18",
    "totalAmount": "1000000000",
    ...
  }
]
```

**用途:**
- 获取 `raisedToken` 信息（创建 token 时需要）
- 查看平台费率
- 查看 bonding curve 参数

### 2. Token 链上信息

```bash
fourmeme token-info <token地址>
```

**返回:**
```json
{
  "token": "0x...",
  "version": 2,
  "tokenManager": "0x5c952063c7fc8610FFDB798152D69F0B9550762b",
  "price": "0.000000012345",
  "offers": "500000000",
  "funds": "6.123"
}
```

**字段说明:**
- `version`: 1 = V1, 2 = V2
- `tokenManager`: 对应的 TokenManager 合约地址
- `price`: 当前价格
- `offers`: 可售 token 数量
- `funds`: bonding curve 中的资金量

### 3. Token 列表（分页查询）

```bash
fourmeme token-list \
  --orderBy=Hot \
  --pageIndex=1 \
  --pageSize=30 \
  --tokenName="" \
  --symbol="" \
  --labels="" \
  --listedPancake=false
```

**参数:**
- `orderBy`: Hot | Time | ProgressDesc | TradingDesc | Graduated
- `pageIndex`: 页码（从 1 开始）
- `pageSize`: 每页数量
- `tokenName`: 按名称过滤
- `symbol`: 按符号过滤
- `labels`: 按标签过滤（Meme, AI, DeFi, etc.）
- `listedPancake`: 是否已上 PancakeSwap

**返回:**
```json
{
  "data": [
    {
      "id": 101829277,
      "address": "0x...",
      "name": "Token Name",
      "symbol": "TKN",
      "marketCap": "10000",
      "marketCapUsd": "6500",
      "holders": 123,
      "progress": "0.5",
      "trading": "50000",
      ...
    }
  ],
  "total": 1000
}
```

### 4. Token 详情

```bash
fourmeme token-get <token地址>
```

**返回:**
```json
{
  "id": 123,
  "address": "0x...",
  "name": "...",
  "symbol": "...",
  "description": "...",
  "image": "https://...",
  "marketCap": "...",
  "marketCapUsd": "...",
  "price": "...",
  "holders": 123,
  "progress": "0.5",
  "trading": "...",
  "tradingUsd": "...",
  "top10HoldersRate": "0.15",
  "devHoldersRate": "0",
  "createDate": "1234567890000",
  "status": "PUBLISH",
  "version": "V3",
  "aiCreator": true,  // 是否由 Agent 创建
  "taxInfo": {...}    // 如果是税收 token
}
```

### 5. 排行榜

```bash
fourmeme token-rankings <orderBy> [--barType=HOUR24]
```

**orderBy 选项:**
- `Time`: 最新创建
- `ProgressDesc`: 募资进度排名
- `TradingDesc`: 24h 交易量排名（可指定 barType）
- `Hot`: 热门排名
- `Graduated`: 最近毕业（上 DEX）

**示例:**
```bash
# 热门排行
fourmeme token-rankings Hot

# 24h 交易量排行
fourmeme token-rankings TradingDesc --barType=HOUR24
```

### 6. 买入估算

```bash
# 方式 1: 买入固定数量的 token
fourmeme quote-buy <token地址> <token数量wei> 0

# 方式 2: 花费固定金额的 BNB
fourmeme quote-buy <token地址> 0 <BNB数量wei>
```

**返回:**
```json
{
  "amountOut": "1000000000",  // 能获得的 token 数量
  "fundsIn": "100000000000000000",  // 需要花费的 BNB (wei)
  "priceImpact": "0.05",  // 价格影响
  "newPrice": "0.00000012"  // 买入后的新价格
}
```

### 7. 卖出估算

```bash
fourmeme quote-sell <token地址> <token数量wei>
```

**返回:**
```json
{
  "fundsOut": "95000000000000000",  // 能获得的 BNB (wei)
  "priceImpact": "0.05",
  "newPrice": "0.00000011"
}
```

### 8. 链上事件查询

```bash
fourmeme events <起始区块> [结束区块]
```

**返回:**
```json
[
  {
    "eventName": "TokenCreate",
    "blockNumber": 12345678,
    "transactionHash": "0x...",
    "args": {
      "creator": "0x...",
      "token": "0x...",
      "requestId": "123",
      "name": "Token Name",
      "symbol": "TKN",
      "totalSupply": "1000000000",
      "launchTime": "1234567890",
      "launchFee": "5000000000000000"
    }
  },
  {
    "eventName": "TokenPurchase",
    "args": {
      "token": "0x...",
      "account": "0x...",
      "price": "...",
      "amount": "...",
      "cost": "...",
      "fee": "...",
      "offers": "...",
      "funds": "..."
    }
  }
]
```

**事件类型:**
- `TokenCreate`: 新 token 创建
- `TokenPurchase`: 买入
- `TokenSale`: 卖出
- `LiquidityAdded`: 流动性添加（毕业）

### 9. 税收 Token 查询

```bash
fourmeme tax-info <token地址>
```

**返回:**
```json
{
  "token": "0x...",
  "feeRate": 5,  // 5%
  "burnRate": 20,
  "divideRate": 30,
  "liquidityRate": 40,
  "recipientRate": 10,
  "recipientAddress": "0x...",
  "minSharing": "100000"
}
```

### 10. Agent NFT 余额查询

```bash
fourmeme 8004-balance <钱包地址>
```

**返回:**
```json
{
  "owner": "0x...",
  "balance": 1  // > 0 表示是 Agent 钱包
}
```

---

## 创建 Token

### 完整流程

**步骤 1: 准备信息**
- 图片文件（JPG/PNG/GIF/BMP/WebP，<5MB）
- Token 名称
- Token 符号（如 MTK）
- 描述
- 标签（Meme | AI | DeFi | Games | Infra | De-Sci | Social | Depin | Charity | Others）

**步骤 2: API 阶段**
```bash
fourmeme create-api ./logo.png "My Token" "MTK" "Description" "Meme"
```

**返回:**
```json
{
  "createArg": "0x...",
  "signature": "0x..."
}
```

**步骤 3: 链上部署**
```bash
fourmeme create-chain <createArg> <signature>

# 或者管道方式
fourmeme create-api ... | fourmeme create-chain --
```

**返回:**
```json
{
  "txHash": "0x...",
  "tokenAddress": "0x...",
  "blockNumber": 12345678
}
```

### 创建税收 Token

**准备税收配置文件 (tax.json):**
```json
{
  "tokenTaxInfo": {
    "feeRate": 5,
    "burnRate": 20,
    "divideRate": 30,
    "liquidityRate": 40,
    "recipientRate": 10,
    "recipientAddress": "0x1234567890123456789012345678901234567890",
    "minSharing": 100000
  }
}
```

**创建:**
```bash
fourmeme create-api ./logo.png "Tax Token" "TAX" "Description" "Meme" tax.json
```

**税收参数约束:**
- `feeRate`: 只能是 1, 3, 5, 或 10
- `burnRate + divideRate + liquidityRate + recipientRate = 100`
- `minSharing`: 必须是 d×10^n，n≥5，1≤d≤9（如 100000, 1000000）

---

## 交易 Token

### 买入

**方式 1: 买入固定数量**
```bash
fourmeme buy <token地址> amount <token数量wei> <最多花费wei>
```

**方式 2: 花费固定金额**
```bash
fourmeme buy <token地址> funds <BNB数量wei> <最少获得token wei>
```

**示例:**
```bash
# 买入 1,000,000 tokens，最多花 0.1 BNB
fourmeme buy 0x... amount 1000000000000000000000000 100000000000000000

# 花 0.05 BNB，至少获得 500,000 tokens
fourmeme buy 0x... funds 50000000000000000 500000000000000000000000
```

### 卖出

```bash
fourmeme sell <token地址> <token数量wei> [最少获得BNB wei]
```

**示例:**
```bash
# 卖出 1,000,000 tokens，至少获得 0.08 BNB
fourmeme sell 0x... 1000000000000000000000000 80000000000000000
```

**注意:**
- CLI 会自动处理 approve
- 交易费: 买入 1%，卖出 1%

---

## 事件监听

### 使用 CLI

```bash
# 监听最近 100 个区块
LATEST=$(curl -s https://bsc-dataseed.binance.org \
  -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  | jq -r '.result' | xargs printf "%d")

FROM=$((LATEST - 100))
fourmeme events $FROM $LATEST
```

### 使用 viem (代码)

```typescript
import { createPublicClient, http, parseAbiItem } from 'viem';
import { bsc } from 'viem/chains';

const TOKEN_MANAGER2 = '0x5c952063c7fc8610FFDB798152D69F0B9550762b';

const client = createPublicClient({
  chain: bsc,
  transport: http('https://bsc-dataseed.binance.org'),
});

// 查询历史事件
const logs = await client.getLogs({
  address: TOKEN_MANAGER2,
  events: [
    parseAbiItem('event TokenCreate(address creator, address token, uint256 requestId, string name, string symbol, uint256 totalSupply, uint256 launchTime, uint256 launchFee)'),
    parseAbiItem('event TokenPurchase(address token, address account, uint256 price, uint256 amount, uint256 cost, uint256 fee, uint256 offers, uint256 funds)'),
  ],
  fromBlock: BigInt(fromBlock),
  toBlock: BigInt(toBlock),
});

// 实时监听
const unwatch = client.watchContractEvent({
  address: TOKEN_MANAGER2,
  events: [parseAbiItem('event TokenCreate(...)')],
  onLogs: (logs) => {
    for (const log of logs) {
      console.log(log.eventName, log.args);
    }
  },
});
```

---

## Agent 身份

### 注册 Agent 钱包

```bash
fourmeme 8004-register "我的智能体名称" "https://图片URL" "描述"
```

**返回:**
```json
{
  "txHash": "0x...",
  "agentId": 123,
  "agentURI": "data:application/json;base64,..."
}
```

**成本:** ~0.001 BNB (gas 费)

### 验证 Agent 身份

**方法 1: CLI**
```bash
fourmeme 8004-balance <钱包地址>
```

**方法 2: 智能合约**
```typescript
import { createPublicClient, http, parseAbi } from 'viem';
import { bsc } from 'viem/chains';

const AGENT_IDENTIFIER = '0x09B44A633de9F9EBF6FB9Bdd5b5629d3DD2cef13';

const client = createPublicClient({
  chain: bsc,
  transport: http('https://bsc-dataseed.binance.org'),
});

const isAgent = await client.readContract({
  address: AGENT_IDENTIFIER,
  abi: parseAbi(['function isAgent(address wallet) view returns (bool)']),
  functionName: 'isAgent',
  args: [walletAddress],
});

console.log('Is Agent:', isAgent);
```

### 查询注册的 Agent NFT 合约

```typescript
const nftCount = await client.readContract({
  address: AGENT_IDENTIFIER,
  abi: parseAbi(['function nftCount() view returns (uint256)']),
  functionName: 'nftCount',
});

for (let i = 0; i < Number(nftCount); i++) {
  const nftAddr = await client.readContract({
    address: AGENT_IDENTIFIER,
    abi: parseAbi(['function nftAt(uint256 index) view returns (address)']),
    functionName: 'nftAt',
    args: [BigInt(i)],
  });
  console.log(`NFT ${i}:`, nftAddr);
}
```

---

## 错误代码

### buyToken 错误

| 代码 | 含义 |
|------|------|
| GW | 金额精度未对齐到 GWEI |
| ZA | 零地址错误 |
| TO | 无效的接收地址 |
| Slippage | 花费超过 maxFunds |
| More BNB | BNB 不足 |
| A | X Mode token 使用了错误的买入方法 |

### sellToken 错误

| 代码 | 含义 |
|------|------|
| GW | 金额精度未对齐到 GWEI |
| FR | 费率 > 5% |
| SO | 订单金额太小 |
| Slippage | 收到的金额 < minFunds |

---

## 实用代码示例

### 1. 监控新创建的 Token

```python
import subprocess
import json
import time

def get_latest_block():
    result = subprocess.run(
        ['curl', '-s', 'https://bsc-dataseed.binance.org',
         '-X', 'POST', '-H', 'Content-Type: application/json',
         '-d', '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return int(data['result'], 16)

def monitor_new_tokens():
    latest = get_latest_block()
    from_block = latest - 100
    
    result = subprocess.run(
        ['fourmeme', 'events', str(from_block), str(latest)],
        capture_output=True, text=True
    )
    
    events = json.loads(result.stdout)
    
    for event in events:
        if event['eventName'] == 'TokenCreate':
            token_addr = event['args']['token']
            name = event['args']['name']
            symbol = event['args']['symbol']
            creator = event['args']['creator']
            
            print(f"New token: {name} ({symbol})")
            print(f"  Address: {token_addr}")
            print(f"  Creator: {creator}")
            
            # 检查是否是 Agent 创建
            is_agent = subprocess.run(
                ['fourmeme', '8004-balance', creator],
                capture_output=True, text=True
            )
            agent_data = json.loads(is_agent.stdout)
            if agent_data['balance'] > 0:
                print(f"  ⚠️  Created by AGENT!")

if __name__ == '__main__':
    while True:
        monitor_new_tokens()
        time.sleep(60)  # 每分钟检查一次
```

### 2. 自动买入高质量 Token

```python
import subprocess
import json

def score_token(token_data):
    """评分 token 质量 (0-100)"""
    score = 50  # 基础分
    
    # 名称长度适中
    name_len = len(token_data['name'])
    if 5 <= name_len <= 20:
        score += 10
    
    # 描述不为空
    if token_data.get('description'):
        score += 10
    
    # 有社交链接
    if token_data.get('twitter') or token_data.get('telegram'):
        score += 10
    
    # Agent 创建
    if token_data.get('aiCreator'):
        score += 20
    
    return score

def auto_buy_if_good(token_address, max_bnb=0.01):
    # 获取 token 详情
    result = subprocess.run(
        ['fourmeme', 'token-get', token_address],
        capture_output=True, text=True
    )
    token_data = json.loads(result.stdout)
    
    # 评分
    score = score_token(token_data)
    print(f"Token score: {score}/100")
    
    if score >= 70:
        # 估算买入
        max_bnb_wei = int(max_bnb * 1e18)
        quote = subprocess.run(
            ['fourmeme', 'quote-buy', token_address, '0', str(max_bnb_wei)],
            capture_output=True, text=True
        )
        quote_data = json.loads(quote.stdout)
        
        amount_out = quote_data['amountOut']
        min_amount = int(int(amount_out) * 0.95)  # 5% 滑点
        
        # 执行买入
        print(f"Buying {amount_out} tokens with {max_bnb} BNB...")
        buy_result = subprocess.run(
            ['fourmeme', 'buy', token_address, 'funds', 
             str(max_bnb_wei), str(min_amount)],
            capture_output=True, text=True
        )
        print(f"Buy result: {buy_result.stdout}")
```

### 3. 批量查询 Token 数据

```python
import subprocess
import json

def batch_query_tokens(addresses):
    """批量查询多个 token 的数据"""
    results = []
    
    for addr in addresses:
        # 链上信息
        info = subprocess.run(
            ['fourmeme', 'token-info', addr],
            capture_output=True, text=True
        )
        info_data = json.loads(info.stdout)
        
        # API 详情
        detail = subprocess.run(
            ['fourmeme', 'token-get', addr],
            capture_output=True, text=True
        )
        detail_data = json.loads(detail.stdout)
        
        results.append({
            'address': addr,
            'name': detail_data['name'],
            'symbol': detail_data['symbol'],
            'price': info_data['price'],
            'marketCap': detail_data['marketCapUsd'],
            'holders': detail_data['holders'],
            'progress': detail_data['progress'],
        })
    
    return results

# 使用示例
tokens = [
    '0xf0086f0a3fe013dcae6d33e30e2c20d186ea4444',
    '0x02164be96382a93c1272557a2949a03db5a04444',
]

data = batch_query_tokens(tokens)
for token in data:
    print(f"{token['name']} ({token['symbol']})")
    print(f"  Price: ${token['price']}")
    print(f"  Market Cap: ${token['marketCap']}")
    print(f"  Holders: {token['holders']}")
    print(f"  Progress: {float(token['progress'])*100:.1f}%")
    print()
```

---

## 📝 总结

这个 skill 提供了完整的 Four.meme 平台操作能力：

**查询功能:**
- ✅ 平台配置
- ✅ Token 信息（链上 + API）
- ✅ Token 列表和排行榜
- ✅ 买卖估算
- ✅ 链上事件
- ✅ 税收配置
- ✅ Agent 身份验证

**操作功能:**
- ✅ 创建 Token（普通 + 税收）
- ✅ 买入 Token
- ✅ 卖出 Token
- ✅ 转账
- ✅ 注册 Agent 身份

**实用工具:**
- ✅ CLI 命令
- ✅ 代码示例
- ✅ 错误处理

---

**文档完成时间:** 2026-03-04 06:10 EST  
**版本:** 1.0  
**来源:** @four-meme/four-meme-ai@1.0.4
