from app.repositories import OrderRepository

class OrderService:
    @staticmethod
    def create_order(full_name, email, phone, payment):
        return OrderRepository.create(full_name, email, phone, payment, "Waiting")

    @staticmethod
    def get_order(order_id):
        return OrderRepository.get_by_id(order_id)

    @staticmethod
    def get_all_orders():
        return OrderRepository.get_all()

    @staticmethod
    def get_order_by_email(email):
        return OrderRepository.get_by_email(email)

    @staticmethod
    def get_order_by_phone(phone):
        return OrderRepository.get_by_phone(phone)