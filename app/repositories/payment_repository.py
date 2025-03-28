from typing import List

from app.models import Payment
from app import db

class PaymentRepository:
    @staticmethod
    def get_by_id(payment_id) -> Payment:
        return Payment.query.filter_by(id=payment_id).first()

    @staticmethod
    def get_by_order_id(order_id) -> Payment:
        return Payment.query.filter_by(order=order_id).first()

    @staticmethod
    def get_all() -> List[Payment]:
        return Payment.query.all()

    @staticmethod
    def create(price, adult_quantity, child_quantity, start_date, order, status) -> Payment:
        new_payment = Payment(price, adult_quantity, child_quantity, start_date, None, order, status)
        db.session.add(new_payment)
        db.session.commit()
        return new_payment

