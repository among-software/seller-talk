import os, hashlib, hmac, base64, requests, time
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://api.naver.com'
CUSTOMER_ID = os.getenv('CUSTOMER_ID')
API_KEY = os.getenv('AD_API_KEY')
SECRET_KEY = os.getenv('AD_API_SECRET')

# naver ads ap
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

    return return_data