import hashlib

from app.repositories import UserRepository

class AuthService:
    @staticmethod
    def login_with_email(email, password):
        user = UserRepository.get_user_by_email(email)
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if user and hashed_password == user.password:
            return True
        return False

    @staticmethod
    def login_with_phone(phone, password):
        user = UserRepository.get_user_by_phone(phone)
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if user and hashed_password == user.password:
            return True
        return False

    @staticmethod
    def find_by_email(email):
        user = UserRepository.get_user_by_email(email)
        if user:
            return True
        return False

    @staticmethod
    def find_by_phone(phone):
        user = UserRepository.get_user_by_phone(phone)
        if user:
            return True
        return False


    @staticmethod
    def check_session(session):
        user = None
        key = 'email' if 'email' in session else 'phone' if 'phone' in session else None

        if key:
            user = UserRepository.get_user_by_email(session[key]) if key == 'email' else UserRepository.get_user_by_phone(session[key])

        return user and user.password == session['password']