from app.models import Payment
from app.services import PaymentService

class PaymentController:

    @staticmethod
    def get_payment(payment_id) -> Payment:
        return PaymentService.get_payment(payment_id)

    @staticmethod
    def get_payment_by_order_id(order_id) -> Payment:
        return PaymentService.get_payment_by_order_id(order_id)
