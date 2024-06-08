import logging

from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.util.SignatureUtils import verify_with_rsa

from config.alipay_config import alipay_config
from config.config import Config
from model.models import RechargeItem, Order, db, User, PayFlow
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
        model.total_amount = recharge_item.price
        model.subject = recharge_item.title
        model.product_code = 'QUICK_MSECURITY_PAY'
        request = AlipayTradeAppPayRequest(biz_model=model)
        request.notify_url = Config.NOTIFY_URL
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

    @staticmethod
    def notify(data: dict):
        # 获取支付宝签名
        signature = data.pop('sign', None)
        # 移除签名类型
        data.pop('sign_type')
        # 验证签名
        success = verify_with_rsa(
            Config.ALIPAY_PUBLIC_KEY,
            '&'.join(f"{key}={value}" for key, value in sorted(data.items())).encode(),
            signature
        )
        if not success:
            logging.error(f'验签失败：{data}')
            return
        # 验签通过，检查支付状态
        trade_status = data.get('trade_status')
        # 记录支付流水
        pay_flow = PayFlow(
            trade_no=data.get('trade_no'),
            subject=data.get('subject'),
            trade_status=trade_status,
            out_trade_no=data.get('out_trade_no'),
            total_amount=data.get('total_amount'),
            buyer_id=data.get('buyer_id'),
            gmt_payment=data.get('gmt_payment'),
            buyer_pay_amount=data.get('buyer_pay_amount')
        )
        db.session.add(pay_flow)
        # 支付异常，不增加用户的音乐币数量
        if not trade_status == 'TRADE_SUCCESS':
            logging.error(f'支付异常：{trade_status}，回调数据：{data}')
            db.session.commit()
            return
        # 支付成功，查询订单信息
        out_trade_no = data.get('out_trade_no')
        order = Order.query.filter(Order.out_trade_no == out_trade_no).one_or_none()
        if not order:
            logging.error(f'订单未找到：{out_trade_no}')
            db.session.commit()
            return
        # 更新用户音乐币数量
        user = User.query.filter(User.username == order.username).one_or_none()
        if not user:
            logging.error(f'用户未找到：{order.username}')
            db.session.commit()
            return
        user.music_coin += order.amount
        db.session.commit()
        return
