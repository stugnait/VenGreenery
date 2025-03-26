import hashlib

from app.models import User
from app.repositories import UserRepository
class AdminService:
    @staticmethod
    def create_user(name, password, email, phone) -> User:
        password_encoded = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return UserRepository.create(name, password_encoded, email, phone)

    @staticmethod
    def get_user_by_email(email) -> User:
        return UserRepository.get_user_by_email(email)

    @staticmethod
    def get_user_by_phone(phone) -> User:
        return UserRepository.get_user_by_phone(phone)

