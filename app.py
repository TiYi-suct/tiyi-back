from flask import Flask

from config.config import Config
from config.routes import config_routes
from model.models import db

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
config_routes(app)

if __name__ == '__main__':
    app.run()
