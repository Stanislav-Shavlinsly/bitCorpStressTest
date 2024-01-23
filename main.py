import sys
from Classes.users_manage import *
import asyncio
import aiohttp

async def login(n):
    print('hello bitcorp')
    all_users = init_users(n)
    semaphore = asyncio.Semaphore(n)

    async with aiohttp.ClientSession() as session:
        message_tasks = [Users.message_func(session, user, semaphore) for user in all_users]
        await asyncio.gather(*message_tasks)

        authorization_tasks = [Users.tokensAuthorization(session, user, semaphore, n) for n, user in enumerate(all_users)]
        await asyncio.gather(*authorization_tasks)
    return all_users

async def post_request(session, user, body, url):
        post_url = f"{backend}{url}"
        post_body = body
        headers = {'Authorization': f'Token {user.token}'}
        start_time = time.time()
        async with session.post(post_url, json=post_body, headers=headers) as post_response:
            end_time = time.time()
            result = end_time - start_time
            # print("POST", n, post_response.status, result)
            return result

async def request_async(all_users):
    # semaphore = asyncio.Semaphore(n)

    async with aiohttp.ClientSession() as session:
        durations = await asyncio.gather(*[post_request(session, user, body, url) for n, user in enumerate(all_users)])
    return durations
'url: crowdsale/refund/   body: {"chain_id": 0}'




if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    all_users = asyncio.run(login(800))
    # for user in all_users:
    #     print(user.id, user.address, user.token)

    while True:
        url = input('url: ')
        body = input('body: ')

        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        durations = asyncio.run(request_async(all_users))

        print(sum(durations) / 800)



