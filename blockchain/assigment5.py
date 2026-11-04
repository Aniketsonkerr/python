// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract VariableScope {
    // 1. State Variables (Stored on Blockchain storage)
    string public stateText = "State Variable: Stored in Blockchain Storage";
    uint256 public count = 100;
    address public owner;

    constructor() {
        owner = msg.sender; // msg.sender is a Global Variable
    }

    // Function demonstrating Local Variables & Scope
    function scopeDemo() public view returns (
        string memory localStr,
        uint256 totalSum,
        address senderAddress,
        uint256 blockTimestamp
    ) {
        // 2. Local Variables (Stored in Memory / Stack during execution)
        uint256 localValue = 50;
        string memory tempMessage = "Local Variable: Temporary Execution Scope";

        // Accessing State Variable and combining with Local Variable
        totalSum = count + localValue;
        localStr = tempMessage;

        // 3. Global Variables (Provides EVM & Blockchain Information)
        senderAddress = msg.sender;     // Address of caller
        blockTimestamp = block.timestamp; // Current block timestamp
    }

    // Function to update state variable
    function updateCount(uint256 _newCount) public {
        // _newCount is a local function parameter variable
        count = _newCount;
    }
}