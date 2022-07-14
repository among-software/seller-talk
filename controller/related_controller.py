import json
import time

import aiohttp as aiohttp

from services.contraction import search_volume
from services import total_product
from services.detail_category import category_list
from services.related import web_doc
import asyncio


async def test(client, relation_keyword_stat, keyword, classification, volume, product, competitve):
    pc_query_count = relation_keyword_stat['monthlyPcQcCnt']
    if pc_query_count == '< 10':
        pc_query_count = 9
    mo_query_count = relation_keyword_stat['monthlyMobileQcCnt']
    if mo_query_count == '< 10':
        mo_query_count = 9
    total_num = await total_product.get_total_product(client, relation_keyword_stat['relKeyword'])
    category = json.loads(await category_list.crawling(client, relation_keyword_stat['relKeyword']))['categories'][0]
    naver_classification = await web_doc.get_naver_web_doc(client, keyword)

    competitive_strength = round(total_num / (pc_query_count + mo_query_count), 2)
    total_query = pc_query_count + mo_query_count
    print(time.time())
    if classification == "전체":
        print('전체')
        if int(volume[0]) <= total_query <= int(volume[1]) and int(product[0]) <= total_num <= int(
                product[1]) and int(competitve[0]) <= competitive_strength <= int(competitve[1]):
            return {
                'keyword': relation_keyword_stat['relKeyword'],
                'totalQuery': total_query,
                'items': total_num,
                'competition': competitive_strength,
                'category': category['title'][-1],
                'classification': naver_classification
            }

    elif classification == "쇼핑성":
        if naver_classification == '쇼핑성' and int(volume[0]) <= total_query <= int(volume[1]) and int(
                product[0]) <= total_num <= int(product[1]) and int(competitve[0]) <= competitive_strength <= int(
            competitve[1]):
            return {
                'keyword': relation_keyword_stat['relKeyword'],
                'totalQuery': total_query,
                'items': total_num,
                'competition': competitive_strength,
                'category': category['title'][-1],
                'classification': naver_classification
            }

    elif classification == "정보성":
        if naver_classification == '정보성' and int(volume[0]) <= total_query <= int(volume[1]) and int(
                product[0]) <= total_num <= int(product[1]) and int(competitve[0]) <= competitive_strength <= int(
            competitve[1]):
            return {
                'keyword': relation_keyword_stat['relKeyword'],
                'totalQuery': total_query,
                'items': total_num,
                'competition': competitive_strength,
                'category': category['title'][-1],
                'classification': naver_classification
            }


# related_contoller
async def controller(keyword, keyword_classification, keyword_volume, keyword_product, competitive_strength):
    search_volume_data = search_volume.search_volume(keyword)

    classification = keyword_classification
    volume = keyword_volume.split("~")
    product = keyword_product.split("~")
    competitve = competitive_strength.split("~")

    response = []

    async with aiohttp.ClientSession() as client:
        for relation_keyword_stat in search_volume_data['keywordList'][0:20]:
            response.append(
                asyncio.ensure_future(test(client, relation_keyword_stat, keyword, classification, volume, product, competitve)))

    response = await asyncio.gather(*response)

    return response
