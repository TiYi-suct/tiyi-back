"""
用户服务
"""
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
            db.session.rollback()
            return Response.error_default('注册失败')
