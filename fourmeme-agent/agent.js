#!/usr/bin/env node
/**
 * Four.meme 自主交易 Agent
 * 负责监控市场、分析机会、执行交易
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs/promises';
import path from 'path';

const execAsync = promisify(exec);

const CONFIG = {
  // 风险控制
  MAX_POSITION_PERCENT: 5,      // 单个 token 最多占总资金 5%
  MAX_TOTAL_INVESTED: 20,        // 最多投入总资金的 20%
  STOP_LOSS_PERCENT: 50,         // 单个 token 止损 50%
  MIN_BNB_RESERVE: 0.02,         // 保留至少 0.02 BNB 作为 gas
  
  // 交易策略
  MIN_TRADE_AMOUNT: 0.01,        // 最小交易金额 0.01 BNB
  MAX_TRADE_AMOUNT: 0.02,        // 最大交易金额 0.02 BNB
  MAX_POSITIONS: 5,              // 最多同时持有 5 个 token
  
  // 分析参数
  MIN_MARKET_CAP: 1000,          // 最小市值 $1000
  MIN_HOLDERS: 10,               // 最少持有人数
  MIN_LIQUIDITY: 500,            // 最小流动性 $500
};

const STATE_FILE = '/root/.openclaw/workspace/fourmeme-agent/state.json';
const LOG_FILE = '/root/.openclaw/workspace/fourmeme-agent/trading.log';

// 日志函数
function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] [${level}] ${message}\n`;
  console.log(logMessage.trim());
  fs.appendFile(LOG_FILE, logMessage).catch(console.error);
}

// 执行 fourmeme 命令
async function runFourmeme(command) {
  try {
    const { stdout, stderr } = await execAsync(`npx fourmeme ${command}`, {
      cwd: '/root/.openclaw/workspace/fourmeme-agent',
      env: { ...process.env, PATH: process.env.PATH + ':/root/.local/share/pnpm' }
    });
    if (stderr && !stderr.includes('Debugger')) {
      log(`Command stderr: ${stderr}`, 'WARN');
    }
    return stdout;
  } catch (error) {
    log(`Command failed: ${command}\nError: ${error.message}`, 'ERROR');
    throw error;
  }
}

// 加载状态
async function loadState() {
  try {
    const data = await fs.readFile(STATE_FILE, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    return {
      initialized: false,
      agentRegistered: false,
      positions: [],
      totalInvested: 0,
      totalProfit: 0,
      tradeHistory: [],
      lastCheck: null
    };
  }
}

// 保存状态
async function saveState(state) {
  await fs.writeFile(STATE_FILE, JSON.stringify(state, null, 2));
}

// 检查钱包余额
async function checkBalance() {
  try {
    const response = await fetch(
      'https://api.bscscan.com/api?module=account&action=balance&address=0x334b920C32E32c3d8Dd14A05D50A36DB92cf534a&tag=latest'
    );
    const data = await response.json();
    if (data.status !== '1' || !data.result) {
      log(`Balance check failed: ${data.message || 'Unknown error'}`, 'WARN');
      return 0;
    }
    const bnbBalance = parseFloat(data.result) / 1e18;
    log(`Current BNB balance: ${bnbBalance.toFixed(6)} BNB`);
    return bnbBalance;
  } catch (error) {
    log(`Failed to check balance: ${error.message}`, 'ERROR');
    return 0;
  }
}

// 注册 Agent 身份
async function registerAgent(state) {
  if (state.agentRegistered) {
    log('Agent already registered');
    return true;
  }
  
  try {
    log('Registering Agent identity (EIP-8004)...');
    const agentName = 'GuoGuoTrader';
    const agentImage = 'https://static.four.meme/market/fc6c4c92-63a3-4034-bc27-355ea380a6795959172881106751506.png';
    const agentDesc = 'Autonomous trading agent managed by Guo Guo';
    const result = await runFourmeme(`8004-register "${agentName}" "${agentImage}" "${agentDesc}"`);
    log(`Agent registration result: ${result}`);
    state.agentRegistered = true;
    await saveState(state);
    return true;
  } catch (error) {
    log(`Agent registration failed: ${error.message}`, 'ERROR');
    return false;
  }
}

// 获取热门 token 列表
async function getHotTokens() {
  try {
    const result = await runFourmeme('token-rankings --type hot --limit 20');
    const tokens = JSON.parse(result);
    log(`Found ${tokens.length} hot tokens`);
    return tokens;
  } catch (error) {
    log(`Failed to get hot tokens: ${error.message}`, 'ERROR');
    return [];
  }
}

// 分析 token 是否值得买入
function analyzeToken(token) {
  const score = {
    total: 0,
    reasons: []
  };
  
  // 市值检查
  if (token.marketCap >= CONFIG.MIN_MARKET_CAP) {
    score.total += 20;
    score.reasons.push(`Good market cap: $${token.marketCap}`);
  }
  
  // 持有人数检查
  if (token.holders >= CONFIG.MIN_HOLDERS) {
    score.total += 20;
    score.reasons.push(`Sufficient holders: ${token.holders}`);
  }
  
  // 流动性检查
  if (token.liquidity >= CONFIG.MIN_LIQUIDITY) {
    score.total += 20;
    score.reasons.push(`Good liquidity: $${token.liquidity}`);
  }
  
  // 24h 交易量
  if (token.volume24h > 1000) {
    score.total += 20;
    score.reasons.push(`High volume: $${token.volume24h}`);
  }
  
  // 价格趋势（如果有数据）
  if (token.priceChange24h > 0) {
    score.total += 20;
    score.reasons.push(`Positive trend: +${token.priceChange24h}%`);
  }
  
  return score;
}

// 主循环
async function mainLoop() {
  log('=== Four.meme Agent Starting ===');
  
  const state = await loadState();
  const balance = await checkBalance();
  
  // 检查余额
  if (balance < CONFIG.MIN_BNB_RESERVE) {
    log(`Insufficient balance: ${balance} BNB. Need at least ${CONFIG.MIN_BNB_RESERVE} BNB`, 'WARN');
    log('Waiting for funding...');
    return;
  }
  
  // 注册 Agent（如果还没注册）
  if (!state.agentRegistered) {
    const registered = await registerAgent(state);
    if (!registered) {
      log('Cannot proceed without Agent registration', 'ERROR');
      return;
    }
  }
  
  // 获取热门 token
  const hotTokens = await getHotTokens();
  
  // 分析每个 token
  for (const token of hotTokens) {
    const analysis = analyzeToken(token);
    if (analysis.total >= 60) {
      log(`Potential opportunity: ${token.name} (${token.symbol})`);
      log(`Score: ${analysis.total}/100`);
      log(`Reasons: ${analysis.reasons.join(', ')}`);
      
      // TODO: 实现买入逻辑
      // 当前只是观察和记录
    }
  }
  
  state.lastCheck = new Date().toISOString();
  await saveState(state);
  
  log('=== Check completed ===');
}

// 运行
mainLoop().catch(error => {
  log(`Fatal error: ${error.message}`, 'ERROR');
  process.exit(1);
});
