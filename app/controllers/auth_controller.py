from app.services import AuthService


class AuthController:

    @staticmethod
    def check_email(email):
        return AuthService.find_by_email(email)

    @staticmethod
    def check_phone(phone):
        return AuthService.find_by_phone(phone)

    @staticmethod
    def login_with_email(email, password):
        return AuthService.login_with_email(email, password)

    @staticmethod
    def login_with_phone(phone, password):
        return AuthService.login_with_phone(phone, password)

    @staticmethod
    def check_session(session):
        return AuthService.check_session(session)