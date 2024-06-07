"""
用户服务
"""
import logging
import uuid

from model.models import User, db
from utils.response import Response
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class UserService:
    @staticmethod
    def register(data):
        # 检查数据
        if not data or not data.get('username') or not data.get('password'):
            return Response.error_default('用户名和密码不能为空')
        username = data['username']
        password = data['password']
        # 检查用户名是否已经被占用
        if User.query.filter_by(username=username).first():
            return Response.error_default('用户名已存在')
        # 对密码进行加密保存
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(
            username=username,
            password=hashed_password
        )
        # 保存到数据库
        try:
            db.session.add(user)
            db.session.commit()
            return Response.success()
        except Exception as e:
            logging.error(f'保存用户到数据库异常：{e}，用户信息：{user}')
            db.session.rollback()
            return Response.error_default('注册失败')

    @staticmethod
    def login(data):
        if not data or not data.get('username') or not data.get('password'):
            return Response.error_default('用户名和密码不能为空')
        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username).first()
        if not user:
            return Response.error_default('用户不存在')
        if not bcrypt.check_password_hash(user.password, password):
            return Response.error_default('密码错误')
        # todo 保存登录凭证
        token = uuid.uuid4().hex
        return Response.success(token)
