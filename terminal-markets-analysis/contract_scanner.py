#!/usr/bin/env python3
"""
Terminal Markets 合约地址扫描器
通过分析前端代码和链上活动来识别相关合约
"""

import requests
import re
import json
from web3 import Web3
from typing import List, Dict, Set

class ContractScanner:
    def __init__(self):
        self.base_rpc = "https://mainnet.base.org"
        self.w3 = Web3(Web3.HTTPProvider(self.base_rpc))
        self.found_addresses = set()
        
    def scan_frontend_js(self) -> Set[str]:
        """扫描前端JavaScript代码中的合约地址"""
        print("[*] 扫描前端JavaScript代码...")
        
        addresses = set()
        
        try:
            # 获取主页面
            response = requests.get("https://www.terminal.markets/")
            html = response.text
            
            # 提取所有JavaScript文件URL
            js_files = re.findall(r'src="(/_next/static/[^"]+\.js)"', html)
            
            print(f"[+] 找到 {len(js_files)} 个JavaScript文件")
            
            for js_file in js_files[:10]:  # 限制前10个文件
                try:
                    js_url = f"https://www.terminal.markets{js_file}"
                    js_response = requests.get(js_url, timeout=10)
                    js_content = js_response.text
                    
                    # 查找以太坊地址模式
                    found = re.findall(r'0x[a-fA-F0-9]{40}', js_content)
                    
                    for addr in found:
                        if self.is_valid_address(addr):
                            addresses.add(addr)
                            print(f"  [+] 发现地址: {addr}")
                            
                except Exception as e:
                    print(f"  [-] 处理 {js_file} 失败: {e}")
                    
        except Exception as e:
            print(f"[-] 扫描失败: {e}")
            
        return addresses
    
    def is_valid_address(self, address: str) -> bool:
        """验证地址是否有效且不是常见的零地址"""
        if not Web3.is_address(address):
            return False
        
        # 排除零地址和常见的无效地址
        invalid = [
            "0x0000000000000000000000000000000000000000",
            "0x0000000000000000000000000000000000000001",
            "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",  # ETH placeholder
        ]
        
        return address not in invalid
    
    def check_contract(self, address: str) -> Dict:
        """检查地址是否为合约并获取信息"""
        try:
            code = self.w3.eth.get_code(address)
            
            if len(code) > 2:
                balance = self.w3.eth.get_balance(address)
                
                return {
                    "address": address,
                    "is_contract": True,
                    "code_size": len(code),
                    "balance": self.w3.from_wei(balance, 'ether'),
                    "balance_wei": balance
                }
            else:
                return {
                    "address": address,
                    "is_contract": False
                }
                
        except Exception as e:
            return {
                "address": address,
                "error": str(e)
            }
    
    def scan_opensea_nft(self) -> List[str]:
        """尝试从OpenSea获取NFT合约地址"""
        print("[*] 扫描OpenSea NFT合约...")
        
        addresses = []
        
        try:
            # OpenSea API (可能需要API key)
            url = "https://api.opensea.io/api/v1/collection/dxterminal"
            headers = {
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # 提取合约地址
                if "collection" in data:
                    contracts = data["collection"].get("primary_asset_contracts", [])
                    for contract in contracts:
                        addr = contract.get("address")
                        if addr:
                            addresses.append(addr)
                            print(f"  [+] NFT合约: {addr}")
                            
        except Exception as e:
            print(f"[-] OpenSea扫描失败: {e}")
            
        return addresses
    
    def scan_recent_transactions(self, blocks: int = 1000) -> Set[str]:
        """扫描最近区块中的大额交易"""
        print(f"[*] 扫描最近 {blocks} 个区块...")
        
        addresses = set()
        
        try:
            latest_block = self.w3.eth.block_number
            start_block = latest_block - blocks
            
            print(f"[+] 当前区块: {latest_block}")
            print(f"[+] 扫描范围: {start_block} - {latest_block}")
            
            # 分批扫描
            batch_size = 100
            for i in range(0, blocks, batch_size):
                from_block = start_block + i
                to_block = min(from_block + batch_size - 1, latest_block)
                
                try:
                    # 获取区块中的交易
                    for block_num in range(from_block, to_block + 1):
                        block = self.w3.eth.get_block(block_num, full_transactions=True)
                        
                        for tx in block.transactions:
                            # 检查大额交易
                            value_eth = self.w3.from_wei(tx['value'], 'ether')
                            
                            if value_eth >= 1.0:  # 大于1 ETH
                                if tx['to']:
                                    addresses.add(tx['to'])
                                    
                    print(f"  [+] 已扫描到区块 {to_block}")
                    
                except Exception as e:
                    print(f"  [-] 扫描区块 {from_block}-{to_block} 失败: {e}")
                    
        except Exception as e:
            print(f"[-] 扫描失败: {e}")
            
        return addresses
    
    def analyze_addresses(self, addresses: Set[str]):
        """分析所有发现的地址"""
        print(f"\n[*] 分析 {len(addresses)} 个地址...")
        
        contracts = []
        
        for addr in addresses:
            info = self.check_contract(addr)
            
            if info.get("is_contract"):
                contracts.append(info)
                print(f"\n[+] 合约发现:")
                print(f"    地址: {info['address']}")
                print(f"    代码大小: {info['code_size']} bytes")
                print(f"    余额: {info['balance']} ETH")
                
        return contracts
    
    def save_results(self, contracts: List[Dict], filename: str = "found_contracts.json"):
        """保存结果到文件"""
        with open(filename, 'w') as f:
            json.dump(contracts, f, indent=2)
        print(f"\n[+] 结果已保存到 {filename}")
    
    def run_full_scan(self):
        """执行完整扫描"""
        print("=" * 60)
        print("Terminal Markets 合约地址扫描器")
        print("=" * 60)
        
        all_addresses = set()
        
        # 1. 扫描前端代码
        frontend_addrs = self.scan_frontend_js()
        all_addresses.update(frontend_addrs)
        
        # 2. 扫描OpenSea
        opensea_addrs = self.scan_opensea_nft()
        all_addresses.update(opensea_addrs)
        
        # 3. 分析所有地址
        contracts = self.analyze_addresses(all_addresses)
        
        # 4. 保存结果
        if contracts:
            self.save_results(contracts)
        
        print("\n" + "=" * 60)
        print(f"扫描完成! 共发现 {len(contracts)} 个合约")
        print("=" * 60)
        
        return contracts

if __name__ == "__main__":
    scanner = ContractScanner()
    scanner.run_full_scan()
