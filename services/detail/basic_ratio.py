import json
import os, hashlib, hmac, base64, requests, time, math, datetime, dateutil.relativedelta
import random

from dotenv import load_dotenv
from services import naver_smart_store

load_dotenv()

BASE_URL = 'https://api.naver.com'
CUSTOMER_ID = os.getenv('CUSTOMER_ID')
API_KEY = os.getenv('AD_API_KEY')
SECRET_KEY = os.getenv('AD_API_SECRET')


def search_volume(keyword):

    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
    #     hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)
        hash = hmac.new(secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())

    def get_header(method, uri, api_key, secret_key, customer_id):
        timestamp = str(int(time.time() * 1000))
        signature = generate(timestamp, method, uri, SECRET_KEY)
        return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

    def call_RelKwdStat(_kwds_string):
        dic_return_kwd = {}
        uri = '/keywordstool'
        method = 'GET'
        prm = {'hintKeywords': _kwds_string, 'showDetail': 1}

        # ManageCustomerLink Usage Sample
        r = requests.get(BASE_URL + uri, params=prm, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
        r_data = r.json()

        return r_data

    kwd_list = [keyword]
    kwds_string = ','.join(kwd_list)
    return_data = call_RelKwdStat(kwds_string)
    now = datetime.datetime.now().replace(second=0, microsecond=0)
    now = now.date()
    current_date = now + dateutil.relativedelta.relativedelta(days=-1, second=0, microsecond=0)
    current_date = current_date.date()
    previous_now = now + dateutil.relativedelta.relativedelta(months=-1, days=-1, second=0, microsecond=0)
    previous_now = previous_now.date()

    all_ratio = naver_smart_store.get_shopping_keyword_trend(start_date=previous_now, end_date=current_date, keyword=keyword)

    total_product = 0
    for i in return_data['keywordList'][0:1]:
        if i['monthlyPcQcCnt'] == '< 10':
            i['monthlyPcQcCnt'] = random.randrange(0, 9)
        if i['monthlyMobileQcCnt'] == '< 10':
            i['monthlyMobileQcCnt'] = random.randrange(0, 9)
        total = i['monthlyMobileQcCnt'] + i['monthlyPcQcCnt']
        total_product += total

    if all_ratio['ratio_sum'] == 0:
        all_ratio['ratio_sum'] = 1
    if len(all_ratio['ratio_list']) == 0:
        all_ratio['ratio_list'].append({'ratio': 1})
    daily = total_product / all_ratio['ratio_sum']
    basic_ratio = all_ratio['ratio_list'][0]['ratio']
    one_day_search = basic_ratio * daily
    one_ratio = one_day_search / basic_ratio
    return one_ratio
