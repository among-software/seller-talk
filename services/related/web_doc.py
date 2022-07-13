# 환경변수 호출
import requests, os
from bs4 import BeautifulSoup


def get_naver_web_doc(keyword):
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&"

    request = requests.get(url, params={'query': keyword})

    response_code = request.status_code
    response_html = request.text
    keyword_order = response_html
    if response_code == 200:
        return str(response_html)
    else:
        print("Error Code : " + str(response_code))
        return str(response_code)