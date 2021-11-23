# NOTE: The following tests begin by transferring assets to the deployed flashloan
# contract. this ensures that the tests pass with the base Flashloan implementation,
# i.e. one that does not implement any custom logic.

from brownie import interface
from web3 import Web3
import brownie


def test_flashloan(acct, flashloan_v2, set_tokens):


    amount_to_loan = Web3.toWei(100, 'ether')
  
    
    with brownie.reverts("Did not make profit"):
        flashloan_v2.flashloan(amount_to_loan, {"from": acct})
