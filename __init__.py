from flask import Flask
from .views import views
from .auth import auth


# Init method to create the app, or re-run for every initialization
def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = '54e24481c2936c021ab570ea568d81db3f7d12da6fe3cdda'
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
