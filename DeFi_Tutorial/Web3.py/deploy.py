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

w3 = Web3(Web3.HTTPProvider(" "))
