from app.models import User
from app import db

class UserRepository:
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def create(name, password, email, phone):
        new_user = User(name=name, password=password, email=email, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        return new_user

