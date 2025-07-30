const { ethers } = require("hardhat");

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying with:", deployer.address);

    const FlashArbBot = await ethers.getContractFactory("FlashArbBot");
    const bot = await FlashArbBot.deploy(
        "0xYourAaveProvider",
        "0xUniswapRouter",
        "0xSushiRouter"
    );

    await bot.deployed();
    console.log("FlashArbBot deployed to:", bot.address);
}
main().catch((e) => console.error(e));
