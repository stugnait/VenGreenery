import hashlib
import json
import os
from datetime import datetime
from io import BytesIO

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_mail import Message
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.textobject import PDFTextObject

from app import mail, db, cache
from app.controllers import *
import qrcode
from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize

from app.modules import WayForPay

routes = Blueprint('routes', __name__)


@routes.route('/', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def index():
    return render_template('index.html')


@routes.route('/order')
@cache.cached(timeout=50)
def do_order():
    return render_template("order.html")


@routes.route('/order', methods=['POST'])
def do_order_post():
    try:
        name = request.json.get("name")
        surname = request.json.get("surname")
        email = request.json.get("email")
        phone = request.json.get("phone")
        adult_quantity = int(request.json.get("adult_quantity"))
        child_quantity = int(request.json.get("child_quantity"))
        invoice = OrderController.create_order(name, surname, email, phone, adult_quantity, child_quantity)
        return jsonify(invoice.get("invoiceUrl"))
    except KeyError as e:
        return jsonify({"error": f"No {e} parameter"})


@routes.route('/admin_auth')
def admin_auth():
    if AuthService.check_session(session):
        return redirect(url_for("admin_dashboard.html"))
    return render_template("admin_auth.html")


@routes.route('/verify_qr', methods=['POST'])
def verify_qr():
    try:
        user = None
        if "email" in session:
            user = AdminController.get_user_by_email(session["email"])
        elif "phone" in session:
            user = AdminController.get_user_by_phone(session["phone"])
        else:
            return jsonify({"error": "No user found"})

        qr_data = request.json.get('qr_data')
        qr_dict = json.loads(qr_data)

        name = qr_dict.get("name")
        surname = qr_dict.get("surname")
        email = qr_dict.get("email")
        phone = qr_dict.get("phone")

        if not qr_data:
            return jsonify({"error": "QR code not detected."}), 400

        ticket = TicketController.get_ticket(qr_dict["id"])
        order = OrderController.get_order(ticket.order)
        if ticket:
            if ticket.used:
                return jsonify({"error": "Ticket already used."}), 400
            if name == order.name and surname == order.surname and email == order.email and phone == order.phone:
                ticket.use_date = datetime.now()
                ticket.used = True
                ticket.who_scanned = user.id
                db.session.commit()
                return jsonify({"success": "ok"}), 200
            return jsonify({"error": "Ticket data isn't equal to QR code data."}), 400
        else:
            return jsonify({"error": "Ticket not found."}), 404

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
    if AuthController.check_session(session):
        return render_template("admin_dashboard.html")
    return render_template("admin_auth.html")


def generate_pdf(ticket_id, ticket_naming, image_path):
    pdf_path = f"app/static/pdf/ticket_{ticket_id}.pdf"
    pdf_buffer = BytesIO()
    can = canvas.Canvas(pdf_buffer)
    pdfmetrics.registerFont(TTFont('Arial', 'app/static/fonts/Arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'app/static/fonts/Arial_Bold.ttf'))

    width = defaultPageSize[0]
    height = defaultPageSize[1]

    text = f"Квиток №{ticket_id} ({ticket_naming})"
    text_width = stringWidth(text, "Arial-Bold", 20)

    can.setFont("Arial-Bold", 20)
    headline = PDFTextObject(can, (width - text_width) / 2.0, height - 80.0)
    headline.textLine(text)
    can.drawText(headline)

    text = [
        "Дякуємо за вашу покупку!",
        "",
        "",
        "Ви успішно придбали квиток. Будь ласка, збережіть цей документ та пред’явіть",
        "його на вході.",
        "",
        "",
        f"    Номер квитка: №{ticket_id} ({ticket_naming})",
        f"    Місце проведення: вулиця Шевченка, Мамаївці, Чернівецька область",
        "",
        "",
        "Умови використання:",
        "    • Цей квиток є одноразовим та дійсний лише для одного входу.",
        "    • Доступ можливий тільки за цим QR-кодом.",
        "",
        "Бажаємо вам гарного відпочинку!"
    ]

    can.setFont("Arial", 12)
    main_text = PDFTextObject(can, 100.0, height - 140.0, "LTR")
    main_text.textLines(text)
    can.drawText(main_text)

    can.drawImage(image_path, (width - 300) / 2, 0, width=300, preserveAspectRatio=True, mask='auto')

    can.showPage()
    can.save()
    pdf_buffer.seek(0)

    with open(pdf_path, "wb") as f:
        f.write(pdf_buffer.getvalue())

    return pdf_path


def create_qr_ticket(ticket_type, order):
    ticket = TicketController.create_ticket(ticket_type, order.id)
    ticket_naming = 'Дорослий' if ticket_type == 'adult' else 'Дитячий'

    qr_data = {
        "id": ticket.id,
        "name": order.name,
        "surname": order.surname,
        "email": order.email,
        "phone": order.phone
    }
    json_data = json.dumps(qr_data, separators=(",", ":"))

    img = qrcode.make(json_data)
    img_path = f"app/static/qr/ticket_{qr_data['id']}.png"
    img.save(img_path)

    pdf_path = generate_pdf(qr_data["id"], ticket_naming, img_path)

    return qr_data["id"], pdf_path, ticket_naming


@routes.route("/accept_payment", methods=['POST'])
@cache.cached(timeout=30)
def accept_payment():
    try:
        raw_data = next(iter(request.values.keys()), '{}')
        data = json.loads(raw_data)
        now = datetime.now()

        wfp_order_id = data["orderReference"]
        order_id = wfp_order_id.split("_")[1]
        order = OrderController.get_order(order_id)
        payment = PaymentController.get_payment_by_order_id(order_id)
        if data["reasonCode"] == 1100:
            if not TicketController.get_ticket_by_order_id(order.id):
                pdf_paths = []
                for i in range(payment.adult_quantity):
                    pdf_paths.append(create_qr_ticket("adult", order))

                for i in range(payment.child_quantity):
                    pdf_paths.append(create_qr_ticket("child", order))

                msg = Message('Ваш квиток до Ven Greenery', recipients=[order.email])
                msg.body = "Дякуємо за покупку!"
                for pdf in pdf_paths:
                    with open(pdf[1], 'rb') as f:
                        msg.attach(f"Квиток №{pdf[0]} {pdf[2]}", "application/pdf", f.read())
                mail.send(msg)

                payment.status = "Success"
                payment.end_date = now
                order.status = "Success"
                db.session.commit()
        else:
            payment.status = "Error"
            payment.end_date = now
            order.status = "Error"
            db.session.commit()

        answer = {
            "orderReference": data["orderReference"],
            "status": "accept",
            "time": int(now.timestamp()),
        }
        answer["signature"] = WayForPay.get_answer_signature(os.getenv("MERCHANT_SECRET_KEY"), answer)

        return jsonify(answer), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route("/order_status/<int:order_id>/<string:email>", methods=["GET", "POST"])
def thanks(order_id, email):
    order = OrderController.get_order(order_id)

    if order and order.email == email:
        tickets = TicketController.get_ticket_by_order_id(order_id)
        if tickets:
            tickets_ids = [ticket.id for ticket in tickets]
            return render_template('thanks.html', tickets=tickets_ids)
    return redirect(url_for('routes.index'))
