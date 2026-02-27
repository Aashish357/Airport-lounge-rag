from flask import jsonify

def ok(data=None, message="Success"):
    return jsonify({
        "status": "success",
        "message": message,
        "data": data
    }), 200


def err(message="Error", code=400):
    return jsonify({
        "status": "error",
        "message": message
    }), code
