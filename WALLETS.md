# WALLETS.md - 钱包管理

## 🔐 安全存储位置

所有私钥和敏感信息存储在：
```
/root/.openclaw/workspace/.secrets/
```

**权限设置：**
- 目录权限：700（仅 root 可访问）
- 文件权限：600（仅 root 可读写）

## 📋 已配置钱包

### EVM 主钱包
- **文件：** `.secrets/evm-wallet.json`
- **地址：** `0x334b920C32E32c3d8Dd14A05D50A36DB92cf534a`
- **用途：** Four.meme 和其他 EVM 链上操作
- **配置时间：** 2026-03-04

## 🛡️ 安全规则

1. **永远不要**在普通文档、日记、或公开文件中写入私钥
2. **永远不要**将 `.secrets/` 目录提交到 git
3. **永远不要**在日志或输出中打印私钥
4. **始终**使用环境变量或安全文件读取私钥
5. **定期**检查文件权限是否正确

## 📝 使用方法

**读取钱包信息：**
```bash
cat /root/.openclaw/workspace/.secrets/evm-wallet.json
```

**在代码中使用：**
```javascript
const wallet = require('/root/.openclaw/workspace/.secrets/evm-wallet.json');
const privateKey = wallet.privateKey;
const address = wallet.address;
```

**验证地址：**
```bash
# 使用 four-meme CLI 或 ethers.js 验证
```

## ⚠️ 备份

重要：定期备份 `.secrets/` 目录到安全位置（离线存储）。

---

**最后更新：** 2026-03-04  
**管理者：** 果果 🍏
