import os.path

from flask import Flask

from config.config import Config
from config.routes import config_routes
from model.models import db

app = Flask(__name__)

# 加载配置
app.config.from_object(Config())
# 初始化数据库连接
db.init_app(app)
# 配置路由
config_routes(app)
# 在当前工作区创建存储目录
if not os.path.exists(Config.STORE_FOLDER):
    os.makedirs(Config.STORE_FOLDER)

if __name__ == '__main__':
    app.run()
