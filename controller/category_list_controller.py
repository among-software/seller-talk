from services.detail_category import category_list
import asyncio, json


async def get_detail(keyword):
    category = await category_list.crawling(keyword)
    return {
        'category': json.loads(category)['categories']
    }


def category_list_controller(keyword):

    return json.dumps(asyncio.run(get_detail(keyword)), ensure_ascii=False)
