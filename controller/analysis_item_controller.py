from flask_restful import Resource

from service.analysis_item_service import AnalysisItemService


class AnalysisItemController(Resource):
    @staticmethod
    def get():
        return AnalysisItemService.list_analysis_items()
