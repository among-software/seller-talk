import json
import time
import asyncio

from services.contraction import search_volume
from services import total_product
from services.detail_category import category_list
from services.related import web_doc


async def get_detail(relation_keyword_stat, keyword, classification, volume, product, competitve):
    total_num, category, naver_classification = await asyncio.gather(
        total_product.get_total_product(relation_keyword_stat['relKeyword']),
        category_list.crawling(relation_keyword_stat['relKeyword']),
        web_doc.get_naver_web_doc(keyword)
    )
    category = json.loads(category)['categories'][0]

    pc_query_count = relation_keyword_stat['monthlyPcQcCnt']
    if pc_query_count == '< 10':
        pc_query_count = 9

    mo_query_count = relation_keyword_stat['monthlyMobileQcCnt']
    if mo_query_count == '< 10':
        mo_query_count = 9

    competitive_strength = round(total_num / (pc_query_count + mo_query_count), 2)
    total_query = pc_query_count + mo_query_count

    if classification == "전체":
        class_filter = ['쇼핑성', '정보성']
    else:
        class_filter = [classification]

    if not (naver_classification in class_filter):
        return

    if not (int(volume[0]) <= total_query <= int(volume[1])):
        return

    if not (int(product[0]) <= total_num <= int(product[1])):
        return

    if not (int(competitve[0]) <= competitive_strength <= int(competitve[1])):
        return

    return {
        'keyword': relation_keyword_stat['relKeyword'],
        'totalQuery': total_query,
        'items': total_num,
        'competition': competitive_strength,
        'category': category['title'][2],
        'classification': naver_classification
    }


async def task_gather(task_params):
    task_group = []
    for task in task_params:
        task_group.append(asyncio.ensure_future(get_detail(**task)))

    return await asyncio.gather(*task_group)


def controller(keyword, keyword_classification, keyword_volume, keyword_product, competitive_strength):
    search_volume_data = search_volume.search_volume(keyword)

    classification = keyword_classification
    volume = keyword_volume.split("~")
    product = keyword_product.split("~")
    competitve = competitive_strength.split("~")

    task_group = []
    response = []

    loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    for relation_keyword_stat in search_volume_data['keywordList'][0:20]:
        task_group.append({
            "relation_keyword_stat": relation_keyword_stat,
            "keyword": keyword,
            "classification": classification,
            "volume": volume,
            "product": product,
            "competitve": competitve
        })

        if len(task_group) == 3:
            response += loop.run_until_complete(task_gather(task_group))
            task_group = []
            time.sleep(1)

    loop.close()
    response = [x for x in response if x is not None]
    return response
