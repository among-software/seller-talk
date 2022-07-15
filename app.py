import asyncio

import requests
from flask import Flask, request, Response, jsonify
from controller import simple_data_controller, category_list_controller, detail_controller, related_controller
from flask_cors import CORS, cross_origin
import json
app = Flask(__name__)

CORS(app)


@app.route("/api/simple-data/", methods=['GET'])
def return_simple_data():
    return simple_data_controller.data_controller(request.args.get('keyword'))


@app.route("/api/category-list/", methods=['GET'])
def category_list():
    return category_list_controller.category_list_controller(request.args.get('keyword'))


@app.route("/api/detail/", methods=['GET'])
def detail():
    return detail_controller.detail_controller(start_date=request.args.get('start-date'),
                                               end_date=request.args.get('end-date'),
                                               keyword=request.args.get('keyword'))


@app.route("/api/related/", methods=['GET'])
def related():
    return json.dumps(related_controller.controller(keyword=request.args.get('keyword'),
                                                    keyword_classification=request.args.get('classification'),
                                                    keyword_volume=request.args.get('volume'),
                                                    keyword_product=request.args.get('product'),
                                                    competitive_strength=request.args.get('competition')),
                      ensure_ascii=False)


if __name__ == "__main__":
    app.run()
