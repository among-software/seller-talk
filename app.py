import asyncio

import requests
from flask import Flask, request, make_response
from controller import simple_data_controller, category_list_controller, detail_controller, related_controller
from flask_cors import CORS, cross_origin
import json
app = Flask(__name__)

CORS(app)


@app.route("/api/simple-data/", methods=['GET'])
def return_simple_data():
    try:
        return simple_data_controller.data_controller(request.args.get('keyword'))
    except:
        return make_response('Internal Server Error', 500)


@app.route("/api/category-list/", methods=['GET'])
def category_list():
    try:
        return category_list_controller.category_list_controller(request.args.get('keyword'))
    except:
        return make_response('Internal Server Error', 500)


@app.route("/api/detail/", methods=['GET'])
def detail():
    try:
        return detail_controller.detail_controller(start_date=request.args.get('start-date'),
                                                   end_date=request.args.get('end-date'),
                                                   keyword=request.args.get('keyword'))
    except:
        return make_response('Internal Server Error', 500)


@app.route("/api/related/", methods=['GET'])
def related():
    try:
        return json.dumps(related_controller.controller(keyword=request.args.get('keyword'),
                                                    keyword_classification=request.args.get('classification'),
                                                    keyword_total_query=request.args.get('total-query'),
                                                    keyword_items=request.args.get('items'),
                                                    competitive_strength=request.args.get('competition'),
                                                    list_index=request.args.get('list-index')),
                      ensure_ascii=False)
    except:
        return make_response('Internal Server Error', 500)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=80)
