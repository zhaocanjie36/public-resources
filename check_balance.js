const { ethers } = require('ethers');

const RPC = 'https://bsc-dataseed.binance.org/';
const WALLET = '0x334b920C32E32c3d8Dd14A05D50A36DB92cf534a';

async function checkBalance() {
  const provider = new ethers.JsonRpcProvider(RPC);
  
  // BNB balance
  const bnbBalance = await provider.getBalance(WALLET);
  console.log('BNB Balance:', ethers.formatEther(bnbBalance), 'BNB');
  
  // USDC balance (BSC)
  const USDC_ADDRESS = '0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d';
  const usdcContract = new ethers.Contract(
    USDC_ADDRESS,
    ['function balanceOf(address) view returns (uint256)'],
    provider
  );
  const usdcBalance = await usdcContract.balanceOf(WALLET);
  console.log('USDC Balance:', ethers.formatUnits(usdcBalance, 18), 'USDC');
}

checkBalance().catch(console.error);
