# NOTE: The following tests begin by transferring assets to the deployed flashloan
# contract. this ensures that the tests pass with the base Flashloan implementation,
# i.e. one that does not implement any custom logic.
from scripts.tokens import tokens, curve_tokens

def test_set_tokens(acct, flashloan_v2):
    flashloan_v2.setTokens(
        tokens['dai'],
        curve_tokens['dai'],
        tokens['usdc'],
        curve_tokens['usdc'],
        {'from': acct}
    )

def test_dai_flashloan(acct, DAI, WMATIC, router, flashloan_v2):
    """
    Test a flashloan that borrows DAI.

    To use a different asset, swap DAI with any of the fixture names in `tests/conftest.py`
    """


    # purchase DAI on uniswap
    amount = 10 * 10**18
    router.swapExactETHForTokens(0, [WMATIC.address, DAI.address], acct.address, 9999999999999999, {"from": acct, "value": amount})

    # transfer DAI to the flashloan contract
    balance = DAI.balanceOf(acct)
    DAI.transfer(flashloan_v2, balance, {"from": acct})
    amount = 100 * 10**18
    flashloan_v2.flashloan(amount, {"from": acct})
