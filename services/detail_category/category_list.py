import json, os
import requests, random
from collections import Counter

from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv('NAVER_CLIENT_SECRET')


def crawling(keyword):

    open_api_url = f"https://openapi.naver.com/v1/search/shop.json?query={keyword}&display=80"

    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret,
               "Content-Type": "application/json"}

    request = requests.get(open_api_url, headers=headers)

    response_code = request.status_code
    response_message = request.json()
    category_list = []
    for i in response_message['items']:
        category = i['category1'] + ',' + i['category2'] + ',' + i['category3'] + ',' + i['category4']
        category_list.append(category)

    counter = Counter(category_list)
    if len(counter) < 2:
        rel_category_one_percent = str("%.0f" % (100.0 * counter.most_common(n=2)[0][1] / 80.0) + '%')
        category_name_list1 = str(counter.most_common(n=2)[0][0]).split(',')
        crawling_data = {
            "categories": [{
                'title': category_name_list1,
                'percent': rel_category_one_percent
            }]
        }
    else:
        rel_category_one_percent = str("%.0f" % (100.0 * counter.most_common(n=2)[0][1] / 80.0) + '%')
        rel_category_two_percent = str("%.0f" % (100.0 * counter.most_common(n=2)[1][1] / 80.0) + '%')
        category_name_list1 = str(counter.most_common(n=2)[0][0]).split(',')
        category_name_list2 = str(counter.most_common(n=2)[1][0]).split(',')

        crawling_data = {
            "categories": [
                {
                    'title': category_name_list1,
                    'percent': rel_category_one_percent
                },
                {
                    'title': category_name_list2,
                    'percent': rel_category_two_percent
                }
            ]
        }
    if response_code == 200:
        return json.dumps(crawling_data, ensure_ascii=False)
    else:
        return str(response_code)
