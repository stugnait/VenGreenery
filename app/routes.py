import hashlib
import os

from flask import Blueprint, render_template, request, jsonify, session
from flask_mail import Message
from app import mail
from app.controllers import *


routes = Blueprint('routes', __name__)

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

        if not qr_data:
            return jsonify({"error":"QR code not detected."}), 400

        ticket = TicketController.get_ticket(int(qr_data))
        if ticket:
            if ticket.used:
                return jsonify({"error":"Ticket already used."}), 400
            return jsonify({"success": "ok"}), 200
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

@routes.route('/test_email', methods=['GET'])
def test_email():
    try:
        msg = Message('Test Email', recipients=['nikitaz9251015@gmail.com'])
        msg.body = "I'm testing email!"
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {str(e)}"