import json
import time
import asyncio

from services.contraction import search_volume
from services import total_product
from services.detail_category import category_list
from services.related import web_doc, ad_cost


async def get_detail(relation_keyword_stat, keyword, classification, total_query, items, competitve):
    total_num, category, naver_classification, ad_cost_info = await asyncio.gather(
        total_product.get_total_product(relation_keyword_stat['relKeyword']),
        category_list.crawling(relation_keyword_stat['relKeyword']),
        web_doc.get_naver_web_doc(keyword),
        ad_cost.search_volume(relation_keyword_stat['relKeyword']),
    )
    category = json.loads(category)['categories'][0]

    pc_query_count = relation_keyword_stat['monthlyPcQcCnt']
    if pc_query_count == '< 10':
        pc_query_count = 9

    mo_query_count = relation_keyword_stat['monthlyMobileQcCnt']
    if mo_query_count == '< 10':
        mo_query_count = 9

    pc_ad_click_percentage = relation_keyword_stat['monthlyAvePcCtr']
    mo_ad_click_percentage = relation_keyword_stat['monthlyAveMobileCtr']

    pc_ad_click_count = relation_keyword_stat['monthlyAvePcClkCnt']
    mo_ad_click_count = relation_keyword_stat['monthlyAveMobileClkCnt']

    ad_click_count_average = round((pc_ad_click_count + mo_ad_click_count) / 2, 2)
    if ad_click_count_average == 0:
        ad_click_count_average = 1

    competitive_strength = round(total_num / (pc_query_count + mo_query_count), 2)
    total_query_count = pc_query_count + mo_query_count
    ad_click_competition = round(total_num / ad_click_count_average, 2)
    click_to_click_ad = round(ad_cost_info['average'] / ad_click_count_average, 2)

    if classification == "전체":
        class_filter = ['쇼핑성', '정보성']
    else:
        class_filter = [classification]

    if not (naver_classification in class_filter):
        return

    if not (int(total_query[0]) <= total_query_count <= int(total_query[1])):
        return

    if not (int(items[0]) <= total_num <= int(items[1])):
        return

    if not (int(competitve[0]) <= competitive_strength <= int(competitve[1])):
        return

    return {
        'keyword': relation_keyword_stat['relKeyword'],
        'totalQuery': total_query_count,
        'items': total_num,
        'competition': competitive_strength,
        'category': category['title'][2],
        'classification': naver_classification,
        'pc_ad_cost': ad_cost_info['pc_ad_cost'],
        'mo_ad_cost': ad_cost_info['mo_ad_cost'],
        'pc_ad_click_percentage': pc_ad_click_percentage,
        'mo_ad_click_percentage': mo_ad_click_percentage,
        'average_ad_click_percentage': ad_click_count_average,
        'ad_click_competition': ad_click_competition,
        'click_to_click_ad': click_to_click_ad
    }


async def task_gather(task_params):
    task_group = []
    for task in task_params:
        task_group.append(asyncio.ensure_future(get_detail(**task)))

    return await asyncio.gather(*task_group)


def controller(keyword, keyword_classification, keyword_total_query, keyword_items, competitive_strength, list_index):
    search_volume_data = search_volume.search_volume(keyword)

    classification = keyword_classification
    total_query = keyword_total_query.split("~")
    items = keyword_items.split("~")
    competitve = competitive_strength.split("~")
    list_index = list_index.split("~")

    task_group = []
    response = []

    loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    for relation_keyword_stat in search_volume_data['keywordList'][int(list_index[0]):int(list_index[1])]:
        task_group.append({
            "relation_keyword_stat": relation_keyword_stat,
            "keyword": keyword,
            "classification": classification,
            "total_query": total_query,
            "items": items,
            "competitve": competitve
        })

        if len(task_group) == 5:
            response += loop.run_until_complete(task_gather(task_group))
            task_group = []

    loop.close()
    response = [x for x in response if x is not None]
    return response

