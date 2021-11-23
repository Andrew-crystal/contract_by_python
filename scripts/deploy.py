from brownie import FlashloanV2, accounts, config, network, interface, Contract
from web3 import Web3

def main():
    lending_pool = "0xd05e3E715d945B59290df0ae8eF85c1BdB684744"
    acct = accounts.add(config['wallets']['from_key'])
    flashloan = FlashloanV2.deploy(
            lending_pool,
            {"from": acct}
    )
    return flashloan