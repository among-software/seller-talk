import json

from services.contraction import search_volume
from services import total_product
from services.detail_category import category_list
from services.related import web_doc


# related_contoller
def controller(keyword, keyword_classifiction, keyword_volume, keyword_product, competitive_strength):
    search_volume_data = search_volume.search_volume(keyword)
    classification = keyword_classifiction
    volume = keyword_volume.split("~")
    product = keyword_product.split("~")
    competitve = competitive_strength.split("~")
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
        total_query = pc_query_count + mo_query_count
        category = json.loads(category_list.crawling(relation_keyword_stat['relKeyword']))['categories'][0]
        if classification == "전체":
            if int(volume[0]) <= total_query <= int(volume[1]) and int(product[0]) <= total_num <= int(product[1]) and int(competitve[0]) <= competitive_strength <= int(competitve[1]):
                response.append({
                    'keyword': relation_keyword_stat['relKeyword'],
                    'totalQuery': total_query,
                    'items': total_num,
                    'competition': competitive_strength,
                    'category': category['title'][-1],
                    'classification': web_doc.get_naver_web_doc(keyword)
                })

        elif classification == "쇼핑성":
            if web_doc.get_naver_web_doc(keyword) == '쇼핑성' and int(volume[0]) <= total_query <= int(volume[1]) and int(product[0]) <= total_num <= int(product[1]) and int(competitve[0]) <= competitive_strength <= int(competitve[1]):
                response.append({
                    'keyword': relation_keyword_stat['relKeyword'],
                    'totalQuery': total_query,
                    'items': total_num,
                    'competition': competitive_strength,
                    'category': category['title'][-1],
                    'classification': web_doc.get_naver_web_doc(keyword)
                })

        elif classification == "정보성":
            if web_doc.get_naver_web_doc(keyword) == '정보성' and int(volume[0]) <= total_query <= int(volume[1]) and int(product[0]) <= total_num <= int(product[1]) and int(competitve[0]) <= competitive_strength <= int(competitve[1]):
                response.append({
                    'keyword': relation_keyword_stat['relKeyword'],
                    'totalQuery': total_query,
                    'items': total_num,
                    'competition': competitive_strength,
                    'category': category['title'][-1],
                    'classification': web_doc.get_naver_web_doc(keyword)
                })

    return json.dumps(response, ensure_ascii=False)
