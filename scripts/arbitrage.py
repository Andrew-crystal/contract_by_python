from brownie import FlashloanV2, accounts, network, interface, Contract, config
from web3 import Web3
import random

CURVE_ROUTER = "0x1d8b86e3D88cDb2d34688e87E72F388Cb541B7C8"
UNI_ROUTER = "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff"
LENDING_POOL = '0xd05e3E715d945B59290df0ae8eF85c1BdB684744'
ACCT =  accounts[8]
CURVE_SWAP = interface.StableSwap(CURVE_ROUTER)
UNI_SWAP = interface.IUniswapRouterV2(UNI_ROUTER)
AMOUNT_STABLE = 5000
AMOUNT_ETH = 2
AMOUNT_BTC = 0.1

def main():
    if 'fork' not in network.show_active():
        acct = connect_fork()
        flashloan = FlashloanV2.deploy(
            LENDING_POOL,
            {"from": acct}
    )
    flashloan_addr = input('Enter deployed flashloan address')
    

    approve_all()
    token_names = ['dai', 'usdc', 'usdt', 'wbtc', 'weth']
    all_token_pairs = [(a, b) for idx, a in enumerate(token_names) for b in token_names[idx + 1:]]

    for pair in all_token_pairs:
        profitable, from_token, to_token, amount =  test_arb(*pair)

        if profitable:
            acct = connect_mainnet()
            flashloan = Contract(flashloan_addr)
            flashloan.setTokens(
            from_token,
            curve_tokens[from_token],
            to_token,
            curve_tokens[to_token],
            {'from': acct}
            )
            flashloan.flashloan(amount, {"from": acct})
            flashloan.getProfit(from_token, {'from': acct})
            acct = connect_fork()


def test_arb(from_token, to_token):
    # SET UP
    from_address = tokens[from_token]
    to_address = tokens[to_token]
    from_index = curve_tokens[from_token]
    to_index = curve_tokens[to_token]

    decimals = int(ERC20(from_address).decimals())

    if from_token in ['dai', 'usdc', 'usdt']:
        amount = AMOUNT_STABLE * 10 ** decimals
    elif from_token == 'wbtc':
        amount = AMOUNT_BTC * 10 ** decimals
    else:
        amount = AMOUNT_ETH * 10 ** decimals

    swap_eth_for_erc20(from_address, amount * 1.1, ACCT)

    # ARBITRAGE
    starting_from = balanceOf(from_address, ACCT.address)
    print(f"Starting balance of {from_token}: {starting_from}")
    print(f'ARBITRAGING {amount} {from_token}')
    CURVE_SWAP.exchange_underlying(from_index, to_index, amount, 1, {"from": ACCT})
    UNI_SWAP.swapExactTokensForTokens(balanceOf(to_address, ACCT.address), 1, [to_address, from_address], ACCT.address, 9999999999999999, {'from': ACCT})
    ending_from = balanceOf(from_address, ACCT.address)
    profit = ending_from - starting_from
    print(f"PAIR: ({from_token}, {to_token})\nARBITRAGE PROFIT: {profit} wei")
    if profit > 0:
        return (True, from_address, to_address, amount)
    return (False, from_address, to_address, amount)
 
   
def connect_mainnet():
    network.disconnect()
    network.connect('polygon-main')
    return accounts.add(config['wallets']['from_key'])

def connect_fork():
    network.disconnect()
    network.connect('polygon-main-fork')
    return accounts[0]

def approve_all():
    for token in [tokens[token] for token in tokens.keys() if token != 'wmatic']:
        ERC20(token).approve(CURVE_ROUTER, 1_000_000_000_000 * 10**18, {"from": ACCT})
        ERC20(token).approve(UNI_ROUTER, 1_000_000_000_000 * 10**18, {"from": ACCT})


def swap_eth_for_erc20(erc20_address, amount_out, acct):
    router = interface.IUniswapRouterV2("0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff") #Polygon
    router.swapETHForExactTokens(amount_out, [tokens['wmatic'], erc20_address], acct.address, 9999999999999999, {"from": acct, "value": 10000 * 10**18})

def balanceOf(erc20_address, account_address):
        return ERC20(erc20_address).balanceOf(account_address)

def ERC20(token_address):
    return interface.IERC20(token_address)

tokens = {
    'wmatic': "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
    'dai': "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
    'usdc': "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    'usdt': "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
    'weth': "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
    'wbtc': "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6"
    }

curve_tokens = {
    'dai': 0,
    'usdc': 1,
    'usdt': 2,
    'wbtc': 3,
    'weth': 4
}