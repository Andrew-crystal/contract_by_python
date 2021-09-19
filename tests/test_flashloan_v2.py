# NOTE: The following tests begin by transferring assets to the deployed flashloan
# contract. this ensures that the tests pass with the base Flashloan implementation,
# i.e. one that does not implement any custom logic.
from scripts.tokens import tokens, curve_tokens
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

def test_over_collateralized_flashloan(acct, DAI, WMATIC, router, flashloan_v2):
    """
    Test a flashloan that borrows DAI.

    To use a different asset, swap DAI with any of the fixture names in `tests/conftest.py`
    """


    # purchase DAI on uniswap
    amount_to_loan = Web3.toWei(0.01, 'ether')
    fee = int(amount_to_loan * 0.0009)
    router.swapExactETHForTokens(0, [WMATIC.address, DAI.address], acct.address, 9999999999999999, {"from": acct, "value": Web3.toWei(100000000, 'ether')})
    balance = DAI.balanceOf(acct)


    DAI.transfer(flashloan_v2, balance, {"from": acct})
    assert DAI.balanceOf(flashloan_v2.address) == balance
    flashloan_v2.flashloan(amount_to_loan / 10, {"from": acct})

