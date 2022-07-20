import os
import aiohttp as aiohttp

from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv('NAVER_CLIENT_SECRET')


async def get_total_product(keyword):
    open_api_url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=10"

    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret,
               "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as client:
        async with client.get(open_api_url, headers=headers) as resp:
            response = await resp.json()
            print(response)
            return response["total"]
