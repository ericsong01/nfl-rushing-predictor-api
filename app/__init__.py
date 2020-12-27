from flask import Flask, request 
from config import Configuration
from app.api import bp as api_bp
from app.site import bp as site_bp
from app.extensions import db, migrate, bootstrap, login_manager

def create_app():
    app = Flask(__name__)
    bootstrap.init_app(app)

    app.config.from_object('config.Configuration')

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(site_bp)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'site.login'

    return app 

 

