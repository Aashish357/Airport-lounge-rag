Lounge = {
    "LNG001": {
        "id": "LNG001",
        "name": "Platinum Business Lounge",
        "airport_code": "DEL",
        "capacity": 80,
        "occupancy": 55,
        "created_at": "2025-10-01T10:30:00Z"
    },
    "LNG002": {
        "id": "LNG002",
        "name": "SkyElite International Lounge",
        "airport_code": "DXB",
        "capacity": 120,
        "occupancy": 120,
        "created_at": "2025-09-15T08:15:00Z"
    },
    "LNG003": {
        "id": "LNG003",
        "name": "Aurora Premium Lounge",
        "airport_code": "LHR",
        "capacity": 60,
        "occupancy": 42,
        "created_at": "2025-11-20T06:45:00Z"
    }
}
Lounge_session = {
    "SES1001": {
        "id": "SES1001",
        "lounge_id": "LNG001",
        "user_id": "USR001",
        "status": "ACTIVE",
        "checkin_time": "2026-01-20T07:40:00Z",
        "exit_time": None
    },
    "SES1002": {
        "id": "SES1002",
        "lounge_id": "LNG002",
        "user_id": "USR002",
        "status": "EXITED",
        "checkin_time": "2026-01-20T05:10:00Z",
        "exit_time": "2026-01-20T06:45:00Z"
    },
    "SES1003": {
        "id": "SES1003",
        "lounge_id": "LNG001",
        "user_id": "USR003",
        "status": "ACTIVE",
        "checkin_time": "2026-01-20T08:05:00Z",
        "exit_time": None
    }
}
Waitlist = {
    "WL001": {
        "id": "WL001",
        "lounge_id": "LNG002",
        "user_id": "USR004",
        "status": "WAITING",
        "created_at": "2026-01-20T07:55:00Z",
        "promoted_at": None
    },
    "WL002": {
        "id": "WL002",
        "lounge_id": "LNG002",
        "user_id": "USR005",
        "status": "PROMOTED",
        "created_at": "2026-01-20T06:20:00Z",
        "promoted_at": "2026-01-20T07:10:00Z"
    },
    "WL003": {
        "id": "WL003",
        "lounge_id": "LNG003",
        "user_id": "USR006",
        "status": "EXPIRED",
        "created_at": "2026-01-19T23:50:00Z",
        "promoted_at": None
    }
}
Lounge_audit = {
    1: {
        "id": 1,
        "lounge_id": "LNG001",
        "user_id": "USR001",
        "action": "CHECKIN",
        "details": "User checked into lounge",
        "timestamp": "2026-01-20T07:40:00Z"
    },
    2: {
        "id": 2,
        "lounge_id": "LNG002",
        "user_id": "USR002",
        "action": "EXIT",
        "details": "User exited lounge",
        "timestamp": "2026-01-20T06:45:00Z"
    },
    3: {
        "id": 3,
        "lounge_id": "LNG002",
        "user_id": "SYSTEM",
        "action": "WAITLIST_PROMOTION",
        "details": "User promoted from waitlist",
        "timestamp": "2026-01-20T07:10:00Z"
    }
}
