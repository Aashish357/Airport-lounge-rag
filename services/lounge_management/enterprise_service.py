import uuid
from datetime import datetime
from common.db import db
from .models import Lounge, Lounge_session, Waitlist, Lounge_audit

def audit(lounge_id, user_id, action, details=""):
    db.session.add(Lounge_audit(
        lounge_id=lounge_id,
        user_id=user_id,
        action=action,
        details=details
    ))
    db.session.commit()

def join_waitlist(lounge_id, user_id):
    entry = Waitlist(
        id=f"wl_{uuid.uuid4().hex[:10]}",
        lounge_id=lounge_id,
        user_id=user_id,
        status="WAITING"
    )
    db.session.add(entry)
    db.session.commit()
    audit(lounge_id, user_id, "WAITLIST_JOIN", entry.id)
    return entry

def promote_waitlist_if_possible(Lounge):
    # promote first waiting user if seat available
    if Lounge.occupancy >= Lounge.capacity:
        return None

    entry = (Waitlist.query
             .filter_by(lounge_id=Lounge.id, status="WAITING")
             .order_by(Waitlist.created_at.asc())
             .first())

    if not entry:
        return None

    Lounge.occupancy += 1
    entry.status = "PROMOTED"
    entry.promoted_at = datetime.utcnow()

    session = Lounge_session(
        id=f"sess_{uuid.uuid4().hex[:10]}",
        lounge_id=Lounge.id,
        user_id=entry.user_id,
        status="ACTIVE"
    )
    db.session.add(session)
    db.session.commit()

    audit(Lounge.id, entry.user_id, "WAITLIST_PROMOTED", session.id)
    return session

def checkin(lounge_id, user_id):
    lounge = Lounge.query.get(lounge_id)
    if not lounge:
        return None, "Invalid lounge_id"

    if lounge.occupancy >= lounge.capacity:
        entry = join_waitlist(lounge_id, user_id)
        return {"waitlist_id": entry.id, "status": "WAITLISTED"}, None

    lounge.occupancy += 1
    session = Lounge_session(
        id=f"sess_{uuid.uuid4().hex[:10]}",
        lounge_id=lounge_id,
        user_id=user_id,
        status="ACTIVE"
    )
    db.session.add(session)
    db.session.commit()

    audit(lounge_id, user_id, "CHECKIN", session.id)
    return {"session_id": session.id, "status": "ACTIVE"}, None

def exit_session(session_id):
    session = Lounge_session.query.get(session_id)
    if not session:
        return None, "Invalid session_id"
    if session.status != "ACTIVE":
        return None, "Session already closed"

    lounge = Lounge.query.get(session.lounge_id)
    if lounge and lounge.occupancy > 0:
        lounge.occupancy -= 1

    session.status = "EXITED"
    session.exit_time = datetime.utcnow()
    db.session.commit()

    audit(session.lounge_id, session.user_id, "EXIT", session.id)

    # auto promote waitlist
    if lounge:
        promote_waitlist_if_possible(lounge)

    return {"session_id": session.id, "status": "EXITED"}, None
