from app.models import Order
from app.services import OrderService, PaymentService


class OrderController:

    @staticmethod
    def create_order(name, surname, email, phone, ticket_type) -> Order:
        order = OrderService.create_order(name, surname, email, phone)
        return PaymentService.create_payment(ticket_type, order.id, name, surname, email, phone)

    @staticmethod
    def get_order(order_id) -> Order:
        return OrderService.get_order(order_id)