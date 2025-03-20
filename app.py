from flask_mail import Message

from app import create_app
from app import routes
from app import mail

app = create_app()
app.register_blueprint(routes.routes)


@app.route('/test_email', methods=['GET'])
def test_email():
    try:
        msg = Message('Test Email', recipients=['nikitaz9251015@gmail.com'])
        msg.body = "I'm testing email!"
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)