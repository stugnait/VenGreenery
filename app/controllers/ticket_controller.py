from app.models import Ticket
from app.services import TicketService


class TicketController:

    @staticmethod
    def get_ticket(ticket_id) -> Ticket:
        return TicketService.get_ticket_by_id(ticket_id)

    @staticmethod
    def get_ticket_by_order_id(order_id) -> Ticket:
        return TicketService.get_ticket_by_order_id(order_id)

    @staticmethod
    def create_ticket(ticket_type, order_id) -> Ticket:
        return TicketService.create_ticket(ticket_type, order_id)