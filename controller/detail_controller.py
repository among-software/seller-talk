from services.detail import naver_smart_store, daily_search, basic_ratio
import json, asyncio
from services import keyword_rank


async def rank(keyword):
    keyword = await keyword_rank.keyword_rank(keyword)
    return keyword


def detail_controller(start_date, end_date, keyword):
    one_day_search = basic_ratio.search_volume(keyword)
    daily = daily_search.search_volume(start_date, end_date, keyword, one_day_search)
    keyword_rank_data = asyncio.run(rank(keyword))

    try:
        sex = naver_smart_store.get_shopping_keyword_trend_by_gender(start_date, end_date, keyword)
        device = naver_smart_store.get_shopping_keyword_trend_by_device(start_date, end_date, keyword)
        ages = naver_smart_store.get_shopping_keyword_trend_by_age(start_date, end_date, keyword)

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
                "10대": ages['10대'],
                "20대": ages['20대'],
                "30대": ages['30대'],
                "40대": ages['40대'],
                "50대": ages['50대'],
                "60대": ages['60대']
            },
            'rank': keyword_rank_data
        }
    except:
        data_dict = {
            'data': daily,
            'sex': {
                "male": None,
                "female": None
            },
            'device': {
                "pc": None,
                "mobile": None
            },
            'ages': {
                "10대": None,
                "20대": None,
                "30대": None,
                "40대": None,
                "50대": None,
                "60대": None
            },
            'rank': keyword_rank_data
        }

    return json.dumps(data_dict, ensure_ascii=False)
