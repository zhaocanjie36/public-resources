# Four.meme Agentic Mode 完整调研报告

**调研时间:** 2026-03-04 05:15 EST  
**调研人:** 果果 (Guo Guo)  
**目标:** 全面了解 four.meme 项目，识别盈利机会

---

## 📅 项目时间线

### 2024年6月
- **项目启动**: four.meme 在 BNB Chain 上线
- **定位**: BSC 上的 memecoin 公平发射平台（对标 Solana 的 Pump.fun）
- **Twitter 账号创建**: @four_meme_ (2024年6月)

### 2024年中期至今
- **成长数据**:
  - 已创建 **52,000+ tokens**
  - **27,000+ 独立创建者**
  - **1,000+ tokens** 成功毕业到 PancakeSwap
  - 日交易额峰值: **$60M**

### 2025年2月18日
- **BNB Chain 流动性支持计划** 第一轮启动
- BNB Chain Foundation 提供 **$4.4M 永久流动性支持**

### 2025年末 - 2026年初（预计）
- **Agentic Mode 即将上线**（目前处于开发/测试阶段）
- GitHub 项目 `four-meme-agent` 由 @alenfour（four.meme 后端工程师）开发

---

## 🏗️ 技术架构

### 平台核心功能

**1. 公平发射机制**
- 无预售（No presale）
- 无团队分配（No team allocation）
- 无内幕优势（No insider advantage）
- 固定总供应量: **1,000,000,000 tokens**

**2. Bonding Curve 机制**
```
创建 Token → 内部交易阶段 → 达到目标 → 自动毕业到 PancakeSwap
```

**3. 费用结构**
- 创建费用: **0.005 BNB** (~$1.5 USD)
- 种子流动性（可选）: 0 - 10 BNB

**4. 智能合约**
- **TokenManager2**: `0x5c952063c7fc8610FFDB798152D69F0B9550762b`
- 链: BSC Mainnet (Chain ID: 56)
- 功能: `createToken(bytes createArg, bytes signature)`

---

## 🤖 Agentic Mode 详解

### 什么是 Agentic Mode？

**核心概念**: AI 智能体自主创建和运营 memecoin

**两阶段发行机制**:

```
┌─────────────────────────────────┐
│ INSIDER PHASE (内部阶段)        │
│                                 │
│ ✅ 只有智能体钱包能买入          │
│ ✅ Bonding curve 价格上升        │
│ ✅ 达到募资目标后进入公开阶段    │
└─────────────────┬───────────────┘
                  │
                  ▼
┌─────────────────────────────────┐
│ PUBLIC PHASE (公开阶段)         │
│                                 │
│ ✅ 所有钱包都能交易              │
│ ✅ 正常 bonding curve           │
│ ✅ 达到市值目标后毕业到 DEX      │
└─────────────────────────────────┘
```

### 智能体钱包认证

**要求**: 持有以下任一 NFT 标准的 token

| NFT 标准 | 合约地址 | 状态 |
|---------|---------|------|
| ERC-8004 | TBD (由 four.meme 定义) | 待公布 |
| BAP-578 | TBD (由 four.meme 定义) | 待公布 |

**验证逻辑** (伪代码):
```python
def is_agent_wallet(address: str) -> bool:
    return (
        holds_erc8004_nft(address) or
        holds_bap578_nft(address)
    )

def can_trade_insider(tx_origin: str, token: Token) -> bool:
    if not token.insider_phase_active:
        return True  # 公开阶段，任何人都能交易
    return is_agent_wallet(tx_origin)
```

**重要**: four.meme 检查 `tx.origin`（交易发起者），而不是 `msg.sender`
- 这意味着即使通过第三方路由器（1inch, Paraswap）也无法绕过检查
- 只有真正的智能体钱包持有者才能在内部阶段交易

**已验证的智能体钱包示例**:
- `0x4d246f362fd94ba04d2909b7fff3621244d8ab7b`

---

## 💻 开源智能体实现

### GitHub 项目: `alenfour/four-meme-agent`

**作者**: @alenfour (four.meme Solidity & Backend Engineer)

**技术栈**:
```
- Python 3.10+
- Web3.py (BSC 交互)
- httpx (异步 HTTP)
- OpenAI API (GPT-4o)
- DALL-E / Stable Diffusion / Pillow (图片生成)
```

**核心模块**:

1. **src/four_meme/auth.py** - 钱包签名登录
   - 获取 nonce
   - 签名消息: `"You are sign in Meme {nonce}"`
   - 获取 access_token

2. **src/four_meme/api.py** - REST API 客户端
   - 上传图片
   - 创建 token (获取 createArg + signature)
   - 查询市场数据

3. **src/four_meme/onchain.py** - BSC 链上交互
   - 调用 TokenManager2.createToken()
   - 解析 TokenCreated 事件
   - 获取新 token 地址

4. **src/agent/brain.py** - AI 决策引擎
   - 生成 token 概念（名称、符号、描述）
   - 市场分析和趋势判断
   - 概念排名和评分
   - 决定募资金额
   - 生成图片 prompt
   - 生成 Twitter 推文

5. **src/agent/strategy.py** - 发射策略
   - 市场时机判断
   - 风险评估
   - 发射频率控制

6. **src/agent/memory.py** - 记忆系统
   - 记录历史发射
   - 学习成功/失败模式
   - 持久化到 JSON

7. **src/image/generator.py** - 图片生成
   - DALL-E 3 集成
   - Stable Diffusion 集成
   - Pillow 本地生成（备用）

### 智能体工作流程

```
┌─────────────────────────────────────────────────────┐
│ Agent Loop (每 10 分钟一次)                          │
│                                                     │
│ 1. MarketAnalyzer                                   │
│    ├─ 获取 trending tokens                          │
│    ├─ 分析热门关键词                                 │
│    └─ 评估市场情绪                                   │
│                                                     │
│ 2. AgentBrain.generate_token_concepts()             │
│    ├─ 输入: 市场上下文                               │
│    ├─ LLM: GPT-4o                                   │
│    └─ 输出: 3个 token 概念                           │
│                                                     │
│ 3. AgentBrain.rank_concepts()                       │
│    ├─ 评估病毒传播潜力                               │
│    ├─ 评估文化共鸣                                   │
│    └─ 选出最佳概念                                   │
│                                                     │
│ 4. ImageGenerator.generate()                        │
│    ├─ 输入: image_prompt                            │
│    ├─ DALL-E 3 生成图片                             │
│    └─ 保存到本地                                     │
│                                                     │
│ 5. FourMemeClient.upload_image()                    │
│    └─ 上传到 four.meme CDN                          │
│                                                     │
│ 6. FourMemeClient.create_token()                    │
│    ├─ 提交 token 元数据                             │
│    └─ 获取 createArg + signature                    │
│                                                     │
│ 7. BSCChain.submit_create_token()                   │
│    ├─ 构建交易                                       │
│    ├─ 签名并发送                                     │
│    └─ 等待确认                                       │
│                                                     │
│ 8. AgentMemory.record_launch()                      │
│    └─ 记录到 agent_memory.json                      │
│                                                     │
│ 9. AgentBrain.reflect_on_launch()                   │
│    └─ 生成反思，优化未来策略                         │
└─────────────────────────────────────────────────────┘
```

### 环境变量配置

```bash
# 钱包
WALLET_PRIVATE_KEY=0xyour_private_key_here

# LLM (OpenAI 或兼容 API)
LLM_API_BASE=https://api.openai.com/v1
LLM_API_KEY=sk-your_openai_key_here
LLM_MODEL=gpt-4o

# 图片生成后端: dalle | stable_diffusion | pillow
IMAGE_BACKEND=dalle

# BSC RPC
BSC_RPC_URL=https://bsc-dataseed1.binance.org/

# 智能体循环
LOOP_INTERVAL_SECONDS=600  # 10分钟
MEMORY_PATH=agent_memory.json
```

### 使用示例

**1. 自动循环模式**:
```bash
python scripts/run_agent.py
```

**2. 单次发射（测试）**:
```bash
python scripts/run_agent.py --once --dry-run
```

**3. 指定主题**:
```bash
python scripts/run_agent.py --once --theme "AI cat taking over BSC"
```

**4. 手动创建 token**:
```bash
python scripts/create_token.py \
  --name "My Token" \
  --symbol "MTK" \
  --description "The most based token on BSC" \
  --image path/to/logo.png \
  --raise-bnb 0.5
```

---

## 💰 盈利机会详细分析

### 机会 #1: 智能体钱包套利（最直接）

**前提**: 获取 ERC-8004 或 BAP-578 NFT

**策略**:
1. 监控所有新发行的 token（通过 TokenCreated 事件）
2. 快速分析 token 质量（名称、图片、描述、创建者历史）
3. 在内部阶段抢先买入优质 token
4. 公开阶段开盘时卖出

**优势**:
- 比散户早 N 分钟/小时
- 内部阶段价格更低
- 信息差

**风险**:
- NFT 获取难度未知
- 需要快速决策算法
- 90% 的 token 会归零

**预期 ROI**: 高风险高回报（单次 2-10x，但成功率 <20%）

---

### 机会 #2: 部署多个 AI 智能体（技术流）

**策略**:
1. Fork 开源代码
2. 优化 AI prompt（更好的概念生成）
3. 优化图片生成（更吸睛）
4. 部署多个智能体，批量创建 token
5. 撒网式，总有几个会爆

**成本**:
- 每个 token: 0.005 BNB (gas) + 0-2 BNB (种子流动性)
- OpenAI API: ~$0.10 per token (GPT-4o + DALL-E 3)
- 服务器: 已有（我们的 racknerd-53f4468）

**优势**:
- 24/7 自动运行
- 可扩展（多钱包并行）
- 数据积累（学习什么 token 会成功）

**风险**:
- 竞争激烈（其他人也在用同样的代码）
- 需要持续优化策略
- 资金消耗快

**预期 ROI**: 中等风险中等回报（月投入 10 BNB，预期回报 15-30 BNB）

---

### 机会 #3: 改进智能体策略（高级玩法）

**策略**:
1. 收集历史数据（所有 token 的表现）
2. 训练机器学习模型预测成功率
3. 优化 prompt engineering（更病毒式的概念）
4. 优化发射时机（避开竞争高峰）
5. 优化图片生成（使用 Midjourney 或自训练模型）

**技术要求**:
- 数据科学能力
- 机器学习经验
- 创意能力

**优势**:
- 竞争优势（比开源版本更好）
- 更高成功率
- 可持续盈利

**风险**:
- 开发时间长
- 需要大量数据
- 市场变化快

**预期 ROI**: 低风险高回报（如果策略有效，月回报 50-200%）

---

### 机会 #4: 数据分析平台（卖铲子）

**策略**:
1. 追踪所有智能体创建的 token
2. 分析成功 vs 失败的模式
3. 提供实时信号（哪些 token 值得买）
4. 卖订阅或 API 访问

**产品形态**:
- Web 仪表盘（类似我们的 Kiro Gateway Manager）
- Telegram Bot（实时推送信号）
- API（给量化交易者）

**收费模式**:
- 免费版: 延迟 5 分钟的数据
- 基础版: $50/月，实时数据
- 专业版: $200/月，API 访问 + 高级信号

**优势**:
- 不直接参与赌博
- 稳定收入
- 可扩展

**风险**:
- 需要营销
- 竞争对手可能出现
- 用户获取成本

**预期 ROI**: 低风险稳定回报（6个月后月收入 $2k-10k）

---

### 机会 #5: 智能体托管服务（SaaS）

**策略**:
1. 提供"智能体即服务"
2. 用户只需提供钱包和 API key
3. 我们运行和优化智能体
4. 收取订阅费或利润分成

**收费模式**:
- 订阅制: $100/月
- 或利润分成: 20% 的净利润

**优势**:
- 目标市场: 想参与但没技术的人
- 可扩展（一台服务器运行多个智能体）
- 稳定收入

**风险**:
- 法律风险（可能被视为投资顾问）
- 客户资金管理风险
- 需要客户信任

**预期 ROI**: 中等风险稳定回报（10个客户 = $1k/月）

---

## 🚨 关键风险

### 1. NFT 获取难度（最大未知数）

**问题**: ERC-8004 和 BAP-578 NFT 的获取方式尚未公布

**可能性**:
- **免费注册**: 任何人都能获得（竞争激烈）
- **白名单**: 需要申请或邀请（门槛高）
- **购买**: 需要花钱买 NFT（成本未知）
- **质押**: 需要质押 BNB 或其他 token（资金锁定）

**影响**: 如果 NFT 很难获得，整个 Agentic Mode 的参与门槛会很高

---

### 2. 市场饱和

**问题**: 太多智能体后，竞争白热化

**后果**:
- Token 质量下降（垃圾泛滥）
- 散户失去兴趣
- 成功率降低
- 利润空间压缩

**时间窗口**: 预计 Agentic Mode 上线后 3-6 个月是黄金期

---

### 3. 监管风险

**问题**: SEC 可能认定为非法证券发行

**风险**:
- 平台被关闭
- 用户资金损失
- 法律责任

**缓解**: 使用匿名钱包，不 KYC

---

### 4. 技术风险

**问题**:
- 智能合约漏洞
- API 不稳定
- 链上拥堵（gas 费暴涨）

**缓解**: 小资金测试，逐步扩大规模

---

### 5. 资金风险

**问题**: Memecoin 市场极度投机，90% 的 token 会归零

**缓解**:
- 严格止损
- 分散投资
- 只用闲钱

---

## 📊 市场数据

### Four.meme 平台数据

- **总创建 token**: 52,000+
- **独立创建者**: 27,000+
- **成功毕业到 PancakeSwap**: 1,000+
- **日交易额峰值**: $60M
- **成功率**: ~2% (1,000 / 52,000)

### 成功案例

**1. Test Token ($TST)**
- 意外爆火（原本是教程 token）
- 价格暴涨 1,000%+
- 当前价格: ~$0.075

**2. BIC ($BIC)**
- Four.meme 旗舰 token
- 公平发射，无预售
- 稳定增长

**3. FOUR & WHY**
- 平台奖励 token
- 用于空投和社区激励

---

## 🎯 实施建议

### 短期（1-2周）

**目标**: 了解和测试

**行动**:
1. ✅ 深入研究 four.meme 文档（已完成）
2. ⏳ 关注 four.meme Twitter，等待 Agentic Mode 上线公告
3. ⏳ 研究如何获取智能体钱包 NFT
4. ⏳ 准备测试钱包（0.5-1 BNB）
5. ⏳ 在本地运行开源智能体（dry-run 模式）

**预算**: 0.5-1 BNB (~$300-600)

---

### 中期（1-2月）

**目标**: 小规模实战

**行动**:
1. 获取 1-2 个智能体钱包 NFT
2. 部署监控系统（追踪所有新 token）
3. 手动测试：在内部阶段买入 5-10 个 token
4. 分析数据，找出成功 token 的模式
5. 部署 1 个自己的智能体，小规模发行（3-5 个 token）

**预算**: 5-10 BNB (~$3k-6k)

**预期回报**: 测试阶段，目标是学习，不是盈利

---

### 长期（3月+）

**目标**: 规模化或转型

**路径 A: 如果套利成功**
1. 扩大规模（多个智能体钱包）
2. 优化策略（机器学习模型）
3. 自动化交易（狙击机器人）

**路径 B: 如果竞争太激烈**
1. 转型做数据分析平台（卖铲子）
2. 或做智能体托管服务（SaaS）
3. 或退出，寻找下一个机会

**预算**: 20-50 BNB (~$12k-30k)

**预期回报**: 如果成功，月回报 50-200%

---

## 🔍 下一步行动

### 立即行动（今天）

1. **关注 four.meme 官方渠道**:
   - Twitter: @four_meme_
   - Telegram: 搜索 "four.meme official"
   - Discord: 如果有的话

2. **准备测试环境**:
   - 创建新的 BSC 钱包（用于测试）
   - 转入 0.5 BNB
   - 配置 OpenAI API key

3. **本地测试开源智能体**:
   ```bash
   cd /tmp/four-meme-agent
   cp .env.example .env
   # 编辑 .env，填入测试钱包和 API key
   python scripts/run_agent.py --once --dry-run --theme "test"
   ```

### 等待触发（1-4周内）

**触发条件**: four.meme 官方公布 Agentic Mode 上线时间和 NFT 获取方式

**届时行动**:
1. 第一时间获取智能体钱包 NFT
2. 部署监控系统
3. 开始小规模测试

---

## 📝 总结

### 核心洞察

**Four.meme Agentic Mode = AI 智能体竞争创造病毒式 memecoin 的新游戏**

**关键成功因素**:
1. **早期参与** - 时间窗口只有 3-6 个月
2. **更好的 AI** - 策略优化是核心竞争力
3. **快速迭代** - 市场变化快，需要持续优化
4. **风险控制** - 90% 的 token 会归零，严格止损

**最佳策略**:
- 短期: 智能体钱包套利（如果能获取 NFT）
- 中期: 部署优化的智能体（如果套利成功）
- 长期: 转型做数据分析平台（卖铲子，稳定收入）

**风险提示**:
- 这是一个高风险高回报的投机市场
- 只用闲钱参与
- 随时准备退出

---

**调研完成时间**: 2026-03-04 05:30 EST  
**下次更新**: 等待 Agentic Mode 上线公告
