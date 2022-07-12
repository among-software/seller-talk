import json
import os
import requests
from services import get_category_id

# 환경변수 호출
from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv('NAVER_CLIENT_SECRET')


def get_shopping_keyword_trend(start_date, end_date, keyword):
    open_api_url = "https://openapi.naver.com/v1/datalab/search"
    payload = {'startDate': str(start_date),
               'endDate': str(end_date),
               'timeUnit': 'date',
               'keywordGroups': [{'groupName': str(keyword), 'keywords': [str(keyword)]}],
               'device': "",
               'gender': "",
               'ages': []}
    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret,
               "Content-Type": "application/json"}

    request = requests.post(open_api_url, data=json.dumps(payload), headers=headers)

    response_code = request.status_code
    response_message = request.json()
    ratio_sum = 0
    ratio_list = []
    for i in response_message['results'][0]['data']:
        ratio_sum += i['ratio']
        ratio_list.append(i)
    if response_code == 200:
        return {"ratio_sum": ratio_sum, "ratio_list": ratio_list}
    else:
        print("Error Code : " + str(response_code))
        return str(response_code)


def get_shopping_keyword_trend_by_gender(start_date, end_date, keyword):
    open_api_url = "https://openapi.naver.com/v1/datalab/shopping/category/keyword/gender"
    payload = {'startDate': str(start_date),
               'endDate': str(end_date),
               'timeUnit': 'date',
               'category': str(get_category_id.get_category_id(keyword)),
               'keyword': str(keyword),
               'device': "",
               'gender': "",
               'ages': []}
    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret,
               "Content-Type": "application/json"}

    request = requests.post(open_api_url, data=json.dumps(payload), headers=headers)

    response_code = request.status_code
    response_message = request.json()
    male_sum = 0
    female_sum = 0
    for i in response_message['results'][0]['data']:
        if i['group'] == 'm':
            male_sum += i['ratio']
        if i['group'] == 'f':
            female_sum += i['ratio']

    average = male_sum + female_sum
    if male_sum > 0:
        male_average = round((male_sum / average) * 100)
    else:
        male_average = 0
    if female_sum > 0:
        female_average = round((female_sum / average) * 100)
    else:
        female_average = 0

    if response_code == 200:
        return {"male": male_average, "female": female_average}
    else:
        print("Error Code : " + str(response_code))
        return str(response_code)


def get_shopping_keyword_trend_by_device(start_date, end_date, keyword):
    open_api_url = "https://openapi.naver.com/v1/datalab/shopping/category/keyword/device"
    payload = {'startDate': str(start_date),
               'endDate': str(end_date),
               'timeUnit': 'date',
               'category': str(get_category_id.get_category_id(keyword)),
               'keyword': str(keyword),
               'device': "",
               'gender': "",
               'ages': []}
    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret,
               "Content-Type": "application/json"}

    request = requests.post(open_api_url, data=json.dumps(payload), headers=headers)

    response_code = request.status_code
    response_message = request.json()

    pc_sum = 0
    mobile_sum = 0
    for i in response_message['results'][0]['data']:
        if i['group'] == 'pc':
            pc_sum += i['ratio']
        else:
            mobile_sum += i['ratio']
    average = pc_sum + mobile_sum
    if pc_sum > 0:
        pc_average = round(pc_sum / average * 100)
    else:
        pc_average = 0
    if mobile_sum > 0:
        mobile_average = round(mobile_sum / average * 100)
    else:
        mobile_average = 0

    if response_code == 200:
        return {"pc": pc_average, "mobile": mobile_average}
    else:
        print("Error Code : " + str(response_code))
        return str(response_code)


def get_shopping_keyword_trend_by_age(start_date, end_date, keyword):
    open_api_url = "https://openapi.naver.com/v1/datalab/shopping/category/keyword/age"
    payload = {'startDate': str(start_date),
               'endDate': str(end_date),
               'timeUnit': 'date',
               'category': str(get_category_id.get_category_id(keyword)),
               'keyword': str(keyword),
               'device': "",
               'gender': "",
               'ages': ["10", "20", "30", "40", "50", "60"]}
    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret,
               "Content-Type": "application/json"}

    request = requests.post(open_api_url, data=json.dumps(payload), headers=headers)

    response_code = request.status_code
    response_message = request.json()

    teen_sum = 0
    twenty_sum = 0
    thirty_sum = 0
    forty_sum = 0
    fifty_sum = 0
    sixty_sum = 0
    for i in response_message['results'][0]['data']:
        if i['group'] == '10':
            teen_sum += i['ratio']
        if i['group'] == '20':
            twenty_sum += i['ratio']
        if i['group'] == '30':
            thirty_sum += i['ratio']
        if i['group'] == '40':
            forty_sum += i['ratio']
        if i['group'] == '50':
            fifty_sum += i['ratio']
        if i['group'] == '60':
            sixty_sum += i['ratio']
    average = teen_sum + twenty_sum + thirty_sum + forty_sum + fifty_sum + sixty_sum

    if teen_sum > 0:
        teen_average = round(teen_sum / average * 100)
    else:
        teen_average = 0
    if twenty_sum > 0:
        twenty_average = round(twenty_sum / average * 100)
    else:
        twenty_average = 0
    if thirty_sum > 0:
        thirty_average = round(thirty_sum / average * 100)
    else:
        thirty_average = 0
    if forty_sum > 0:
        forty_average = round(forty_sum / average * 100)
    else:
        forty_average = 0
    if fifty_sum > 0:
        fifty_average = round(fifty_sum / average * 100)
    else:
        fifty_average = 0
    if sixty_sum > 0:
        sixty_average = round(sixty_sum / average * 100)
    else:
        sixty_average = 0

    if response_code == 200:
        return {"10대": teen_average, "20대": twenty_average, "30대": thirty_average,
                "40대": forty_average, "50대": fifty_average, "60대": sixty_average}
    else:
        print("Error Code : " + str(response_code))
        return str(response_code)
