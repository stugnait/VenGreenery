from app.models import Ticket
from app.services import TicketService


class TicketController:

    @staticmethod
    def get_ticket(ticket_id) -> Ticket:
        return TicketService.get_ticket_by_id(ticket_id)