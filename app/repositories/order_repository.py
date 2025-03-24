from app.models import Order
from app import db

class OrderRepository:
    @staticmethod
    def get_by_id(order_id) -> Order:
        return Order.query.get(order_id)

    @staticmethod
    def get_all() -> Order:
        return Order.query.all()

    @staticmethod
    def get_by_email(email) -> Order:
        return Order.query.filter_by(email=email).first()

    @staticmethod
    def get_by_phone(phone) -> Order:
        return Order.query.filter_by(phone=phone).first()

    @staticmethod
    def create(name, surname, email, phone, status) -> Order:
        new_order = Order(name=name, surname=surname, email=email, phone=phone,status=status)
        db.session.add(new_order)
        db.session.commit()
        return new_order
