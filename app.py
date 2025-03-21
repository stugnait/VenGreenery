from flask_mail import Message

from app import create_app
from app import routes
from app import mail

app = create_app()
app.register_blueprint(routes.routes)




if __name__ == '__main__':
    app.run(debug=True)