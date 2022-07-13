import json

from services.contraction import search_volume
from services import total_product
from services.detail_category import category_list


def controller(keyword):
    search_volume_data = search_volume.search_volume(keyword)
    response = []

    for relation_keyword_stat in search_volume_data['keywordList'][0:3]:
        pc_query_count = relation_keyword_stat['monthlyPcQcCnt']
        if pc_query_count == '< 10':
            pc_query_count = 9
        mo_query_count = relation_keyword_stat['monthlyMobileQcCnt']
        if mo_query_count == '< 10':
            mo_query_count = 9
        total_num = total_product.get_total_product(keyword)
        competitive_strength = round(total_num / (pc_query_count + mo_query_count), 2)
        response.append({
            'keyword': relation_keyword_stat['relKeyword'],
            'pc': pc_query_count,
            'mobile': mo_query_count,
            'items': total_num,
            'competition': competitive_strength,
            'category': category_list.crawling(relation_keyword_stat['relKeyword']),
            'classification': '쇼핑성'
        })

    return json.dumps(response, ensure_ascii=False)