import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
用户模型
'''


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    music_coin = db.Column(db.Integer, default=100)
    avatar = db.Column(db.String(1023), nullable=True)
    signature = db.Column(db.String(1023), default='在签名中展现你的个性吧！')
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def to_dict(self):
        return {
            'username': self.username,
            'music_coin': self.music_coin,
            'avatar': self.avatar,
            'signature': self.signature
        }


'''
音频模型
'''


class Audio(db.Model):
    __tablename__ = 'audio'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    audio_id = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    extension = db.Column(db.String(255), nullable=False)
    local_path = db.Column(db.String(1023), unique=True, nullable=False)
    url = db.Column(db.String(1023), unique=True, nullable=False)
    tags = db.Column(db.String(1023), unique=False, nullable=False)
    cover = db.Column(db.String(1023), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def to_dict(self):
        return {
            'audio_id': self.audio_id,
            'name': self.name,
            'extension': self.extension,
            'url': self.url,
            'tags': self.tags.split(',') if self.tags else [],
            'cover': self.cover,
            'username': self.username
        }


'''
用户定义音频标签模型
'''


class AudioTags(db.Model):
    __tablename__ = 'audio_tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.String(1023), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


'''
音频分析项目模型
'''


class AnalysisItem(db.Model):
    __tablename__ = 'analysis_item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键id')
    name = db.Column(db.String(255), nullable=False, unique=True, comment='音频分析项名称，如BPM、频谱等')
    price = db.Column(db.Integer, nullable=False, default=0, comment='消耗音乐币数量')
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now(), comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now(), onupdate=datetime.now(), comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }


'''
充值项目模型
'''


class RechargeItem(db.Model):
    __tablename__ = 'recharge_item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键id')
    title = db.Column(db.String(255), nullable=False, comment='充值项标题，如“1元100个音乐币，10元2000个音乐币”等')
    amount = db.Column(db.Integer, nullable=False, comment='音乐币数量')
    price = db.Column(db.Double, nullable=False, comment='价格')
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'amount': self.amount,
            'price': self.price
        }


'''
充值订单模型
'''


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键id')
    username = db.Column(db.String(255), nullable=False, comment='用户名')
    out_trade_no = db.Column(db.String(255), nullable=False, comment='订单号')
    recharge_title = db.Column(db.String(255), nullable=False, comment='充值项标题')
    amount = db.Column(db.Integer, nullable=False, comment='音乐币数量')
    price = db.Column(db.Double, nullable=False, comment='订单金额')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    @staticmethod
    def generate_out_trade_no():
        # 基于当前时间戳和UUID生成唯一订单号
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_id = uuid.uuid4().hex
        out_trade_no = f"ORDER_{timestamp}_{unique_id[:32 - len('ORDER_') - len(timestamp) - 1]}"
        return out_trade_no


'''
支付流水模型
'''


class PayFlow(db.Model):
    __tablename__ = 'pay_flow'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键id')
    trade_no = db.Column(db.String(255), unique=True, nullable=False, comment='交易凭证')
    subject = db.Column(db.String(255), nullable=False, comment='交易名称')
    trade_status = db.Column(db.String(255), nullable=False, comment='交易状态')
    out_trade_no = db.Column(db.String(255), unique=True, nullable=False, comment='商户订单号')
    total_amount = db.Column(db.Double, nullable=False, comment='交易金额')
    buyer_id = db.Column(db.String(255), nullable=False, comment='支付用户id')
    gmt_payment = db.Column(db.String(255), nullable=False, comment='付款时间')
    buyer_pay_amount = db.Column(db.Double, nullable=False, comment='付款金额')
    create_time = db.Column(db.DateTime, default=datetime.now(), comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), comment='更新时间')
