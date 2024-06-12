from flask_restful import Resource

from service.recharge_item_service import RechargeItemService


class RechargeItemController(Resource):
    @staticmethod
    def get():
        return RechargeItemService.list_recharge_items()
