from flask import Flask, request, jsonify
from services import naver_smart_store, search_volume, crawling
from controller import simple_data_controller
app = Flask(__name__)


@app.route("/api/simple-data/", methods=['GET'])
def return_simple_data():
    # return get_shopping_keyword_trend(start_date=request.args.get('start-date'),
    #                                   end_date=request.args.get('end-date'),
    #                                   time_unit=request.args.get('time-unit'),
    #                                   category=request.args.get('category'),
    #                                   keyword=request.args.get('keyword'),
    #                                   device=request.args.get('device'),
    #                                   gender=request.args.get('gender'),
    #                                   ages=request.args.get('ages'))
    return simple_data_controller.data_controller(request.args.get('keyword'))


if __name__ == "__main__":
    app.run()
