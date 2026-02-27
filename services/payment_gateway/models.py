PAYMENT_GATEWAY_DB = {
    "ORDER_001": {
        "table_name": "pg_order",
        "user_id": "USR_100",
        "token_fee": 0,
        "lounge_fee": 500,
        "amount": 1500,
        "status": "CREATED",
        "created_at": "2024-01-20 10:30:00"
    },
    "ORDER_002": {
        "table_name": "pg_order",
        "user_id": "USR_101",
        "token_fee": 200,
        "lounge_fee": 1000,
        "amount": 2500,
        "status": "PAID",
        "created_at": "2024-01-20 11:15:00"
    },
    "PAY_001": {
        "table_name": "pg_payment",
        "order_id": "ORDER_001",
        "method": "UPI",
        "status": "AUTHORIZED",
        "gateway_ref": "GW_REF_12345",
        "created_at": "2024-01-20 10:31:00"
    },
    "PAY_002": {
        "table_name": "pg_payment",
        "order_id": "ORDER_002",
        "method": "CARD",
        "status": "CAPTURED",
        "gateway_ref": "GW_REF_12346",
        "created_at": "2024-01-20 11:16:00"
    },
    "REF_001": {
        "table_name": "pg_refund",
        "order_id": "ORDER_001",
        "payment_id": "PAY_001",
        "amount": 500,
        "status": "INITIATED",
        "created_at": "2024-01-20 12:00:00"
    },
    "REF_002": {
        "table_name": "pg_refund",
        "order_id": "ORDER_002",
        "payment_id": "PAY_002",
        "amount": 0,
        "status": "COMPLETED",
        "created_at": "2024-01-20 12:30:00"
    }
}