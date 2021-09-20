from brownie import FlashloanV2, accounts, network, interface, Contract, config
from web3 import Web3
from scripts.tokens import tokens, curve_tokens
from scripts.utils import *

flashloan_amount = Web3.toWei(10000, 'ether')
fee_payment = flashloan_amount * 0.0009
lending_pool = "0xd05e3E715d945B59290df0ae8eF85c1BdB684744"



def main():
    if 'fork' in network.show_active():
        acct = accounts.at('0xe7804c37c13166fF0b37F5aE0BB07A3aEbb6e245', force=True) # random whale
        flashloan_addr = None
    else:
        acct = accounts.add(config['wallets']['from_key'])
        flashloan_addr = input('Enter deployed flashloan address')

    flashloan(acct, 'dai', 'usdc', flashloan_addr)


def flashloan(acct, from_token_name, to_token_name, flashloan_address):
    print(network.show_active())
    from_token = tokens[from_token_name]
    to_token = tokens[to_token_name]
    from_curve_token = curve_tokens[from_token_name]
    to_curve_token = curve_tokens[to_token_name]
    
    if flashloan_address:
        flashloan_address = Contract(flashloan_address)
        
    else:
        flashloan = FlashloanV2.deploy(
            lending_pool,
            {"from": acct}
        )
    flashloan.setTokens(
        from_token,
        from_curve_token,
        to_token,
        to_curve_token,
        {'from': acct}
        )


    swap_eth_for_erc20(from_token, fee_payment, acct)
    print(f'Received {balanceOf(from_token, acct.address)} {from_token_name}')
   
    flashloan = FlashloanV2[len(FlashloanV2) - 1]
    bal = balanceOf(from_token, flashloan)

    if bal < fee_payment:
        print(f"Funding Flashloan contract with {from_token_name}...")
        ERC20(from_token).transfer(flashloan, fee_payment, {"from": acct})
        print(f'Funded flashloan contract with {from_token_name}!!')


    starting_contract_balance = balanceOf(from_token, flashloan.address)
    print("Executing Flashloan...")

    tx = flashloan.flashloan(flashloan_amount, {"from": acct})

    contract_balance  = balanceOf(from_token, flashloan.address)
    profit = Web3.fromWei(contract_balance, "ether") - Web3.fromWei(starting_contract_balance, "ether")
    print(f'Flashloaned {Web3.fromWei(flashloan_amount, "ether")} {from_token_name}')
    print(f'Starting Contract {from_token_name} Balance: {Web3.fromWei(starting_contract_balance, "ether")}')
    print(f'Contract {from_token_name} Balance After Flashloan: {Web3.fromWei(contract_balance, "ether")}')
    print(f'Profit (ether): {profit}')
    current_from_bal = balanceOf(from_token, acct.address)

    flashloan.getProfit(from_token, {'from': acct})

    after_withdraw_bal = balanceOf(from_token, acct.address) - current_from_bal
    print('Funds Sent back to Deployer:', Web3.fromWei(after_withdraw_bal, "ether"))
    return flashloan