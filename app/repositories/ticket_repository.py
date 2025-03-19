from app.models import Ticket
from app import db

class TicketRepository:
    @staticmethod
    def get_by_id(ticket_id):
        return Ticket.query.get(ticket_id)

    @staticmethod
    def get_all():
        return Ticket.query.all()

    @staticmethod
    def create(ticket_type, used, create_date, use_date, order, who_scanned):
        new_ticket = Ticket(ticket_type=ticket_type, used=used, create_date=create_date, use_date=use_date, order=order, who_scanned=who_scanned)
        db.session.add(new_ticket)
        db.session.commit()
        return new_ticket