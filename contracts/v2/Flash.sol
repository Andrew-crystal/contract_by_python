// pragma solidity ^0.6.6;

// import "./aave/FlashLoanReceiverBaseV2.sol";
// import "../../interfaces/v2/ILendingPoolAddressesProviderV2.sol";
// import "../../interfaces/v2/ILendingPoolV2.sol";
// import "../../interfaces/IUniswapRouterV2.sol";
// import "../../interfaces/curve/StableSwap.sol";
// // import "../utils/Withdrawable.sol"
// contract Flash is FlashLoanReceiverBaseV2, Withdrawable {
//     address public constant ROUTER = 0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff;
//     address public constant ATRIV1 = 0x3FCD5De6A9fC8A99995c406c77DDa3eD7E406f81; // v1
//     address public constant ATRIV3 = 0x1d8b86e3D88cDb2d34688e87E72F388Cb541B7C8; // v3
//     address public constant LENDING_POOL_ADDRESS = 0x8dFf5E27EA6b7AC08EbFdf9eB090F32ee9a30fcf;
//     mapping (address => uint8) public tokenToIndex;
//     uint public owed;
//     uint public bal;

//     constructor(address _addressProvider) FlashLoanReceiverBaseV2(_addressProvider) public {
//         tokenToIndex[0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063] = 0;
//         tokenToIndex[0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174] = 1;
//         tokenToIndex[0xc2132D05D31c914a87C6611C10748AEb04B58e8F] = 2;
//         tokenToIndex[0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619] = 3;
//         tokenToIndex[0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6] = 4;
//     }

//     function executeOperation(
//         address[] calldata assets,
//         uint256[] calldata amounts,
//         uint256[] calldata premiums,
//         address initiator,
//         bytes calldata params,
//         address fromToken,
//         address toToken
//     )
//         external
//         override
//         returns (bool)
//     {

//         owed = amounts[0].add(premiums[0]);
//         swap_curve(ATRIV3, IERC20(fromToken).balanceOf(address(this)));

//         uint256 fbal = IERC20(fromToken).balanceOf(address(this));
//         uint256 tbal = IERC20(toToken).balanceOf(address(this));
//         require(tbal > fbal, 'CURVE SWAP FAILED');

//         swap_quickswap(IERC20(toToken).balanceOf(address(this)));

//         uint256 f2bal = IERC20(fromToken).balanceOf(address(this));
//         uint256 t2bal = IERC20(toToken).balanceOf(address(this));
//         require(f2bal > t2bal, 'UNISWAP SWAP FAILED');

//         bal = IERC20(assets[0]).balanceOf(address(this));
//         require(bal > owed, "Did not make profit");
        

        
//         // Approve the LendingPool contract allowance to *pull* the owed amount
//         for (uint i = 0; i < assets.length; i++) {
//             uint amountOwing = amounts[i].add(premiums[i]);
//             IERC20(assets[i]).approve(address(LENDING_POOL), amountOwing);
//         }
        
//         return true;
//     }


//     function swap_quickswap(uint256 amount) public {
//         address[] memory path;
//         path = new address[](2);
//         path[0] = toToken;
//         // path[1] = WMATIC;
//         path[1] = fromToken;
//         IUniswapRouterV2(ROUTER).swapExactTokensForTokens(amount, 1, path, address(this), block.timestamp + 99999999);
//     }

//     function swap_curve(address from_pool, address to_pool, uint256 amount) public {
//         StableSwap(from_pool).exchange_underlying(fromTokenInd, toTokenInd, amount, 1);

//         StableSwap(to_pool).exchange_underlying(toTokenInd, fromTokenInd, IERC20(toToken).balanceOf(address(this)), 1);
//     }

//     function swap_curve(address from_pool, uint256 amount) public {
//         StableSwap(from_pool).exchange_underlying(fromTokenInd, toTokenInd, amount, 1);
//     }


//     function _flashloan(address[] memory assets, uint256[] memory amounts, address fromToken, address toToken) internal {
//         address receiverAddress = address(this);

//         address onBehalfOf = address(this);
//         bytes memory params = "";
//         uint16 referralCode = 0;

//         uint256[] memory modes = new uint256[](assets.length);

//         // 0 = no debt (flash), 1 = stable, 2 = variable
//         for (uint256 i = 0; i < assets.length; i++) {
//             modes[i] = 0;
//         }

//         LENDING_POOL.flashLoan(
//             receiverAddress,
//             assets,
//             amounts,
//             modes,
//             onBehalfOf,
//             params,
//             referralCode,
//             fromToken,
//             toToken
//         );
//     }


//     function flashloan(address fromToken, address toToken, uint _amount) public onlyOwner {
//         bytes memory data = "";
//         uint amount = _amount;

//         address[] memory assets = new address[](1);
//         assets[0] = fromToken;

//         uint256[] memory amounts = new uint256[](1);
//         amounts[0] = amount;

//         _flashloan(assets, amounts, fromToken, toToken);
//     }

//     function setTokens(address from, uint256 fromInd, address to, uint256 toInd) public onlyOwner {
//         fromToken = from;
//         fromTokenInd = fromInd;
//         toToken = to;
//         toTokenInd = toInd;
//         tokensSet = true;
//         IERC20(toToken).approve(ROUTER, type(uint256).max);
//         // IERC20(toToken).approve(ATRIV3, type(uint256).max);
//         // IERC20(fromToken).approve(ROUTER, type(uint256).max);
//         IERC20(fromToken).approve(ATRIV3, type(uint256).max);
//     }

//     function getProfit(address _asset) public onlyOwner {
//         // IERC20(fromToken).transfer(msg.sender, IERC20(fromToken).balanceOf(address(this)));
//         withdraw(_asset);
//     }
// }