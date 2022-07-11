import json

from services.contraction import search_volume, total_product


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
        total_num = total_product.get_total_product(keyword)
        competitive_strength = total_num / pc_query_count + mo_query_count
        single_data = {
            'keyword': i['relKeyword'],
            'pcQuery': pc_query_count,
            'moQuery': mo_query_count,
            'totalproduct': competitive_strength,
            'competitiveStrengthStr': competitive_strength_str
        }
        # 연관검색어 요청시 살리기
        # search_list.append(single_data)

    return json.dumps(single_data, ensure_ascii=False)
