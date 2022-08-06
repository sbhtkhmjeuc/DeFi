// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "./SimpleStorage.sol"; // importing the SimpleStorage contract

contract StorageFactory is SimpleStorage { // inherting from the SimpleStorage
    
    SimpleStorage[] public simpleStorageArray; // an array of SimpleStorage instances called "simpleStorageArray"
    
    // function that creates a new SimpleStorage instance and pushes it into the array above
    function createSimpleStorageContract() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }
    

    function sfStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber) public {
        // this line has an explicit cast to the address type and initializes a new SimpleStorage object from the address
        // running a functoin from the SimpleStorage contract on an SimpleStorage instance that was created here 
        SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).store(_simpleStorageNumber);
    }
    
    function sfGet(uint256 _simpleStorageIndex) public view returns (uint256) {
        // this line has an explicit cast to the address type and initializes a new SimpleStorage object from the address
        // just like above, running a function from SimpleStorage contract on an instance that was created here 
        return SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).retrieve();
    }
}
