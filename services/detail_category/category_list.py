import json
import requests
from collections import Counter


def crawling(keyword):

    url = f"https://search.shopping.naver.com/api/search/all?frm=NVSHCHK&origQuery={keyword}&pagingIndex=1&pagingSize=40&productSet=checkout&query={keyword}&sort=rel&timestamp=&viewType=list"
    r = requests.get(url)
    json_str = json.loads(json.dumps(r.json()))

    val1 = json_str['shoppingResult']["products"]
    category_id = json_str['mainFilters'][0]["filterValues"][0]["value"]
    total_product = json_str['shoppingResult']['orgQueryTotal']
    category_list = []

    for idx, val in enumerate(val1):
        category = val["category1Name"] + "," + val["category2Name"] + "," + val["category3Name"] + "," +\
                   val["category4Name"]
        category_list.append(category)

    counter = Counter(category_list)
    if len(counter) < 2:
        rel_category_one_percent = str("%.0f" % (100.0 * counter.most_common(n=2)[0][1] / 40.0) + '%')
        category_name_list1 = str(counter.most_common(n=2)[0][0]).split(',')
        crawling_data = {
            "category_id": category_id,
            "total_product": total_product,
            "categories": [{
                'title': category_name_list1,
                'percent': rel_category_one_percent
            }]
        }
    else:
        rel_category_one_percent = str("%.0f" % (100.0 * counter.most_common(n=2)[0][1] / 40.0) + '%')
        rel_category_two_percent = str("%.0f" % (100.0 * counter.most_common(n=2)[1][1] / 40.0) + '%')
        category_name_list1 = str(counter.most_common(n=2)[0][0]).split(',')
        category_name_list2 = str(counter.most_common(n=2)[1][0]).split(',')

        crawling_data = {
            "category_id": category_id,
            "total_product": total_product,
            "categories": [
                {
                    'title': category_name_list1,
                    'percent': rel_category_one_percent
                },
                {
                    'title': category_name_list2,
                    'percent': rel_category_two_percent
                }
            ]
        }

    return json.dumps(crawling_data, ensure_ascii=False)
