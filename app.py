from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

# Инициализация приложения
def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '4d7045651894540de9777840b09e4320652cb0bd4b2937ad7dc16b68c62ce514'

    db.init_app(app)

    from routes import routes
    from admin import admin
    from registration import log
    from transaction import api

    app.register_blueprint(routes)
    app.register_blueprint(admin)
    app.register_blueprint(log)
    app.register_blueprint(api)
    return app





