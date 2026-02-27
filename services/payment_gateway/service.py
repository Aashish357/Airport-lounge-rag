import uuid, random, hmac, hashlib, json
from datetime import datetime
from common.config import Settings
from .models import PAYMENT_GATEWAY_DB


def get_order(order_id):
    """Retrieve order from database"""
    return PAYMENT_GATEWAY_DB.get(order_id)


def get_payment(payment_id):
    """Retrieve payment from database"""
    return PAYMENT_GATEWAY_DB.get(payment_id)


def get_refund(refund_id):
    """Retrieve refund from database"""
    return PAYMENT_GATEWAY_DB.get(refund_id)


def create_order(user_id, token_fee, lounge_fee):
    """Create a new order in the database"""
    total = int(token_fee) + int(lounge_fee)
    order_id = f"order_{uuid.uuid4().hex[:10]}"
    
    order = {
        "table_name": "pg_order",
        "user_id": user_id,
        "token_fee": token_fee,
        "lounge_fee": lounge_fee,
        "amount": total,
        "status": "CREATED",
        "created_at": datetime.now().isoformat()
    }
    
    PAYMENT_GATEWAY_DB[order_id] = order
    return order_id, order


def initiate_payment(order_id, method="UPI"):
    """Initiate payment for an order"""
    settings = Settings()
    order = get_order(order_id)
    if not order:
        return None, None, None

    payment_id = f"pay_{uuid.uuid4().hex[:10]}"

    payment = {
        "table_name": "pg_payment",
        "order_id": order_id,
        "method": method,
        "status": "AUTHORIZED" if random.random() < settings.PAYMENT_SUCCESS_RATE else "FAILED",
        "gateway_ref": f"gw_{uuid.uuid4().hex[:8]}",
        "created_at": datetime.now().isoformat()
    }
    
    PAYMENT_GATEWAY_DB[payment_id] = payment
    return order, payment, payment_id


def capture_payment(payment_id):
    """Capture an authorized payment"""
    payment = get_payment(payment_id)
    if not payment:
        return None

    order_id = payment.get("order_id")
    order = get_order(order_id)
    if not order:
        return None

    if payment.get("status") != "AUTHORIZED":
        return payment

    payment["status"] = "CAPTURED"
    order["status"] = "PAID"

    return payment


def compute_signature(payload: dict, secret: str):
    """Compute HMAC signature for payload"""
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    return hmac.new(secret.encode(), raw.encode(), hashlib.sha256).hexdigest()


def verify_signature(payload: dict, signature: str, secret: str):
    """Verify HMAC signature"""
    expected = compute_signature(payload, secret)
    print("RAW JSON:", json.dumps(payload, separators=(",", ":"), sort_keys=True))
    print("SIGNATURE:", signature)
    return hmac.compare_digest(expected, signature)

    


def refund_payment(order_id, payment_id, amount):
    """Create a refund for a payment"""
    refund_id = f"rfnd_{uuid.uuid4().hex[:10]}"

    refund = {
        "table_name": "pg_refund",
        "order_id": order_id,
        "payment_id": payment_id,
        "amount": amount,
        "status": "COMPLETED",
        "created_at": datetime.now().isoformat()
    }

    order = get_order(order_id)
    if order:
        order["status"] = "REFUNDED"

    PAYMENT_GATEWAY_DB[refund_id] = refund
    return refund_id, refund
