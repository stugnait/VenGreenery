from app.database import db

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(25), nullable=True)

    def __init__(self, name, surname, email, phone, status):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.status = status
