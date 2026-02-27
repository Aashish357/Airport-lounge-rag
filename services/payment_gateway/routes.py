import os
from flask import Blueprint, request, render_template, redirect, url_for,jsonify
from common.response import ok, err
from common.config import Settings
from .service import (
    create_order,
    initiate_payment,
    capture_payment,
    refund_payment,
    verify_signature,
    get_order,
    get_payment
)


from .models import PAYMENT_GATEWAY_DB

# Get the absolute path to the templates folder
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
payment_bp = Blueprint("payment", __name__, url_prefix="/payment", template_folder=template_dir)


# ---------------------------
# Create Order
# ---------------------------
@payment_bp.route("/api/orders", methods=["POST"])
def api_create_order():
    """
    {
            "user_id" : "USR_121",
            "token_fee": "0",
            "lounge_fee": "500", 
    }
    """
    data = request.json or {}
    user_id = data.get("user_id")
    if not user_id:
        return err("user_id is required", 400)

    token_fee = data.get("token_fee", 0)
    lounge_fee = data.get("lounge_fee", 0)

    order_id, order = create_order(order_id, token_fee, lounge_fee)

    return jsonify({
        "order_id": order_id,
        "amount": order.get("amount"),
        "currency": "INR",
        "checkout_url": f"http://127.0.0.1:8000/payment/checkout/{order_id}"
    })


# ---------------------------
# Get Order
# ---------------------------
@payment_bp.route("/api/orders/<order_id>", methods=["GET"])
def api_get_order(order_id):
    """
    GET
    /api/orders/ORDER_001
    """
    order = get_order(order_id)
    if not order:
        return err("Invalid order_id", 404)

    return jsonify({
        "order_id": order_id,
        "user_id": order.get("user_id"),
        "amount": order.get("amount"),
        "status": order.get("status")
    })


# ---------------------------
# Checkout Page
# ---------------------------
@payment_bp.route("/checkout/<order_id>", methods=["GET"])
def checkout(order_id):
    order = get_order(order_id)
    if not order:
        return "Invalid Order", 404
    return jsonify(
        { **order}
        )


# ---------------------------
# Pay Button pressed
# ---------------------------
@payment_bp.route("/pay/<order_id>", methods=["POST"])
def pay(order_id):
    '''
    {
    "order_id":"ORDER_001"
    }
    
    '''
    method = request.form.get("method", "UPI")  # in checkout.html add dropdown
    order, payment, payment_id = initiate_payment(order_id, method=method)

    if not order or not payment:
        return "Invalid Order", 404

    if payment.get("status") == "FAILED":
        return redirect(url_for("payment.failure", payment_id=payment_id))

    # capture after authorization
    capture_payment(payment_id)
    return redirect(url_for("payment.success", payment_id=payment_id))


# ---------------------------
# Payment Success/Failure Pages
# ---------------------------
@payment_bp.route("/success/<payment_id>", methods=["GET"])
def success(payment_id):
    return render_template("success.html", payment_id=payment_id)

@payment_bp.route("/failure/<payment_id>", methods=["GET"])
def failure(payment_id):
    return render_template("failure.html", payment_id=payment_id)


# ---------------------------
# Webhook (Enterprise)
# ---------------------------
@payment_bp.route("/api/webhooks/payment", methods=["POST"])
def payment_webhook():
    ''''{"order_id":"ORDER_001",
"X-Signature":"b6e52836306102a50bee2ccb61a4f39de56a3bc107a2a44a9814d22a6ad1bd06"}
    '''
    settings = Settings()
    signature = request.headers.get("X-Signature")
    payload = request.json or {}

    if not signature:
        return err("Missing X-Signature", 400)

    if not verify_signature(payload, signature, settings.WEBHOOK_SECRET):
        return err("Invalid signature", 403)

    payment_id = payload.get("payment_id")
    status = payload.get("status")

    payment = get_payment(payment_id)
    if not payment:
        return err("Invalid payment_id", 404)

    payment["status"] = status
    order_id = payment.get("order_id")
    order = get_order(order_id)

    if status == "CAPTURED" and order:
        order["status"] = "PAID"

    return ok({"message": "Webhook processed"})


# ---------------------------
# Refund
# ---------------------------
@payment_bp.route("/api/refunds", methods=["POST"])
def api_refund():
    '''{"order_id": "ORDER_001","payment_id": "PAY_001",
    "amount": 500
}'''
    data = request.json or {}
    order_id = data.get("order_id")
    payment_id = data.get("payment_id")
    amount = data.get("amount")

    if not order_id or not payment_id or amount is None:
        return err("order_id, payment_id, amount required", 400)

    refund_id, refund = refund_payment(order_id, payment_id, int(amount))
    
    if not refund:
        return err("Refund creation failed", 500)

    return ok({
        "refund_id": refund_id,
        "status": refund.get("status"),
        "amount": refund.get("amount")
    })

