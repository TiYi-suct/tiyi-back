from model.models import RechargeItem
from utils.response import Response


class RechargeItemService:
    @staticmethod
    def list_recharge_items():
        # 可考虑从redis获取
        recharge_items = RechargeItem.query.all()
        result = []
        for recharge_item in recharge_items:
            result.append(recharge_item.to_dict())
        return Response.success(result)
