import os, hashlib, hmac, base64, requests, time, json
import aiohttp as aiohttp
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://api.naver.com'
CUSTOMER_ID = os.getenv('CUSTOMER_ID')
API_KEY = os.getenv('AD_API_KEY')
SECRET_KEY = os.getenv('AD_API_SECRET')


async def search_volume(keyword):

    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())

    def get_header(method, uri, api_key, secret_key, customer_id):
        timestamp = str(int(time.time() * 1000))
        signature = generate(timestamp, method, uri, SECRET_KEY)
        return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

    def call_ad_pc_day_cost(_kwds_string):
        uri = '/estimate/exposure-minimum-bid/keyword'
        method = 'POST'
        prm = {"device": "PC", "period": "DAY", "items": [_kwds_string]}

        # ManageCustomerLink Usage Sample
        r = requests.post(BASE_URL + uri, data=json.dumps(prm), headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
        r_data = r.json()

        return r_data

    def call_ad_mo_day_cost(_kwds_string):
        uri = '/estimate/exposure-minimum-bid/keyword'
        method = 'POST'
        prm = {"device": "MOBILE", "period": "DAY", "items": [_kwds_string]}

        # ManageCustomerLink Usage Sample
        r = requests.post(BASE_URL + uri, data=json.dumps(prm), headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
        r_data = r.json()

        return r_data

    pc_ad_month_cost = call_ad_pc_day_cost(keyword)
    mo_ad_month_cost = call_ad_mo_day_cost(keyword)

    average = (pc_ad_month_cost['estimate'][0]["bid"] + mo_ad_month_cost['estimate'][0]["bid"]) / 2
    return {'average': average, "pc_ad_cost": pc_ad_month_cost['estimate'][0]["bid"], "mo_ad_cost": mo_ad_month_cost['estimate'][0]["bid"]}
