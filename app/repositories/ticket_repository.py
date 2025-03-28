from datetime import datetime
from typing import List

from app.models import Ticket
from app import db

class TicketRepository:
    @staticmethod
    def get_by_id(ticket_id) -> Ticket:
        return Ticket.query.get(ticket_id)

    @staticmethod
    def get_ticket_by_order_id(order_id) -> List[Ticket]:
        return Ticket.query.filter_by(order=order_id).all()

    @staticmethod
    def get_all() -> List[Ticket]:
        return Ticket.query.all()

    @staticmethod
    def create(ticket_type, order) -> Ticket:
        now = datetime.now()
        new_ticket = Ticket(ticket_type=ticket_type, used=False, create_date=now, use_date=None, order=order, who_scanned=None)
        db.session.add(new_ticket)
        db.session.commit()
        return new_ticket