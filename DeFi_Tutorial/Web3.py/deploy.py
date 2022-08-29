import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()


# Reading the file and dumping it into a variable called "simple_storage_file"
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.6.0")

# Solidity source code
# Doing all of the calculationsof the ABI and Bytecode
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

# Dumping the json data from the solcx into a file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]


# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 5777
# Setting Everoment Variables 
my_address = os.environ['ADDRESS']
private_key = os.environ['PRIVATE_KEY']

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction (Nonce)
nonce = w3.eth.getTransactionCount(my_address)
# Submit the transaction that deploys the contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Getting the Transaction Receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

##########################################################################################################

# Working with deployed Contracts

# Getting a contract from the Blockchain
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Running a Function from the contract and uploading the new state into the blockchain
greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())
