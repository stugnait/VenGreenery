from sqlalchemy import ForeignKeyConstraint

from app.database import db
from app.models.order import Order

class Payment(db.Model):
    CHILD_PRICE = 100
    # CHILD_PRICE = 1
    ADULT_PRICE = 250
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float, nullable=False)
    adult_quantity = db.Column(db.Integer, nullable=True)
    child_quantity = db.Column(db.Integer, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    order = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint([order], [Order.id], ondelete='NO ACTION'),
    )

    def __init__(self, price, adult_quantity, child_quantity, start_date, end_date, order, status):
        self.price = price
        self.adult_quantity = adult_quantity
        self.child_quantity = child_quantity
        self.start_date = start_date
        self.end_date = end_date
        self.order = order
        self.status = status
