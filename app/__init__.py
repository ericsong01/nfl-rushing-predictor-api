from flask import Flask, request 
from config import Configuration
from app.api import bp as api_bp
from app.site import bp as site_bp
from app.extensions import bootstrap
from app.utils import Utils 

def create_app():
    app = Flask(__name__)
    bootstrap.init_app(app)

    Utils.load_model_and_utils()

    app.config.from_object('config.Configuration')

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(site_bp)

    return app 

 

