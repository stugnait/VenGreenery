from flask import Flask
from flask_migrate import Migrate
from app.database import db
from app import config

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    app.config.from_object(config)

    db.init_app(app)
    from app.models.user import User
    from app.models.order import Order
    from app.models.payment import Payment
    from app.models.ticket import Ticket
    migrate = Migrate(app, db)

    return app
