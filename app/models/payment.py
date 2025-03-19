from app.database import db

class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float, nullable=False)
    ticket_type = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String, nullable=False)


    def __init__(self, price, payment_type, start_date, end_date, status):
        self.__price = price
        self.__type = payment_type
        self.__start_date = start_date
        self.__end_date = end_date