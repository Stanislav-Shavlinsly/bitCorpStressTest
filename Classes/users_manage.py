from manage_bd import read_users_table
from eth_account.messages import encode_defunct
import requests
import json
from web3 import Web3
import time
import asyncio
import aiohttp
from config import backend


class Users:
    def __init__(self, user):
        self.id = user['id']
        self.address = user['address']
        self.private_key = user['private_key']
        self.token = None
        self.message = None


    @staticmethod
    def signed(message, private_key):
        w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/d499d5cfa57f45558c47f9fd7d1f7b3a"))
        # msg = f"Sign a message to log in via MetaMask: {message}"
        message = encode_defunct(text=message)
        signed_message = w3.eth.account.sign_message(message, private_key)
        signature = signed_message.signature.hex()
        return signature

    @staticmethod
    async def message_func(session, user, semaphore):
        n = 0
        async with semaphore:  # Ограничение количества одновременных запросов
            get_url = f"{backend}accounts/wallet/get_message/"
            start_time = time.time()
            async with session.get(get_url) as get_response:
                get_response_json = await get_response.json()
                end_time = time.time()
                duration = end_time - start_time
                # print("GET", get_response.status, duration)
                user.message = get_response_json["message"]


    @staticmethod
    async def tokensAuthorization(session, user, semaphore, n):
        async with semaphore:  # Ограничение количества одновременных запросов

            signature = Users.signed(user.message, user.private_key)
            # Отправка POST запроса
            post_url = f"{backend}accounts/wallet/connect/"
            post_body = {
                "address": user.address,
                "message": user.message,
                "signed_msg": signature
            }

            start_time = time.time()
            async with session.post(post_url, json=post_body) as post_response:
                end_time = time.time()
                duration = end_time - start_time
                # print("POST", n, post_response.status, duration)

                response_text = await post_response.text()
                json_data = json.loads(response_text)
                access_token = json_data["token"]
                token = f'Token {access_token}'
                user.token = token
            return token

def init_users(count):
    i = 0
    all_users = []
    users_data = read_users_table()
    for user in users_data:
        i += 1
        # print(i)
        user_obj = Users(user)
        all_users.append(user_obj)
        if i == count:
            break
    return all_users




