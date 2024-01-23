from manage_bd import read_users_table
from eth_account.messages import encode_defunct
import requests
import json
from web3 import Web3
import time
import asyncio
import aiohttp
from config import backend

w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/d499d5cfa57f45558c47f9fd7d1f7b3a"))

message = 'MhCvcDterUXVOyaicihBpnOVEOOaof'
formatted_message = encode_defunct(text=message)

private_key = '9dd135afa937d185928a69360a728f865a741646eff8a088b29f0d2cdce2474f'
signed_message = w3.eth.account.sign_message(formatted_message, private_key=private_key)
signature = signed_message.signature.hex()

print(signature)