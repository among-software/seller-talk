import json
import os, hashlib, hmac, base64, requests, time, math, datetime
from dotenv import load_dotenv
from services import naver_smart_store

load_dotenv()

BASE_URL = 'https://api.naver.com'
CUSTOMER_ID = os.getenv('CUSTOMER_ID')
API_KEY = os.getenv('AD_API_KEY')
SECRET_KEY = os.getenv('AD_API_SECRET')


def search_volume(start_date, end_date, keyword, one_ratio):

    all_ratio = naver_smart_store.get_shopping_keyword_trend(start_date, end_date, keyword)

    daily_list = []
    for i in all_ratio['ratio_list']:
        ratio_dict = {'x': i['period'], 'y': round(math.ceil(i['ratio'] * one_ratio / 10) * 10)}
        daily_list.append(ratio_dict)
    return json.dumps(daily_list, ensure_ascii=False)
