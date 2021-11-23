import brownie
from web3 import Web3
from brownie import interface


def swap_eth_for_erc20(erc20_address, amount, acct):
    router = interface.IUniswapRouterV2("0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff") #Polygon
    router.swapExactETHForTokens(0, ["0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270", erc20_address], acct.address, 9999999999999999, {"from": acct, "value": amount})

def test_curve_swap(acct, DAI, USDC, flashloan_v2, set_tokens):
    assert flashloan_v2.fromToken() == DAI.address
    assert flashloan_v2.toToken() == USDC.address
    assert USDC.balanceOf(flashloan_v2) == 0

    amount_to_send= Web3.toWei(100, 'ether')
    swap_eth_for_erc20(DAI, amount_to_send * 1.1, acct)

    DAI.transfer(flashloan_v2, amount_to_send, {"from": acct})
    starting_balance = DAI.balanceOf(flashloan_v2.address)
    curve_pool = "0x1d8b86e3D88cDb2d34688e87E72F388Cb541B7C8"

    flashloan_v2.swap_curve(curve_pool, DAI.balanceOf(flashloan_v2.address),  {"from": acct})
    assert USDC.balanceOf(flashloan_v2.address) > 0
    assert DAI.balanceOf(flashloan_v2.address) == 0

    flashloan_v2.swap_quickswap(USDC.balanceOf(flashloan_v2.address), {"from": acct})
    assert DAI.balanceOf(flashloan_v2.address) > 0
    assert USDC.balanceOf(flashloan_v2.address) == 0
    ending_balance = DAI.balanceOf(flashloan_v2.address)
    assert ending_balance > starting_balance
   