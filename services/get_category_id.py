import json, os
import requests, random

# 환경변수 호출
from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv('NAVER_CLIENT_SECRET')


# url = f"https://search.shopping.naver.com/api/search/all?frm=NVSHCHK&origQuery={keyword}&pagingIndex=1&pagingSize=80&productSet=checkout&query={keyword}&sort=rel&timestamp=&viewType=list"
# user_agent_list = [
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
# ]
# user_agent = random.choice(user_agent_list)
# headers = {'User-Agent': user_agent}
# r = requests.get(url, headers=headers)
# json_str = json.loads(json.dumps(r.json()))
# category_id = json_str['mainFilters'][0]["filterValues"][0]["value"]
# print(category_id)
# return category_id

def get_category_id(keyword):

    category_dict = {
        '장마준비': 100008831,
        '여성패션': 50000167,
        '남성패션': 50000169,
        '액세서리': 50000181,
        '화장품/미용': 50000002,
        '가구/인테리어': 50000004,
        '식품': 50000006,
        '출산/유아동': 50000005,
        '출산/육아': 50000005,
        '반려동물용품': 50000155,
        '생활/주방용품': 50000078,
        '가전': 50000210,
        '디지털/가전': 50000003,
        '컴퓨터': 50000151,
        '스포츠/레저': 50000007,
        '건강/의료용품': 50000064,
        '자동차/공구': 50000055,
        '취미/문구/악기': 50000158,
        '정기구독': 50000006,
        '여행': 50007256,
        'E쿠폰/티켓': 50000009,
        '렌탈관': 50000003,
        '리퍼비시관': 50000004,
        '면세점': 50000010,
        '패션잡화': 50000001,
        '패션의류': 50000000,
        '생활/건강': 50000008,
        '여가/생활편의': 50000009,
        '도서': 50005542
    }
    open_api_url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=10"

    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret,
               "Content-Type": "application/json"}

    request = requests.get(open_api_url, headers=headers)

    response_code = request.status_code
    response_message = request.json()
    category_id = category_dict[response_message['items'][0]['category1']]
    if response_code == 200:
        return str(category_id)
    else:
        return str(response_code)

