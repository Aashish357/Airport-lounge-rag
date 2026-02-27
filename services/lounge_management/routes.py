from flask import Blueprint, request, jsonify
from .service import *

lounge_bp = Blueprint("lounge", __name__)


@lounge_bp.route("/lounge/<lounge_id>", methods=["GET"])
def get_lounge(lounge_id):
    '''
    Get lounge details by lounge ID

    Request URL: /lounge/LNG001
    '''
    lounge = get_lounge_by_id(lounge_id)
    if not lounge:
        return jsonify({"error": "Lounge not found"}), 404
    return jsonify(lounge), 200


@lounge_bp.route("/lounge/<lounge_id>/sessions", methods=["GET"])
def get_sessions(lounge_id):
    '''
    Get lounge sessions (ACTIVE / EXITED)

    Method: GET
    URL:
      /lounge/LNG001/sessions
      /lounge/LNG001/sessions?status=ACTIVE
    '''
    status = request.args.get("status")
    sessions = get_lounge_sessions(lounge_id, status)
    return jsonify({"sessions": sessions}), 200


@lounge_bp.route("/lounge/checkin", methods=["POST"])
def lounge_checkin():
    '''
    Check if a Loung checkin membership exists in database
    Request Body:
    {
      "lounge_id": "LNG001",
      "user_id": "USR010"
    }
    '''
    data = request.get_json()
    lounge_id = data.get("lounge_id")
    user_id = data.get("user_id")

    if not lounge_id or not user_id:
        return jsonify({"error": "lounge_id and user_id are required"}), 400

    success, result = checkin_user(lounge_id, user_id)
    if not success:
        return jsonify({"error": result}), 400

    return jsonify({
        "message": "User checked in successfully",
        "session": result
    }), 200


@lounge_bp.route("/lounge/checkout", methods=["POST"])
def lounge_checkout():
    '''
    Checkout a user from a lounge

    Method: POST
    URL:
      /lounge/checkout

    Request Body:
    {
      "session_id": "SES1001"
    }
    '''
    data = request.get_json()
    session_id = data.get("session_id")

    if not session_id:
        return jsonify({"error": "session_id is required"}), 400

    success, result = checkout_user(session_id)
    if not success:
        return jsonify({"error": result}), 400

    return jsonify({
        "message": "User checked out successfully",
        "session": result
    }), 200


@lounge_bp.route("/lounge/waitlist", methods=["POST"])
def lounge_waitlist():
    '''
    Add user to lounge waitlist

    Method: POST
    URL:
      /lounge/waitlist

    Request Body:
    {
      "lounge_id": "LNG002",
      "user_id": "USR011"
    }
    '''
    data = request.get_json()
    lounge_id = data.get("lounge_id")
    user_id = data.get("user_id")

    if not lounge_id or not user_id:
        return jsonify({"error": "lounge_id and user_id are required"}), 400

    entry = add_to_waitlist(lounge_id, user_id)
    return jsonify({
        "message": "User added to waitlist",
        "waitlist": entry
    }), 200


@lounge_bp.route("/lounge/<lounge_id>/promote", methods=["POST"])
def promote_waitlisted_user(lounge_id):
    '''
    Promote first WAITING user from lounge waitlist

    Method: POST
    URL:
      /lounge/LNG002/promote
    '''
    promoted = promote_waitlist(lounge_id)
    if not promoted:
        return jsonify({"message": "No users to promote"}), 200

    return jsonify({
        "message": "User promoted from waitlist",
        "details": promoted
    }), 200
