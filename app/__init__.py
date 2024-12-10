from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from . import routes, models
        db.create_all()

        # Populate mock data
        from mock_data.mock_students import populate_mock_data
        populate_mock_data(db)

    return app
