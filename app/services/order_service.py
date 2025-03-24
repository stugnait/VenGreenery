from app.models import Order
from app.repositories import OrderRepository

class OrderService:
    @staticmethod
    def create_order(name, surname, email, phone) -> Order:
        return OrderRepository.create(name, surname, email, phone, "Waiting")

    @staticmethod
    def get_order(order_id) -> Order:
        return OrderRepository.get_by_id(order_id)

    @staticmethod
    def get_all_orders() -> Order:
        return OrderRepository.get_all()

    @staticmethod
    def get_order_by_email(email) -> Order:
        return OrderRepository.get_by_email(email)

    @staticmethod
    def get_order_by_phone(phone) -> Order:
        return OrderRepository.get_by_phone(phone)