from app.database import db
from sqlalchemy import ForeignKeyConstraint
from app.models.payment import Payment

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    payment = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(25), nullable=True)

    __table_args__ = (
        ForeignKeyConstraint([payment], [Payment.id], ondelete='NO ACTION'),
    )

    def __init__(self, full_name, email, phone, payment, status):
        self.__full_name = full_name
        self.__email = email
        self.__phone = phone
        self.__payment = payment
        self.__status = status
