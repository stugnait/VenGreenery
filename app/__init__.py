from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from app.database import db
from app.config import Config

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)

    from app.models.user import User
    from app.models.payment import Payment
    from app.models.order import Order
    from app.models.ticket import Ticket
    migrate = Migrate(app, db)

    return app
