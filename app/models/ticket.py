from app.database import db
from app.models.order import Order
from app.models.user import User

class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String, nullable=False)
    used = db.Column(db.Boolean, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)
    use_date = db.Column(db.DateTime, nullable=True)
    order = db.Column(db.Integer, nullable=False)
    who_scanned = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.ForeignKeyConstraint([order], [Order.id], ondelete='NO ACTION'),
        db.ForeignKeyConstraint([who_scanned], [User.id], ondelete='NO ACTION')
    )

    def __init__(self, ticket_type, used, create_date, use_date, order, who_scanned):
        self.type = ticket_type
        self.used = used
        self.create_date = create_date
        self.use_date = use_date
        self.order = order
        self.who_scanned = who_scanned
