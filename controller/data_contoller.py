from services import naver_smart_store, search_volume, crawling


def data_controller(start_date, end_date, time_unit, category, keyword, device, gender, ages):
    search_volume_data = search_volume.search_volume(keyword)
    naver_smart_store_data = naver_smart_store.get_shopping_keyword_trend(start_date, end_date, time_unit,
                                                 category, keyword, device, gender, ages)
    crawling_data = crawling.crawling(keyword)
    return
