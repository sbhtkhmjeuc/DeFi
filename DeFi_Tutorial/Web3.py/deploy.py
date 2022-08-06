from distutils.file_util import copy_file
from http.client import HTTPException
from solcx import compile_standard
import json
from web3 import Web3

# Reading the Solidity code with the "file" module, and moving it into a local variable
with open(
    r"C:\Users\sbhtk\Desktop\DeFi\DeFi_Tutorial\SimpleStorage\SimpleStorage.sol", "r"
) as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# Complie Out Solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    # all of the things that are stored in the "compiled_sol" variable (you can see that when you're printing)
                    # ABI -> Application Binary Interface
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open(
    r"C:\Users\sbhtk\Desktop\DeFi\DeFi_Tutorial\Web3.py\compiled_sol.json", "w"
) as file:
    json.dump(compiled_sol, file)

# Getting the Bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Getting the ABI
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 5777
my_address = "0x4372873dB4Ae7E90ebB5E796254aB6C272102C3d"
private_key = "0xc39ba919d594eb798c105a741fd62240ae94a85b70b1d0e2b2bb89d8a7d9d3ed"

# Creating a Contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(my_address) # getting th nonce for the current address

# Building -> Signing -> Seding

# Building 
transaction = SimpleStorage.constructor().buildTransaction({"chainId":chain_id, "from":my_address, "nonce":nonce})

# Signing
signed_txn = w3.eth.account.sign_transaction(transaction,private_key=private_key)

# to create enviroment variables in linux you need to to into the terminal and type "export VARIABLE", 
# and than to view it you need to type in the terminal "echo $VARIABLE" 