import json
import os
import requests

# 환경변수 호출
from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv('NAVER_CLIENT_SECRET')


async def get_total_product(client, keyword):
    open_api_url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=10"

    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret,
               "Content-Type": "application/json"}

    async with client.get(open_api_url, headers=headers) as resp:
        return await resp.json()["total"]
