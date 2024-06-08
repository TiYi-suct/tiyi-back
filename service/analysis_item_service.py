from model.models import AnalysisItem, User
from utils.response import Response


class AnalysisItemService:
    @staticmethod
    def list_analysis_items():
        # 可考虑从redis获取
        analysis_items = AnalysisItem.query.all()
        result = []
        for analysis_item in analysis_items:
            result.append(analysis_item.to_dict())
        return Response.success(result)

    @staticmethod
    def calculate_coins_consumption(username, item_names):
        if not item_names or len(item_names) == 0:
            return Response.error('请选择音频分析项目')
        # 当前登录用户
        user = User.query.filter(User.username == username).one_or_none()
        if not user:
            return Response.error('用户不存在')
        # 查询音频分析项目，名称在item_names中，逗号分隔
        item_name_list = item_names.split(',')
        analysis_items = AnalysisItem.query.filter(AnalysisItem.name.in_(item_name_list)).all()
        coins_consumption = 0
        for analysis_item in analysis_items:
            coins_consumption += analysis_item.price
        return Response.success({
            'allow': coins_consumption <= user.music_coin,
            'required': coins_consumption,
            'user_coins': user.music_coin
        })
