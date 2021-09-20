# NOTE: The following tests begin by transferring assets to the deployed flashloan
# contract. this ensures that the tests pass with the base Flashloan implementation,
# i.e. one that does not implement any custom logic.
from scripts.tokens import tokens, curve_tokens
import brownie
from web3 import Web3

def test_set_tokens(acct, flashloan_v2):
    flashloan_v2.setTokens(
        tokens['dai'],
        curve_tokens['dai'],
        tokens['usdc'],
        curve_tokens['usdc'],
        {'from': acct}
    )
    assert flashloan_v2.tokensSet()

def test_collateralized_flashloan(acct, DAI, WMATIC, router, flashloan_v2):
    """
    Test a flashloan that borrows DAI.

    To use a different asset, swap DAI with any of the fixture names in `tests/conftest.py`
    """


    amount_to_loan = Web3.toWei(10, 'ether')
    fee = int(amount_to_loan * 0.0009)
    router.swapExactETHForTokens(0, [WMATIC.address, DAI.address], acct.address, 9999999999999999, {"from": acct, "value": fee * 2})

    DAI.transfer(flashloan_v2, fee, {"from": acct})
    assert DAI.balanceOf(flashloan_v2.address) == fee
    
    with brownie.reverts("Did not make profit"):
        flashloan_v2.flashloan(amount_to_loan, {"from": acct})

def test_returned_funds(acct, DAI, flashloan_v2):
    assert DAI.balanceOf(flashloan_v2.address) > 0

    before = DAI.balanceOf(acct.address)
    flashloan_v2.getProfit(DAI.address, {'from': acct})

    assert DAI.balanceOf(acct.address) > before


def test_under_collateralized_loan(acct, DAI, flashloan_v2):
    assert DAI.balanceOf(acct) >= 1
    assert DAI.balanceOf(flashloan_v2.address) == 0
    # Transfer 1 wei worth of DAI and initiate expensive flashloan
    DAI.transfer(flashloan_v2, 1, {"from": acct})
    amount = 1000000 * 10**18
    with brownie.reverts():
        flashloan_v2.flashloan(amount, {"from": acct})
