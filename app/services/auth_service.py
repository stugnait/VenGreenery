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