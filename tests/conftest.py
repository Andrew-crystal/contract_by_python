import pytest
from scripts.tokens import tokens


@pytest.fixture(autouse=True)
def setup(fn_isolation):
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
def flashloan_v2(FlashloanV2, aave_lending_pool_v2, accounts):
    """
    Deploy a `Flashloan` contract from `web3.eth.accounts[0]` and yields the
    generated object.
    """
    yield FlashloanV2.deploy(aave_lending_pool_v2, {"from": accounts[0]})


@pytest.fixture(scope="module")
def USDC(Contract):
    yield Contract(tokens['dai'])


@pytest.fixture(scope="module")
def DAI(Contract):
    yield Contract(tokens['usdc'])
