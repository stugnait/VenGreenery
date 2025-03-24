import os
from typing import List

from app.models import Payment
from app.modules import WayForPay
from app.repositories import PaymentRepository
from datetime import datetime, timedelta

class PaymentService:
    @staticmethod
    def create_payment(ticket_type, order_id, name, surname, email, phone):
        now = datetime.now() + timedelta(seconds=30)
        price = Payment.ADULT_PRICE if ticket_type=="adult" else Payment.CHILD_PRICE

        wfp = WayForPay(os.getenv("MERCHANT_ACCOUNT"), os.getenv("MERCHANT_SECRET_KEY"), os.getenv("MERCHANT_DOMAIN"))
        invoice = wfp.create_invoice({
            "orderReference": f"test_{order_id}_test_testing",
            "orderDate": int(now.timestamp()),
            "amount": price,
            "currency": "UAH",
            "productName": [ticket_type],
            "productCount": [1],
            "productPrice": [price],
            "clientFirstName": name,
            "clientLastName": surname,
            "clientEmail": email,
            "clientPhone": phone
        })
        PaymentRepository.create(price, ticket_type, now, order_id, "Waiting")
        return invoice

    @staticmethod
    def get_payment(payment_id) -> Payment:
        return PaymentRepository.get_by_id(payment_id)

    @staticmethod
    def get_payment_by_order_id(order_id) -> Payment:
        return PaymentRepository.get_by_order_id(order_id)

    @staticmethod
    def get_all_payments() -> List[Payment]:
        return PaymentRepository.get_all()

