from app.database import db
from app.models.order import Order

class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String, nullable=False)
    used = db.Column(db.Boolean, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)
    use_date = db.Column(db.DateTime)
    order = db.Column(db.Integer, nullable=False)
    who_scanned = db.Column(db.Integer)

    __table_args__ = (
        db.ForeignKeyConstraint([order], [Order.id], ondelete='NO ACTION'),
    )

    def __init__(self, ticket_type, used, create_date, use_date, order, who_scanned):
        self.__type = ticket_type
        self.__used = used
        self.__create_date = create_date
        self.__use_date = use_date
        self.__order = order
        self.__who_scanned = who_scanned
