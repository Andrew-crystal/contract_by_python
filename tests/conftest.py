import pytest

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

@pytest.fixture(autouse=True)
def setup(module_isolation):
    """
    Isolation setup fixture.

    This ensures that each test runs against the same base environment.
    """
    pass


@pytest.fixture(scope="module")
def aave_lending_pool_v2(Contract):
    """
    Yield a `Contract` object for the Aave lending pool address provider.
    """
    yield Contract("0xd05e3E715d945B59290df0ae8eF85c1BdB684744")


@pytest.fixture(scope="module")
def acct(accounts):
    yield accounts.at('0xe7804c37c13166fF0b37F5aE0BB07A3aEbb6e245', force=True)


@pytest.fixture(scope="module")
def flashloan_v2(FlashloanV2, aave_lending_pool_v2, acct):
    """
    Deploy a `Flashloan` contract from `web3.eth.accounts[0]` and yields the
    generated object.
    """
    yield FlashloanV2.deploy(aave_lending_pool_v2, {"from": acct})

@pytest.fixture(scope="module")
def set_tokens(acct, flashloan_v2):
    flashloan_v2.setTokens(
        tokens['dai'],
        curve_tokens['dai'],
        tokens['usdc'],
        curve_tokens['usdc'],
        {'from': acct}
    )
    assert flashloan_v2.tokensSet()

@pytest.fixture(scope="module")
def WMATIC(Contract):
    yield Contract(tokens['wmatic'])


@pytest.fixture(scope="module")
def USDC(Contract):
    yield Contract(tokens['usdc'])


@pytest.fixture(scope="module")
def DAI(Contract):
    yield Contract(tokens['dai'])
