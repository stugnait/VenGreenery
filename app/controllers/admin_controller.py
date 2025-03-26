from app.models import User
from app.repositories import UserRepository
from app.services.admin_service import AdminService

class AdminController:
    @staticmethod
    def get_user_by_id(user_id) -> User:
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def get_user_by_phone(phone) -> User:
        return UserRepository.get_user_by_phone(phone)

    @staticmethod
    def get_user_by_email(email) -> User:
        return UserRepository.get_user_by_email(email)