from model.models import AnalysisItem
from utils.response import Response


class AnalysisItemService:
    @staticmethod
    def list_analysis_items():
        analysis_items = AnalysisItem.query.all()
        result = []
        for analysis_item in analysis_items:
            result.append(analysis_item.to_dict())
        return Response.success(result)
