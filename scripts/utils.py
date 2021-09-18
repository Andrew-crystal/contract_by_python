from brownie import interface
from scripts.tokens import tokens

def swap_eth_for_erc20(erc20_address, amount, acct):
    router = interface.IUniswapRouterV2("0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff") #Polygon
    router.swapExactETHForTokens(0, [tokens['wmatic'], erc20_address], acct.address, 9999999999999999, {"from": acct, "value": amount})

def balanceOf(erc20_address, account_address):
        return ERC20(erc20_address).balanceOf(account_address)

def ERC20(token_address):
    return interface.IERC20(token_address)