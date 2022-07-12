import json
import os, hashlib, hmac, base64, requests, time, math, collections
from dotenv import load_dotenv
from services import naver_smart_store
from datetime import datetime, timedelta

load_dotenv()

BASE_URL = 'https://api.naver.com'
CUSTOMER_ID = os.getenv('CUSTOMER_ID')
API_KEY = os.getenv('AD_API_KEY')
SECRET_KEY = os.getenv('AD_API_SECRET')


def search_volume(start_date, end_date, keyword, one_ratio):
    all_ratio = naver_smart_store.get_shopping_keyword_trend(start_date, end_date, keyword)

    daily_list = []

    first_search = datetime.strptime(start_date, "%Y-%m-%d")
    first_search = first_search.date()
    end_date_search = datetime.strptime(end_date, "%Y-%m-%d")
    start_date_search = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_search = end_date_search.date()
    start_date_search = start_date_search.date()
    date_diff = end_date_search - start_date_search

    for i in all_ratio['ratio_list']:
        ratio_dict = {'x': i['period'], 'y': math.ceil(i['ratio'] * one_ratio / 10) * 10}
        daily_list.append(ratio_dict)

    if len(daily_list) < date_diff.days:
        for j in range(date_diff.days + 1):
            if not daily_list:
                daily_list.insert(j, {'x': str(first_search), 'y': 0})
                first_search = first_search + timedelta(days=1)
            if daily_list:
                if daily_list[j]['x'] == str(first_search):
                    first_search = first_search + timedelta(days=1)
                else:
                    daily_list.append({'x': str(first_search), 'y': 0})
                    first_search = first_search + timedelta(days=1)

    sorted_list = sorted(daily_list, key=(lambda x: x['x']))
    for values in sorted_list:
        print(values)
    return json.dumps(sorted_list, ensure_ascii=False)

