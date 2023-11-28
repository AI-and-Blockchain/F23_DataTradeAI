// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


contract MLContract {
    address public owner;

    event ModelOutputReceived(uint256 modelOutput);
    event DataReceived(uint256 inputData, uint256 modelOutput);
    event DataSent(uint256 inputData, uint256 modelOutput);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function sendInput(uint256 inputData) external onlyOwner {

        emit DataSent(inputData, 0);
    }

    function recOutput(uint256 _modelOutput) external {

        emit ModelOutputReceived(_modelOutput);
    }
}