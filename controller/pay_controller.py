import logging

from flask import request, g
from flask_restful import Resource

from interceptor.interceptor import login_required
from service.pay_service import PayService
from utils.response import Response


class GetOrderInfo(Resource):
    @login_required
    def get(self):
        recharge_id = request.args.get('recharge_id')
        return PayService.sign_order_info(g.username, recharge_id)


class PayResultNotify(Resource):
    @staticmethod
    def post():
        logging.debug(f'支付结果回调：{request}')
        PayService.notify(request.form.to_dict())
        return Response.success()
