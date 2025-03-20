from app.repositories import TicketRepository
class QRService:

    @staticmethod
    def validate_qr(qr_data):
        ticket = TicketRepository.get_by_id(qr_data)
        if ticket:
            if ticket.used:
                return False
            return True
        return False

