import hashlib

from app.repositories import UserRepository
class AdminService:
    @staticmethod
    def create_user(name, password, email, phone):
        password_encoded = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return UserRepository.create(name, password_encoded, email, phone)

