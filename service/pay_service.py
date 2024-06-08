import logging
import uuid
from datetime import datetime

from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest

from config.alipay_config import alipay_config
from model.models import RechargeItem, Order, db
from utils.response import Response


class PayService:

    @staticmethod
    def sign_order_info(username, recharge_id):
        # 查询充值项
        recharge_item = RechargeItem.query.filter_by(id=recharge_id).first()
        if not recharge_item:
            return Response.error('请选择要充值的项目')
        # 生成唯一订单号
        out_trade_no = Order.generate_out_trade_no()
        # 构建订单信息
        order = Order(
            username=username,
            out_trade_no=out_trade_no,
            recharge_title=recharge_item.title,
            amount=recharge_item.amount,
            price=recharge_item.price
        )
        # 对订单信息进行签名
        model = AlipayTradeAppPayModel()
        model.out_trade_no = out_trade_no
        model.total_amount = recharge_item.amount
        model.subject = recharge_item.title
        model.product_code = 'QUICK_MSECURITY_PAY'
        request = AlipayTradeAppPayRequest(biz_model=model)
        try:
            signed_order_info = alipay_config.client.sdk_execute(request)
            # 保存订单信息到数据库
            db.session.add(order)
            db.session.commit()
            # 返回签名后的订单信息
            return Response.success(signed_order_info)
        except Exception as e:
            logging.error(f'订单信息签名出现错误：{e}')
            db.session.rollback()
            return Response.error('订单信息签名失败')
