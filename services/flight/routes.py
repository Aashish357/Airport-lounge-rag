from flask import Blueprint,request,jsonify
from .service import get_flight_info


flight_bp = Blueprint("flight", __name__, url_prefix="/api")

@flight_bp.route('/flight',methods=["POST"])
def validate_flight():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success":False,
                "error":"Flight data not found, enter flight data"
            }), 400
        
        flight_number = data.get('flight_number','').strip()

        if not flight_number:
            return jsonify({
                "success":False,
                "error":"Flight number not found"
            }), 400
        
        flight_info = get_flight_info(flight_number)

        if not flight_info:
            return jsonify({
                "success":False,
                "error":"unable to fetch Flight details"
            }), 400
        
        return jsonify({
                "success": True,
                **flight_info
                }
            ), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

        
@flight_bp.route("/flight/<flight_number>", methods=['GET'])
def get_flight(flight_number:str):
    try:
        # Get flight information
        flight_info = get_flight_info(flight_number)
        
        if not flight_info:
            return jsonify({
                "success": False,
                "error": f"Flight {flight_number.upper()} not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": {
                "flight_number": flight_number.upper(),
                **flight_info
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500
    
@flight_bp.route('/depart/<flight_number>',methods=['GET'])
def flight_depart(flight_number:str):
    try:
        # Get flight information
        flight_info = get_flight_info(flight_number)#flight_number
        
        if not flight_info:
            return jsonify({
                "success": False,
                "error": f"Flight {flight_number.upper()} not found"
            }), 404
        
        # Determine status message
        is_delayed = flight_info.get('delay_status', False)
        delay_time = flight_info.get('delay_time', '0')
        
        if is_delayed:
            status_message = f"Delayed by {delay_time} minutes"
        else:
            status_message = "On time"
        
        return jsonify({
            "success": True,
            "data": {
                "flight_number": flight_number.upper(),
                "is_delayed": is_delayed,
                "delay_time": delay_time,
                "departure_time": flight_info.get('departure_time'),
                "departure_airport": flight_info.get('departure_airport'),
                "status_message": status_message
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@flight_bp.route('/depart',methods=['POST'])
def get_flight_depart():
    try :
        data = request.get_json()

        if not data:
            return jsonify({
                "success":False,
                "error":"Flight data not found, enter flight data"
            }), 404
        
        flight_number = data.get('flight_number','').strip()

        flight_info = get_flight_info(flight_number)#flight_number
            
        if not flight_info:
            return jsonify({
                "success": False,
                "error": f"Flight {flight_number.upper()} not found"
            }), 404
        
        # Determine status message
        is_delayed = flight_info.get('delay_status', False)
        delay_time = flight_info.get('delay_time', '0')
        
        if is_delayed:
            status_message = f"Delayed by {delay_time} minutes"
        else:
            status_message = "On time"
        
        return jsonify({
            "success": True,
            "data": {
                "flight_number": flight_number.upper(),
                "is_delayed": is_delayed,
                "delay_time": delay_time,
                "departure_time": flight_info.get('departure_time'),
                "departure_airport": flight_info.get('departure_airport'),
                "status_message": status_message
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@flight_bp.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@flight_bp.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 errors"""
    return jsonify({
        "success": False,
        "error": "Method not allowed"
    }), 405