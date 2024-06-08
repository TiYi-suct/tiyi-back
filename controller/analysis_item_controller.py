from flask import g, request
from flask_restful import Resource

from interceptor.interceptor import login_required
from service.analysis_item_service import AnalysisItemService


class AnalysisItemController(Resource):
    @staticmethod
    def get():
        return AnalysisItemService.list_analysis_items()


'''
计算要分析的项目需要消耗的音乐币
'''


class AnalysisItemConsumption(Resource):
    @login_required
    def get(self):
        item_names = request.args.get('item_names')
        return AnalysisItemService.calculate_coins_consumption(g.username, item_names)
