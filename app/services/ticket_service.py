from app.repositories import TicketRepository

class TicketService:

    @staticmethod
    def get_ticket_by_id(ticket_id):
        return TicketRepository.get_by_id(ticket_id)

    @staticmethod
    def get_all_tickets(self):
        return TicketRepository.get_all()

    @staticmethod
    def create_ticket(ticket_type, create_date, order):
        return TicketRepository.create(ticket_type, False, create_date, None, order, None)