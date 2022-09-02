// SPDX-License-Identifier: MIT


pragma solidity >=0.6.0;
contract SimpleStorage {
    uint256 favoriteNumber; // when you don't initilize a numnber variable it will initialized to 0!
    bool favoriteBool; // you NEED to run  
    
    struct People {
        uint256 favoriteNumber;
        string name;
    }
    
    People[] public people; // an Array of a People structure that called "people"
    mapping(string => uint256) public nameToFavoriteNumber; 
    // a mapping structure that called "nameToFavoriteNumber" between a string and a big number
    
    // function that is stores the input into the favoriteNumber field in a instance of a People structure
    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }
    
    // a function that retrives the favoriteNumber from a instace of a People structure
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }
    
    // a function that adds an instance of Poeple structure into the "nameToFavoriteNumber" mapping structure
    function addPerson(string memory _name, uint256 _favoriteNumber) public{
        people.push(People(_favoriteNumber, _name)); // pushing a instance into the mappinf structure
        nameToFavoriteNumber[_name] = _favoriteNumber; // adding a favoriteNumber to a Poeple structure instance
    }    
    
}
