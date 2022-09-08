from flask import Flask
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api

from config import Config

# TODO  api

from flask_migrate import Migrate
from .models import db as root_db, login_manager, ma

app = Flask(__name__)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

app.config.from_object(Config)

root_db.init_app(app)

migrate = Migrate(app, root_db)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin'

ma.init_app(app)
