require("@nomiclabs/hardhat-ethers");
require("dotenv").config();

module.exports = {
    solidity: "0.6.12",
    networks: {
        goerli: {
            url: process.env.INFURA_URL,
            accounts: [process.env.PRIVATE_KEY]
        }
    }
};

