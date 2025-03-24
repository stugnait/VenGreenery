import hashlib
import json
import os
from io import BytesIO

from flask import Blueprint, render_template, request, jsonify, session
from flask_mail import Message
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.textobject import PDFTextObject

from app import mail, db
from app.controllers import *
import qrcode
from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')



@routes.route('/order')
def do_order():
    return render_template("order.html")

@routes.route('/order', methods=['POST'])
def do_order_post():
    try:
        name = request.json.get("name")
        surname = request.json.get("surname")
        email = request.json.get("email")
        phone = request.json.get("phone")
        ticket_type = request.json.get("ticket_type")
        invoice = OrderController.create_order(name, surname, email, phone, ticket_type).get("invoiceUrl")
        return jsonify(invoice)
    except KeyError as e:
        return jsonify({"error": f"No {e} parameter"})

@routes.route('/admin_auth')
def admin_auth():
    return render_template("admin_auth.html")

@routes.route('/verify_qr', methods=['POST'])
def verify_qr():
    try:
        qr_data = request.json.get('qr_data')
        qr_dict = json.loads(qr_data)

        name=qr_dict.get("name")
        surname=qr_dict.get("surname")
        email=qr_dict.get("email")
        phone=qr_dict.get("phone")

        print(qr_dict)
        if not qr_data:
            return jsonify({"error":"QR code not detected."}), 400

        ticket = TicketController.get_ticket(qr_dict["id"])
        order = OrderController.get_order(ticket.order)
        print(f"name: {name} surname: {surname} email: {email} phone: {phone}")
        print(f"name: {order.name} surname: {order.surname} email: {order.email} phone: {order.phone}")
        if ticket:
            if ticket.used:
                return jsonify({"error":"Ticket already used."}), 400
            if name==order.name and surname==order.surname and email==order.email and phone==order.phone:
                return jsonify({"success": "ok"}), 200
            return jsonify({"error":"Ticket data isn't equal to QR code data."}), 400
        else:
            return jsonify({"error":"Ticket not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/find_user", methods=['POST'])
def find_user():
    try:
        cred_type = request.json.get("type")
        answer = False
        if cred_type:
            if cred_type == "email":
                answer = AuthController.check_email(request.json.get("value"))
            elif cred_type == "phone":
                answer = AuthController.check_phone(request.json.get("value"))
            return (jsonify({"success": "ok"}), 200) if answer else (jsonify({"error": "User not found."}), 401)

        return jsonify({"error": "Invalid credentials."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/login", methods=['POST'])
def login():
    try:
        password = request.json.get("password")
        result = False
        if email := request.json.get("email"):
            session["email"] = email
            result = AuthController.login_with_email(email, password)
        elif phone := request.json.get("phone"):
            session["phone"] = phone
            result = AuthController.login_with_phone(phone, password)
        else:
            return jsonify({"error": "Bad request"}), 400

        if result:
            session["password"] = hashlib.sha256(password.encode('utf-8')).hexdigest()
            return jsonify({"success": "ok"}), 200
        return jsonify({"error": "Invalid credentials."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/admin_dashboard", methods=['GET'])
def admin_dashboard():
    if AuthService.check_session(session):
        return render_template("admin_dashboard.html")
    return "Хто може дати/продати цибулю?"





###testing features
@routes.route('/test_qr', methods=['GET'])
def test_qr():
    payment_id = 1
    payment = PaymentController.get_payment(payment_id)
    order = OrderController.get_order(payment.order)

    ticket = TicketController.create_ticket(payment.ticket_type, order.id)

    data = {"id": ticket.id, "name": order.name, "surname": order.surname, "email": order.email, "phone": order.phone}
    json_data = json.dumps(data, separators=(",", ":"))

    img = qrcode.make(json_data)
    img_path = f"app/static/qr/qr_{ticket.id}.png"
    img.save(img_path)

    pdf_path = f"app/static/pdf/pdf_{ticket.id}.pdf"
    pdf_buffer = BytesIO()
    can = canvas.Canvas(pdf_buffer)
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

    width = defaultPageSize[0]
    height = defaultPageSize[1]

    text = "Чек"
    text_width = stringWidth(text, "Arial", 12)

    can.setFont("Arial", 12)
    hui = PDFTextObject(can, (width-text_width)/2.0, height-20.0, "LTR")
    hui.textLines([text, text, text, text, text, text, text, text])
    can.drawText(hui)
    can.drawImage(img_path, (width-300)/2, 0, width=300, preserveAspectRatio=True, mask='auto')

    can.showPage()
    can.save()
    pdf_buffer.seek(0)



    payment.status = "Success"
    db.session.commit()


    try:
        msg = Message('Test Email', recipients=['nikitaz9251015@gmail.com'])
        msg.body = "I'm testing email!"
        msg.attach(pdf_path, "application/pdf", pdf_buffer.read())
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {str(e)}"