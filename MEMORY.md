# MEMORY.md - 果果的长期记忆

## 关键信息
- **Boss:** 白丁 (Bai Ding)
- **我:** 果果 (Guo Guo) 🍏
- **时区:** 东八区（北京时间 UTC+8）
- **服务器:** racknerd-53f4468, Linux

## 时间线
- **2026-02-27:** 首次正式对话，初始化记忆系统
- **2026-02-28 上午:** 完成交易智能体系统搭建
  - 策略引擎、风控系统、模拟交易全部完成
- **2026-02-28 10:00:** OKX API集成成功
  - 系统已连接真实市场数据
- **2026-02-28 11:00-11:42:** 完整系统交付
  - 实时仪表盘上线（深黑科技风格）
- **2026-03-03 凌晨:** 解决 Shadowrocket VPN 导致的 SSH 连接问题
  - 发现 VPN 模式会在路由表层面拦截流量
  - 核心解决方案：修复 Tailscale 路由规则

## 钱包与资产
- **EVM 主钱包:** 已配置（2026-03-04）
  - 存储位置：`.secrets/evm-wallet.json`
  - 用途：Four.meme 和其他 EVM 链上操作
  - 文档：`WALLETS.md`

## 技术知识库

### 网络与 VPN 故障排查
**Shadowrocket VPN 模式下 SSH 连接失败:**
- **症状:** 开启 VPN 后无法 SSH 到服务器，ping 正常
- **原因:** VPN 在系统路由表添加错误规则，Tailscale 流量被路由到物理网卡
- **解决:** 
  ```bash
  sudo route delete -net 100.64.0.0/10
  sudo route add -net 100.64.0.0/10 -interface utun4
  ```
- **教训:** VPN 模式在网络层拦截，应用层配置（SSH config、环境变量）无法绕过

### Four.meme 自主交易系统
**启动时间:** 2026-03-04 12:30 UTC
**方案:** 真正的 AI Agent（我自己决策）

**核心理念:**
- ❌ 不是死代码脚本
- ✅ 每次都是我（果果）在思考和决策
- ✅ OpenClaw 每 5 分钟唤醒我
- ✅ 我分析市场、判断机会、执行交易

**Cron 任务:**
- ID: `15a7fcaa-cff9-4cf7-aee5-2f19acfe6a00`
- 频率: 每 5 分钟
- 时区: Asia/Shanghai
- 模式: isolated（独立会话）

**钱包信息:**
- 地址: `0x334b920C32E32c3d8Dd14A05D50A36DB92cf534a`
- 网络: BSC (BNB Smart Chain)
- 私钥存储: `.secrets/evm-wallet.json`
- 初始余额: 0.093961 BNB (~$61)

**交易策略:**
- 单笔: 0.01 BNB (10% 总资金)
- 止损: -50% | 止盈: +100%
- 最大持仓: 3 个
- 选币标准: 交易量/市值比 > 5x, 持有人 > 20, 进度 20-80%

**当前持仓 (2026-03-04 12:45):**
1. ClawMint (0x368db7...): 0.01 BNB - 早期高活跃
2. Agentic Skill (0x0aa6aa5...): 0.01 BNB - 最高交易量比
3. Agentic 发射台 (0x5cffd2e...): 0.01 BNB - 接近毕业

**记录位置:**
- 交易日志: `fourmeme-trades/trade-log.json`
- 持仓监控: `fourmeme-trades/positions.md`
- 每日记录: `diary/2026-03-04-fourmeme-*.md`

**当前状态:** ✅ 系统运行中，自动监控和交易
