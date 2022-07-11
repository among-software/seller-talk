import json
import requests, random
from collections import Counter


def crawling(keyword):

    url = f"https://search.shopping.naver.com/api/search/all?frm=NVSHCHK&origQuery={keyword}&pagingIndex=1&pagingSize=80&productSet=checkout&query={keyword}&sort=rel&timestamp=&viewType=list"
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    r = requests.get(url, headers=headers)
    json_str = json.loads(json.dumps(r.json()))

    val1 = json_str['shoppingResult']["products"]
    category_list = []

    for idx, val in enumerate(val1):
        category = val["category1Name"] + "," + val["category2Name"] + "," + val["category3Name"] + "," +\
                   val["category4Name"]
        category_list.append(category)

    counter = Counter(category_list)
    if len(counter) < 2:
        rel_category_one_percent = str("%.0f" % (100.0 * counter.most_common(n=2)[0][1] / 80.0) + '%')
        category_name_list1 = str(counter.most_common(n=2)[0][0]).split(',')
        crawling_data = {
            "categories": [{
                'title': category_name_list1,
                'percent': rel_category_one_percent
            }]
        }
    else:
        rel_category_one_percent = str("%.0f" % (100.0 * counter.most_common(n=2)[0][1] / 80.0) + '%')
        rel_category_two_percent = str("%.0f" % (100.0 * counter.most_common(n=2)[1][1] / 80.0) + '%')
        category_name_list1 = str(counter.most_common(n=2)[0][0]).split(',')
        category_name_list2 = str(counter.most_common(n=2)[1][0]).split(',')

        crawling_data = {
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
