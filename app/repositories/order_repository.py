from app.models import Order
from app import db

class OrderRepository:
    @staticmethod
    def get_by_id(order_id):
        return Order.query.get(order_id)

    @staticmethod
    def get_all():
        return Order.query.all()

    @staticmethod
    def get_by_email(email):
        return Order.query.filter_by(email=email).first()

    @staticmethod
    def get_by_phone(phone):
        return Order.query.filter_by(phone=phone).first()

    @staticmethod
    def create(full_name, email, phone, payment, status):
        new_order = Order(full_name=full_name, email=email, phone=phone,)
        db.session.add(new_order)
        db.session.commit()
        return new_order
