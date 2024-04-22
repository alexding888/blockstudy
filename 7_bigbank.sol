// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

import "./5_bank_contract.sol";

contract DAO {

    event Received(address from, address to, uint amount);
    receive() external payable {
        emit Received(msg.sender, address(this), msg.value); 
    }

    function withdraw(address payable bank, uint amount) public {
        BigBank(bank).withdraw(amount);
    }
}

contract BigBank is Bank {
    
    modifier minimumDeposit {
        require (msg.value > 0.001 ether, "Deposit value must be larger than 0.001 ether");
        _;
    }

    receive() external payable override  minimumDeposit {
        balances[msg.sender] += msg.value;
        updateTopThree(msg.sender);
    }

    function delegateOwner(address newOwner) public {
        require(msg.sender == owner, "Only owner can delegate ownership to new address");
        owner = newOwner;
    }

}