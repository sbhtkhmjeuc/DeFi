# clearfrom distutils.file_util import copy_file
from http.client import HTTPException
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()



# Reading the Solidity code with the "file" module, and moving it into a local variable
with open(
    r"/home/sbhtkhmjeuc/Desktop/DeFi/DeFi/DeFi_Tutorial/SimpleStorage/SimpleStorage.sol", "r"
) as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

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
    r"/home/sbhtkhmjeuc/Desktop/DeFi/DeFi/DeFi_Tutorial/Web3.py/compiled_sol.json", "w"
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
chain_id = 1337
my_address = "0x2B4f7E4f57459B451f7Da2236766D614BE49671f"
private_key = "0x3eddc7c98f4ee67e9639b1a3099caf4d0d389157dfdec5c7877e2d969b241b52"
# you can also create an envoriment variable for the private key and access it with
# private_key = os.getenv("PRIVATE_KEY")

# Creating a Contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(
    my_address
)  # getting th nonce for the current address

# Building -> Signing -> Seding

# Building
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

# Signing
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# to create enviroment variables in linux you need to to into the terminal and type "export VARIABLE",
# and than to view it you need to type in the terminal "echo $VARIABLE"
# you can to the Obsidian Notebook and find a file named "What are Environment Variables ? with Examples on Windows & Linux"
# print(signed_txn)
