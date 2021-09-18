pragma solidity ^0.6.12;

interface StableSwap {
    function exchange_underlying(uint256 assetA, uint256 assetB, uint256 amount, uint256 minAmount) external;
}