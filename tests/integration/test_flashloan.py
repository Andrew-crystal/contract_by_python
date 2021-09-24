from brownie.test import given, strategy
from web3 import Web3
import brownie
from scripts.utils import swap_eth_for_erc20
from hypothesis import settings


@given(amount=strategy("uint256", min_value=10))
@settings(max_examples=5)
def test_collateralized_flashloan(acct, DAI, flashloan_v2, amount, set_tokens):
    """
    Test a flashloan that borrows DAI.

    To use a different asset, swap DAI with any of the fixture names in `tests/conftest.py`
    """
    
    amount_to_loan = Web3.toWei(amount, 'ether')
    fee = int(amount_to_loan * 0.0009)
    assert amount > 0
    swap_eth_for_erc20(DAI, fee * 1.1, acct)
    assert DAI.balanceOf(acct) > fee
    DAI.transfer(flashloan_v2, fee, {"from": acct})
    with brownie.reverts("Did not make profit"):
        flashloan_v2.flashloan(amount_to_loan, {"from": acct})

