import json, asyncio

from services.contraction import search_volume
from services import total_product


async def get_total(keyword):
    total_num = await total_product.get_total_product(keyword)
    return total_num


def data_controller(keyword):
    search_volume_data = search_volume.search_volume(keyword)
    single_data = {}
    # search_list = []

    for i in search_volume_data['keywordList'][0:1]:
        pc_query_count = i['monthlyPcQcCnt']
        if pc_query_count == '< 10':
            pc_query_count = 9
        mo_query_count = i['monthlyMobileQcCnt']
        if mo_query_count == '< 10':
            mo_query_count = 9
        competitive_strength_str = i['compIdx']
        total_num = asyncio.run(get_total(keyword))
        competitive_strength = round(total_num / (pc_query_count + mo_query_count), 2)
        single_data = {
            'keyword': i['relKeyword'],
            'pc': pc_query_count,
            'mobile': mo_query_count,
            'items': total_num,
            'competition': competitive_strength,
            # 'competitiveStrengthStr': competitive_strength_str
        }
        # 연관검색어 요청시 살리기
        # search_list.append(single_data)

    return json.dumps(single_data, ensure_ascii=False)
