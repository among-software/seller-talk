import json
import os
import requests

# 환경변수 호출
from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv('NAVER_CLIENT_SECRET')


def get_total_product(keyword):
    open_api_url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=10"

    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret,
               "Content-Type": "application/json"}

    request = requests.get(open_api_url, headers=headers)

    response_code = request.status_code
    response_message = request.json()

    if response_code == 200:
        return response_message["total"]
    else:
        return str(response_code)
