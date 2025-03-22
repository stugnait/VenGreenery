from app.services import OrderService, PaymentService


class OrderController:

    @staticmethod
    def create_order(name, surname, email, phone, ticket_type):
        order = OrderService.create_order(name, surname, email, phone)
        return PaymentService.create_payment(ticket_type, order.id)