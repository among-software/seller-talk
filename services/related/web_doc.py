# 환경변수 호출
import requests, os
from bs4 import BeautifulSoup


def get_naver_web_doc(keyword):
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&"

    request = requests.get(url, params={'query': keyword})

    response_code = request.status_code
    response_html = request.text
    keyword_order = BeautifulSoup(response_html, 'html.parser')
    menu_order = keyword_order.select_one('div#wrap > div#header_wrap > div.api_floating_header > div#lnb > div.lnb_group > div.lnb_menu > ul')
    section_order = keyword_order.select_one('div#wrap > div#container > div#content > div#main_pack')
    li_list = [li for li in menu_order.findAll('li')]
    section_list = [section for section in section_order.findAll('section')]
    tab_order = 1
    for i in li_list:
        if i.select_one('a').get_text() == '쇼핑':
            break
        else:
            tab_order += 1
    section_order = 1
    for i in section_list:
        if 'sp_nshop' in i['class']:
            break
        else:
            section_order += 1

    return_text = ''
    if section_order <= 2:
        return_text = '쇼핑성'
    elif section_order <= 3 and tab_order <= 3:
        return_text = '쇼핑성'
    else:
        return_text = '정보성'
    if response_code == 200:
        return return_text
    else:
        print("Error Code : " + str(response_code))
        return str(response_code)