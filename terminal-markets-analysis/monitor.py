#!/usr/bin/env python3
"""
Terminal Markets 链上监控脚本
用途: 实时监控Base链上的Terminal Markets活动
"""

from web3 import Web3
import json
import time
from datetime import datetime
import requests

# Base主网RPC
BASE_RPC = "https://mainnet.base.org"
w3 = Web3(Web3.HTTPProvider(BASE_RPC))

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    banner = f"""
{Colors.HEADER}╔═══════════════════════════════════════════════════════╗
║     Terminal Markets 链上监控系统 v1.0              ║
║     Base Network Monitor                              ║
╚═══════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)

def get_latest_block():
    """获取最新区块"""
    try:
        return w3.eth.block_number
    except Exception as e:
        print(f"{Colors.FAIL}[ERROR] 获取区块失败: {e}{Colors.ENDC}")
        return None

def monitor_large_transactions(min_value_eth=1.0):
    """监控大额交易"""
    print(f"\n{Colors.OKBLUE}[INFO] 开始监控大额交易 (>= {min_value_eth} ETH)...{Colors.ENDC}")
    
    last_block = get_latest_block()
    if not last_block:
        return
    
    while True:
        try:
            current_block = get_latest_block()
            
            if current_block > last_block:
                for block_num in range(last_block + 1, current_block + 1):
                    block = w3.eth.get_block(block_num, full_transactions=True)
                    
                    for tx in block.transactions:
                        value_eth = w3.from_wei(tx['value'], 'ether')
                        
                        if value_eth >= min_value_eth:
                            print(f"\n{Colors.WARNING}[ALERT] 大额交易检测!{Colors.ENDC}")
                            print(f"  区块: {block_num}")
                            print(f"  交易哈希: {tx['hash'].hex()}")
                            print(f"  发送方: {tx['from']}")
                            print(f"  接收方: {tx['to']}")
                            print(f"  金额: {value_eth} ETH")
                            print(f"  Gas价格: {w3.from_wei(tx['gasPrice'], 'gwei')} Gwei")
                            
                            # 检查是否为合约交互
                            if tx['to']:
                                code = w3.eth.get_code(tx['to'])
                                if len(code) > 0:
                                    print(f"  {Colors.OKGREEN}[合约交互]{Colors.ENDC}")
                
                last_block = current_block
            
            time.sleep(2)  # 每2秒检查一次
            
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}[INFO] 监控已停止{Colors.ENDC}")
            break
        except Exception as e:
            print(f"{Colors.FAIL}[ERROR] {e}{Colors.ENDC}")
            time.sleep(5)

def analyze_contract(address):
    """分析合约代码"""
    print(f"\n{Colors.OKBLUE}[INFO] 分析合约: {address}{Colors.ENDC}")
    
    try:
        # 获取合约代码
        code = w3.eth.get_code(address)
        
        if len(code) <= 2:
            print(f"{Colors.WARNING}[WARN] 不是合约地址{Colors.ENDC}")
            return
        
        print(f"  代码大小: {len(code)} bytes")
        
        # 获取余额
        balance = w3.eth.get_balance(address)
        print(f"  余额: {w3.from_wei(balance, 'ether')} ETH")
        
        # 尝试识别合约类型
        code_hex = code.hex()
        
        patterns = {
            "ERC20": "a9059cbb",  # transfer(address,uint256)
            "ERC721": "42842e0e",  # safeTransferFrom
            "Uniswap": "7ff36ab5",  # swapExactETHForTokens
            "Proxy": "5c60da1b",  # implementation()
        }
        
        detected = []
        for name, pattern in patterns.items():
            if pattern in code_hex:
                detected.append(name)
        
        if detected:
            print(f"  {Colors.OKGREEN}检测到: {', '.join(detected)}{Colors.ENDC}")
        
    except Exception as e:
        print(f"{Colors.FAIL}[ERROR] {e}{Colors.ENDC}")

def monitor_nft_transfers(nft_contract=None):
    """监控NFT转移"""
    print(f"\n{Colors.OKBLUE}[INFO] 监控NFT转移...{Colors.ENDC}")
    
    # ERC721 Transfer事件签名
    transfer_topic = w3.keccak(text="Transfer(address,address,uint256)").hex()
    
    last_block = get_latest_block()
    
    while True:
        try:
            current_block = get_latest_block()
            
            if current_block > last_block:
                # 创建过滤器
                filter_params = {
                    'fromBlock': last_block + 1,
                    'toBlock': current_block,
                    'topics': [transfer_topic]
                }
                
                if nft_contract:
                    filter_params['address'] = nft_contract
                
                logs = w3.eth.get_logs(filter_params)
                
                for log in logs:
                    # 解析Transfer事件
                    from_addr = "0x" + log['topics'][1].hex()[-40:]
                    to_addr = "0x" + log['topics'][2].hex()[-40:]
                    token_id = int(log['topics'][3].hex(), 16)
                    
                    print(f"\n{Colors.OKGREEN}[NFT Transfer]{Colors.ENDC}")
                    print(f"  合约: {log['address']}")
                    print(f"  Token ID: {token_id}")
                    print(f"  从: {from_addr}")
                    print(f"  到: {to_addr}")
                    print(f"  交易: {log['transactionHash'].hex()}")
                
                last_block = current_block
            
            time.sleep(3)
            
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}[INFO] 监控已停止{Colors.ENDC}")
            break
        except Exception as e:
            print(f"{Colors.FAIL}[ERROR] {e}{Colors.ENDC}")
            time.sleep(5)

def check_contract_verification(address):
    """检查合约是否在Basescan上验证"""
    print(f"\n{Colors.OKBLUE}[INFO] 检查合约验证状态...{Colors.ENDC}")
    
    # Basescan API (需要API key)
    api_url = f"https://api.basescan.org/api"
    params = {
        'module': 'contract',
        'action': 'getsourcecode',
        'address': address,
        'apikey': 'YourApiKeyToken'  # 需要替换
    }
    
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        
        if data['status'] == '1' and data['result'][0]['SourceCode']:
            print(f"  {Colors.OKGREEN}✓ 合约已验证{Colors.ENDC}")
            print(f"  合约名称: {data['result'][0]['ContractName']}")
            print(f"  编译器: {data['result'][0]['CompilerVersion']}")
            return True
        else:
            print(f"  {Colors.WARNING}✗ 合约未验证{Colors.ENDC}")
            return False
            
    except Exception as e:
        print(f"{Colors.FAIL}[ERROR] {e}{Colors.ENDC}")
        return False

def detect_honeypot(token_address):
    """检测蜜罐代币"""
    print(f"\n{Colors.OKBLUE}[INFO] 检测蜜罐代币...{Colors.ENDC}")
    
    # 使用Honeypot.is API
    try:
        url = f"https://api.honeypot.is/v2/IsHoneypot"
        params = {
            'address': token_address,
            'chainID': 8453  # Base chainId
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get('honeypotResult', {}).get('isHoneypot'):
            print(f"  {Colors.FAIL}⚠ 警告: 检测到蜜罐特征!{Colors.ENDC}")
            return True
        else:
            print(f"  {Colors.OKGREEN}✓ 未检测到明显蜜罐特征{Colors.ENDC}")
            return False
            
    except Exception as e:
        print(f"{Colors.WARNING}[WARN] 无法完成检测: {e}{Colors.ENDC}")
        return None

def scan_for_terminal_contracts():
    """扫描Terminal Markets相关合约"""
    print(f"\n{Colors.OKBLUE}[INFO] 扫描Terminal Markets合约...{Colors.ENDC}")
    
    # 已知的相关地址（需要更新）
    known_addresses = [
        # "0x...",  # DX Terminal NFT
        # "0x...",  # Vault Factory
        # "0x...",  # Token Router
    ]
    
    print(f"  已知合约数量: {len(known_addresses)}")
    
    for addr in known_addresses:
        print(f"\n  检查: {addr}")
        analyze_contract(addr)
        check_contract_verification(addr)

def monitor_gas_prices():
    """监控Gas价格"""
    print(f"\n{Colors.OKBLUE}[INFO] 监控Gas价格...{Colors.ENDC}")
    
    while True:
        try:
            gas_price = w3.eth.gas_price
            gas_gwei = w3.from_wei(gas_price, 'gwei')
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # 根据价格显示不同颜色
            if gas_gwei < 0.01:
                color = Colors.OKGREEN
                status = "低"
            elif gas_gwei < 0.05:
                color = Colors.WARNING
                status = "中"
            else:
                color = Colors.FAIL
                status = "高"
            
            print(f"\r{color}[{timestamp}] Gas价格: {gas_gwei:.4f} Gwei ({status}){Colors.ENDC}", end='')
            
            time.sleep(10)
            
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}[INFO] 监控已停止{Colors.ENDC}")
            break
        except Exception as e:
            print(f"\n{Colors.FAIL}[ERROR] {e}{Colors.ENDC}")
            time.sleep(5)

def main_menu():
    """主菜单"""
    print_banner()
    
    print(f"{Colors.OKCYAN}请选择监控模式:{Colors.ENDC}")
    print("1. 监控大额交易")
    print("2. 监控NFT转移")
    print("3. 分析指定合约")
    print("4. 扫描Terminal Markets合约")
    print("5. 监控Gas价格")
    print("6. 检测蜜罐代币")
    print("0. 退出")
    
    choice = input(f"\n{Colors.BOLD}选择 (0-6): {Colors.ENDC}")
    
    if choice == "1":
        min_eth = float(input("最小金额 (ETH): ") or "1.0")
        monitor_large_transactions(min_eth)
    elif choice == "2":
        nft_addr = input("NFT合约地址 (留空监控所有): ").strip()
        monitor_nft_transfers(nft_addr if nft_addr else None)
    elif choice == "3":
        addr = input("合约地址: ").strip()
        analyze_contract(addr)
        check_contract_verification(addr)
    elif choice == "4":
        scan_for_terminal_contracts()
    elif choice == "5":
        monitor_gas_prices()
    elif choice == "6":
        addr = input("代币地址: ").strip()
        detect_honeypot(addr)
    elif choice == "0":
        print(f"{Colors.OKGREEN}再见!{Colors.ENDC}")
        return
    else:
        print(f"{Colors.FAIL}无效选择{Colors.ENDC}")
    
    input(f"\n{Colors.BOLD}按Enter返回主菜单...{Colors.ENDC}")
    main_menu()

if __name__ == "__main__":
    try:
        # 检查连接
        if w3.is_connected():
            print(f"{Colors.OKGREEN}✓ 已连接到Base网络{Colors.ENDC}")
            print(f"  最新区块: {get_latest_block()}")
            main_menu()
        else:
            print(f"{Colors.FAIL}✗ 无法连接到Base网络{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}[ERROR] {e}{Colors.ENDC}")
