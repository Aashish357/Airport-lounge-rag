from datetime import datetime
from .models import Lounge, Lounge_session, Waitlist, Lounge_audit


def get_lounge_by_id(lounge_id):
    return Lounge.get(lounge_id)


def get_lounge_sessions(lounge_id, status=None):
    sessions = []
    for session in Lounge_session.values():
        if session["lounge_id"] == lounge_id:
            if status:
                if session["status"] == status:
                    sessions.append(session)
            else:
                sessions.append(session)
    return sessions


def is_lounge_full(lounge_id):
    lounge = get_lounge_by_id(lounge_id)
    if not lounge:
        return None
    return lounge["occupancy"] >= lounge["capacity"]


def checkin_user(lounge_id, user_id):
    lounge = get_lounge_by_id(lounge_id)
    if not lounge:
        return False, "Lounge not found"

    if lounge["occupancy"] >= lounge["capacity"]:
        return False, "Lounge is full"

    session_id = f"SES{1000 + len(Lounge_session) + 1}"
    Lounge_session[session_id] = {
        "id": session_id,
        "lounge_id": lounge_id,
        "user_id": user_id,
        "status": "ACTIVE",
        "checkin_time": datetime.utcnow().isoformat() + "Z",
        "exit_time": None
    }

    lounge["occupancy"] += 1
    add_audit_log(lounge_id, user_id, "CHECKIN", "User checked into lounge")

    return True, Lounge_session[session_id]


def checkout_user(session_id):
    session = Lounge_session.get(session_id)
    if not session or session["status"] != "ACTIVE":
        return False, "Invalid or inactive session"

    session["status"] = "EXITED"
    session["exit_time"] = datetime.utcnow().isoformat() + "Z"

    lounge = get_lounge_by_id(session["lounge_id"])
    if lounge:
        lounge["occupancy"] -= 1

    add_audit_log(session["lounge_id"], session["user_id"], "EXIT", "User exited lounge")

    return True, session


def add_to_waitlist(lounge_id, user_id):
    waitlist_id = f"WL{100 + len(Waitlist) + 1}"
    Waitlist[waitlist_id] = {
        "id": waitlist_id,
        "lounge_id": lounge_id,
        "user_id": user_id,
        "status": "WAITING",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "promoted_at": None
    }
    return Waitlist[waitlist_id]


def promote_waitlist(lounge_id):
    for wl in Waitlist.values():
        if wl["lounge_id"] == lounge_id and wl["status"] == "WAITING":
            wl["status"] = "PROMOTED"
            wl["promoted_at"] = datetime.utcnow().isoformat() + "Z"
            add_audit_log(lounge_id, wl["user_id"], "WAITLIST_PROMOTION", "User promoted from waitlist")
            return wl
    return None


def add_audit_log(lounge_id, user_id, action, details):
    audit_id = len(Lounge_audit) + 1
    Lounge_audit[audit_id] = {
        "id": audit_id,
        "lounge_id": lounge_id,
        "user_id": user_id,
        "action": action,
        "details": details,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
