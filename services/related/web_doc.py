# 환경변수 호출
import requests, os
from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv('NAVER_CLIENT_SECRET')


def get_naver_web_doc(keyword):

    open_api_url = f"https://openapi.naver.com/v1/search/webkr.json?query={keyword}"
    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret,
               "Content-Type": "application/json"}
    request = requests.get(open_api_url, headers=headers)

    response_code = request.status_code
    response_message = request.json()

    if response_code == 200:
        return response_message
    else:
        print("Error Code : " + str(response_code))
        return str(response_code)