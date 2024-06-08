"""
统一响应工具类
"""


class Response:
    @staticmethod
    def success(data: object = '', msg: str = '操作成功'):
        return {'code': 0, 'msg': msg, 'data': data}, 200

    @staticmethod
    def success_of(code: int, data: object, msg: str = '操作成功'):
        return {'code': code, 'msg': msg, 'data': data}, 200

    @staticmethod
    def error_custom(code: int, msg: str, data: object = ''):
        return {'code': code, 'msg': msg, 'data': data}, 400

    @staticmethod
    def error(msg: str):
        return {'code': 1, 'msg': msg, 'data': ''}, 400
