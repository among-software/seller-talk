from services.detail import naver_smart_store, daily_search, basic_ratio
import json


def detail_controller(start_date, end_date, keyword):
    sex = naver_smart_store.get_shopping_keyword_trend_by_gender(start_date, end_date, keyword)
    device = naver_smart_store.get_shopping_keyword_trend_by_device(start_date, end_date, keyword)
    ages = naver_smart_store.get_shopping_keyword_trend_by_age(start_date, end_date, keyword)
    one_day_search = basic_ratio.search_volume(keyword)
    daily = daily_search.search_volume(start_date, end_date, keyword, one_day_search)
    data_dict = {
        'data': daily,
        'sex': {
            "male": sex['male'],
            "female": sex['female']
        },
        'device': {
            "pc": device['pc'],
            "mobile": device['mobile']
        },
        'ages': {
            "10": ages['10'],
            "20": ages['20'],
            "30": ages['30'],
            "40": ages['40'],
            "50": ages['50'],
            "60": ages['60']
        }
    }
    return json.dumps(data_dict, ensure_ascii=False)
