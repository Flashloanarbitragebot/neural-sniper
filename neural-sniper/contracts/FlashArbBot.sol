// SPDX-License-Identifier: MIT
pragma solidity ^0.6.12;

import "@openzeppelin/contracts/math/SafeMath.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import "./aave/FlashLoanReceiverBase.sol";
import "./aave/ILendingPoolAddressesProvider.sol";
import "./aave/ILendingPool.sol";

import "./dex/IUniswapV2Router02.sol";

contract FlashArbBot is FlashLoanReceiverBase, Ownable, ReentrancyGuard {
    using SafeMath for uint256;

    IUniswapV2Router02 public uniswapV2;
    IUniswapV2Router02 public sushiswapV1;

    uint256 public minProfit; // in wei
    uint256 public slippageTolerance; // in basis points (e.g. 50 = 0.5%)
    bool public paused = false;

    event TradeExecuted(address asset, uint256 amount, uint256 profit);
    event ArbOutcome(uint256 profit, uint256 gas, address token, uint timestamp);

    modifier notPaused() {
        require(!paused, "Contract paused");
        _;
    }

    constructor(
        ILendingPoolAddressesProvider _provider,
        address _uni,
        address _sushi
    ) FlashLoanReceiverBase(_provider) public {
        uniswapV2 = IUniswapV2Router02(_uni);
        sushiswapV1 = IUniswapV2Router02(_sushi);
        minProfit = 1e16; // 0.01 ETH
        slippageTolerance = 50;
    }

    function togglePause() external onlyOwner {
        paused = !paused;
    }

    function updateParams(uint256 _minProfit, uint256 _slippage) external onlyOwner {
        minProfit = _minProfit;
        slippageTolerance = _slippage;
    }

    function executeArbOpportunity(
        address asset,
        uint256 amount
    ) external onlyOwner notPaused nonReentrant {
        address[] memory assets = new address[](1);
        assets[0] = asset;

        uint256[] memory amounts = new uint256[](1);
        amounts[0] = amount;

        uint256[] memory modes = new uint256[](1);
        modes[0] = 0;

        LENDING_POOL.flashLoan(
            address(this),
            assets,
            amounts,
            modes,
            address(this),
            "",
            0
        );
    }

    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata
    ) external override returns (bool) {
        require(msg.sender == address(LENDING_POOL), "Lender invalid");
        require(initiator == address(this), "Caller invalid");

        address asset = assets[0];
        uint256 borrowed = amounts[0];
        uint256 fee = premiums[0];

        // Swap 1: Uniswap
        uint256 received = _swap(asset, address(uniswapV2), borrowed);

        // Swap 2: Sushiswap
        uint256 finalAmount = _swap(address(received), address(sushiswapV1), received);

        uint256 totalOwed = borrowed.add(fee);
        require(finalAmount > totalOwed.add(minProfit), "Not profitable");

        IERC20(asset).approve(address(LENDING_POOL), totalOwed);

        emit TradeExecuted(asset, borrowed, finalAmount.sub(totalOwed));
        emit ArbOutcome(finalAmount.sub(totalOwed), tx.gasprice, asset, block.timestamp);
        return true;
    }

    function _swap(address tokenIn, address routerAddr, uint256 amountIn) internal returns (uint256) {
        IUniswapV2Router02 router = IUniswapV2Router02(routerAddr);
        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = address(0); // e.g. WETH

        uint256 minOut = amountIn.mul(10000 - slippageTolerance).div(10000);
        IERC20(tokenIn).approve(routerAddr, amountIn);

        uint[] memory amounts = router.swapExactTokensForETH(
            amountIn,
            minOut,
            path,
            address(this),
            block.timestamp
        );

        return amounts[amounts.length - 1];
    }
}
