// SPDX-License-Identifier: MIT

// Smart contract that lets anyone deposit ETH into the contract-
// Only the owner of the contract can withdraw the ETH
pragma solidity >=0.6.6 <0.9.0;

// Get the latest ETH/USD price from chainlink price feed
// import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
// import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

import "./AggregatorV3Interface.sol"; 


contract FundMe {
	// safe math library check uint256 for integer overflows
    
    //mapping to store which address depositeded how much ETH
    mapping(address => uint256) public addressToAmountFunded;
    // array of addresses who deposited
    address[] public funders;
    //address of the owner (who deployed the contract)
    address public owner;
    
    // the first person to deploy the contract is
    // the owner
    constructor() {
        owner = msg.sender;
    }
    
    // this functoin is marked as "payable" which means that it makes the contract able to hold funds
    function fund() public payable {
    	// 18 digit number to be compared with donated amount 
        uint256 minimumUSD = 50 * 10 ** 18; // the minimum amount in GWEI
        //is the donated amount less than 50USD?
        require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more ETH!");
        //if not, add to mapping and funders array
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }
    
    //function to get the version of the chainlink pricefeed
    function getVersion() public view returns (uint256){
        // to interact with an interface it's just like ineracting with a structure, which is :
        // TYPE VISABILTY NAME = TYPE(ADDRESS OF THE CONTRACT WHERE WE'RE INTERACTING WITH)
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        // the address "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e" is an address of a contract that returns the price feed of ETH/USD that implements the "AggregatorV3Interface" interface
        return priceFeed.version(); // running the function from the contract "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e"
    }
    
    function getPrice() public view returns(uint256){
        // this function makes the same call to the priceFeed in the contract (kind of creates another instence of the contract)
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        // because the function "latestRoundData" returns 5 variables but we only want one, we created a Tuple with 5 places but orders to save in the memory only the second one outof the 5 in the "answer" variable
        (,int256 answer,,,) = priceFeed.latestRoundData();
         // ETH/USD rate in 18 digit, to make it into *GWEI*
         return uint256(answer * 1000000000);
    }
    
    // 1000000000
    function getConversionRate(uint256 ethAmount) public view returns (uint256){
        uint256 ethPrice = getPrice(); // the ETH -> USD conversation rate
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000; // we need to divide by 1000000000000000000 because both ethPrice and ethAmount are in GWEI (1000000000*1000000000)
        // the actual ETH/USD conversation rate, after adjusting the extra 0s.
        return ethAmountInUsd; // the amount of 1 GWEI in Dollars
    }
    
    // let you use the Require statment in other functions
    // the order that the require statement in the first one means that before the contract is executed it will run he modifier
     
    modifier onlyOwner {
    	//is the message sender owner of the contract?
        require(msg.sender == owner);
        
        _;
    }
    
    // onlyOwner modifer will first check the condition inside it 
    // and 
    // if true, withdraw function will be executed 
    function withdraw() payable onlyOwner public {

        // trensfering all of the balance of the contract into the msg.sender
        payable(msg.sender).transfer(address(this).balance);

        
        //iterate through all the mappings and make them 0
        //since all the deposited amount has been withdrawn
        for (uint256 funderIndex=0; funderIndex < funders.length; funderIndex++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        //funders array will be initialized to 0
        funders = new address[](0);
    }
}



