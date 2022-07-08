from flask import Flask, request, jsonify
from services import naver_smart_store, search_volume
app = Flask(__name__)


@app.route("/api/trend/", methods=['GET'])
def shopping_trend_api():
    return get_shopping_keyword_trend(start_date=request.args.get('start-date'),
                                      end_date=request.args.get('end-date'),
                                      time_unit=request.args.get('time-unit'),
                                      category=request.args.get('category'),
                                      keyword=request.args.get('keyword'),
                                      device=request.args.get('device'),
                                      gender=request.args.get('gender'),
                                      ages=request.args.get('ages'))


if __name__ == "__main__":
    app.run()
