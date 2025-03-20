from app.repositories import PaymentRepository

class PaymentService:
    @staticmethod
    def create_payment(ticket_type, start_date):
        return PaymentRepository.create(ticket_type, start_date, None, "Waiting")

    @staticmethod
    def get_payment(payment_id):
        return PaymentRepository.get_by_id(payment_id)

    @staticmethod
    def get_all_payments():
        return PaymentRepository.get_all()

