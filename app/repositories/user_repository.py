from app.models import User
from app import db

class UserRepository:
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id) -> User:
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email) -> User:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_phone(phone) -> User:
        return User.query.filter_by(phone=phone).first()

    @staticmethod
    def create(name, password, email, phone):
        new_user = User(name=name, password=password, email=email, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def is_exist(user_id):
        if User.query.get(user_id) is None:
            return False
        return True
