from app.models import Payment
from app import db

class PaymentRepository:
    @staticmethod
    def get_by_id(payment_id):
        return Payment.query.filter_by(id=payment_id).first()

    @staticmethod
    def get_all():
        return Payment.query.all()

    @staticmethod
    def create(price, ticket_type, start_date, end_date, status):
        new_payment = Payment(price, ticket_type, start_date, end_date, status)
        db.session.add(new_payment)
        db.session.commit()
        return new_payment

