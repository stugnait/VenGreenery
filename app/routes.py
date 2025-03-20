from flask import Blueprint, render_template, request, jsonify
from app.controllers import *


routes = Blueprint('routes', __name__)

@routes.route('/')
def do_order():
    return render_template("order.html")


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

