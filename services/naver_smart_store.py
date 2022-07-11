# import json
# import os
# import requests
#
# # 환경변수 호출
# from dotenv import load_dotenv
# import crawling
# load_dotenv()
#
# client_id = os.getenv('NAVER_CLIENT_ID')
# client_secret = os.getenv('NAVER_CLIENT_SECRET')
#
#
# def get_shopping_keyword_trend(start_date, end_date, time_unit, keyword):
#     open_api_url = "https://openapi.naver.com/v1/datalab/search"
#     payload = {'startDate': str(start_date),
#                'endDate': str(end_date),
#                'time_unit': str(time_unit),
#                'category': crawling(keyword)["category_id"],
#                'keyword': str(keyword), 'device': "pc, mo",
#                'gender': "m, f",
#                'ages': ["10", "20", "30", "40", "50", "60"]}
#     headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret,
#                "Content-Type": "application/json"}
#
#     request = requests.post(open_api_url, data=json.dumps(payload), headers=headers)
#
#     response_code = request.status_code
#     response_message = request.text
#
#     if response_code == 200:
#         print(response_message)
#         return response_message
#     else:
#         print("Error Code : " + str(response_code))
#         return str(response_code)
