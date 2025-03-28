import os
from typing import List

from app.models import Payment
from app.modules import WayForPay
from app.repositories import PaymentRepository
from datetime import datetime, timedelta

class PaymentService:
    @staticmethod
    def create_payment(adult_quantity, child_quantity, order_id, name, surname, email, phone):
        now = datetime.now() + timedelta(seconds=30)

        amount = adult_quantity * Payment.ADULT_PRICE + child_quantity * Payment.CHILD_PRICE

        product_name, product_count, product_price = [], [], []
        if adult_quantity > 0:
            product_name.append('Дорослий квиток')
            product_count.append(adult_quantity)
            product_price.append(Payment.ADULT_PRICE)

        if child_quantity > 0:
            product_name.append('Дитячий квиток')
            product_count.append(child_quantity)
            product_price.append(Payment.CHILD_PRICE)



        wfp = WayForPay(os.getenv("MERCHANT_ACCOUNT"), os.getenv("MERCHANT_SECRET_KEY"), os.getenv("MERCHANT_DOMAIN"))
        invoice = wfp.create_invoice({
            "orderReference": f"test_{order_id}_test_testing_DEV",
            "orderDate": int(now.timestamp()),
            "orderTimeout": 900, #15 хв на оплату
            "amount": amount,
            "currency": "UAH",
            "productName": product_name,
            "productCount": product_count,
            "productPrice": product_price,
            "clientFirstName": name,
            "clientLastName": surname,
            "clientEmail": email,
            "clientPhone": phone,
            "serviceUrl": f"{os.getenv("MERCHANT_DOMAIN")}accept_payment",
            "returnUrl": f"{os.getenv("MERCHANT_DOMAIN")}order_status/{order_id}/{email}"
        })


        PaymentRepository.create(amount, adult_quantity, child_quantity, now, order_id, "Waiting")
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

