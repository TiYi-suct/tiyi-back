import logging
import uuid
from functools import wraps

import jwt
from flask import g, request

from utils.jwt_util import decode_token


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        # 检查用户是否携带token
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return {'code': 1, 'msg': '用户未登录', 'data': ''}, 401
        # 检查token是否有效
        try:
            data = decode_token(token)
            g.username = data['load']
        except jwt.ExpiredSignatureError:
            logging.error(f'Token已过期：{token}')
            return {'code': 1, 'msg': '登录已过期', 'data': ''}, 401
        except jwt.InvalidTokenError:
            logging.error(f'无效的token：{token}')
            return {'code': 1, 'msg': 'token无效', 'data': ''}, 401
        return f(*args, **kwargs)

    return decorated_function
