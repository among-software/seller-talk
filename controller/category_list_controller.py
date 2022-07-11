from services.detail_category import category_list


def category_list_controller(keyword):
    return category_list.crawling(keyword)
