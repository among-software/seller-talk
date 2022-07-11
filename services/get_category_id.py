import json
import requests, random


def get_category_id(keyword):

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
    category_id = json_str['mainFilters'][0]["filterValues"][0]["value"]

    return category_id

