import os
import aiohttp as aiohttp
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv('NAVER_CLIENT_SECRET')


async def keyword_rank(keyword):
    open_api_url = f"https://search.shopping.naver.com/api/search/all?sort=rel&pagingIndex=1&pagingSize=40&viewType=list" \
                   f"&productSet=checkout&deliveryFee=&deliveryTypeValue=&frm=NVSHATC&" \
                   f"query={keyword}&origQuery={keyword}&iq=&eq=&xq="
    async with aiohttp.ClientSession() as client:
        async with client.get(open_api_url) as resp:
            response = await resp.json()
            counter = 0
            try:
                for i in response['shoppingResult']['products']:
                    if i['purchaseCnt'] <= 100:
                        counter += 1
                return counter
            except:
                return counter
