from flask import Blueprint,request,jsonify
from .service import *


card_bp = Blueprint('card',__name__)


@card_bp.route('/loungekey', methods=['POST'])
def check_loungekey_exists():
    """
    Check if a LoungeKey membership exists in database
    
    Request Body:
    {
        "loungekey_number": "LK001234567890"
    }
    """
    try:
        data = request.get_json()
        loungekey_number = data.get('loungekey_number', '').strip().upper()
        
        if not loungekey_number:
            return jsonify({
                'error': 'LoungeKey number is required'
            }), 400
        
        # Validate format (should start with LK and be 14 characters)
        if not loungekey_number.startswith('LK') or len(loungekey_number) != 14:
            return jsonify({
                'exists': False,
                'loungekey_number': loungekey_number,
                'error': 'Invalid LoungeKey format. Must start with LK and be 14 characters long'
            }), 400
        
        # Check if membership exists in database
        exists = loungekey_number in LOUNGEKEY_DATABASE
        
        response = {
            'exists': exists,
            'loungekey_number': loungekey_number
        }
        
        if exists:
            member_info = LOUNGEKEY_DATABASE[loungekey_number]
            response['message'] = 'LoungeKey membership found in database'
            response['member_preview'] = {
                'member_name': member_info['member_name'],
                'membership_type': member_info['membership_type'],
                'status': member_info['status'],
                'tier': member_info['tier']
            }
        else:
            response['message'] = 'LoungeKey membership not found in database'
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@card_bp.route('/bin_validation', methods=['POST'])
def validate_bin():
    """
    Validate BIN (Bank Identification Number) and return card details
    
    Request Body:
    {
        "bin": "453201"
    }
    
    or
    
    {
        "card_number": "4532015112830366"
    }
    """
    try:
        data = request.get_json()
        
        # Get BIN from either 'bin' or 'card_number' field
        bin_number = data.get('bin')
        if not bin_number:
            card_number = data.get('card_number', '').replace(' ', '').replace('-', '')
            if card_number:
                bin_number = card_number[:6]  # First 6 digits
        
        if not bin_number:
            return jsonify({
                'error': 'BIN or card_number is required'
            }), 400
        
        # Validate BIN format
        #bin_number = str(bin_number)
        if not bin_number.isdigit():
            return jsonify({
                'error': 'BIN must contain only digits'
            }), 400
        
        if len(bin_number) < 4 or len(bin_number) > 8:
            return jsonify({
                'error': 'BIN must be between 4 and 8 digits'
            }), 400
        
        # Get card information
        card_info = get_card_type(bin_number)
        
        response = {
            'bin': bin_number,
            'valid': card_info is not None
        }
        
        if card_info:
            response['card_brand'] = card_info['card_type']
            response['card_category'] = card_info['card_category']
            response['issuing_bank'] = card_info['bank']
            response['country'] = card_info['country']
            response['is_credit'] = 'CREDIT' in card_info['card_category']
            response['is_debit'] = 'DEBIT' in card_info['card_category']
            #response['hashed_bin'] = bin_hashing(bin_number)
        else:
            response['message'] = 'BIN not found in database'
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@card_bp.route('/validate',methods=['POST'])
def validate_card():
    """
    Validate complete card details
    
    Request Body:
    {
        "card_number": "4532015112830366",
        "expiry_month": "12",
        "expiry_year": "2025",
        "cvv": "123"
    }
    """
    try:
        data = request.get_json()
        
        # Extract and validate required fields
        card_number = data.get('card_number', '').replace(' ', '').replace('-', '')
        expiry_month = data.get('expiry_month')
        expiry_year = data.get('expiry_year')
        cvv = data.get('cvv')
        
        # Validation results
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Validate card number presence
        if not card_number:
            validation_results['valid'] = False
            validation_results['errors'].append('Card number is required')
            return jsonify(validation_results), 400
        
        # Validate card number format
        if not card_number.isdigit():
            validation_results['valid'] = False
            validation_results['errors'].append('Card number must contain only digits')
        
        # Validate card number length
        if len(card_number) < 13 or len(card_number) > 19:
            validation_results['valid'] = False
            validation_results['errors'].append('Card number must be between 13 and 19 digits')
        
        # Luhn algorithm check
        if card_number.isdigit() and not luhn_algorithm(card_number):
            validation_results['valid'] = False
            validation_results['errors'].append('Invalid card number (failed Luhn check)')
        
        # Get card type and bank information
        card_info = get_card_type(card_number)
        if card_info:
            validation_results['card_type'] = card_info['card_type']
            validation_results['card_category'] = card_info['card_category']
            validation_results['issuing_bank'] = card_info['bank']
            validation_results['country'] = card_info['country']
        else:
            validation_results['warnings'].append('Card type not recognized')
        
        # Validate expiry date
        if expiry_month and expiry_year:
            expiry_valid, expiry_message = validate_expiry(expiry_month, expiry_year)
            if not expiry_valid:
                validation_results['valid'] = False
                validation_results['errors'].append(expiry_message)
        else:
            validation_results['warnings'].append('Expiry date not provided')
        
        # Validate CVV
        if cvv:
            card_type = card_info['card_type'] if card_info else None
            if not validate_cvv(cvv, card_type):
                validation_results['valid'] = False
                validation_results['errors'].append('Invalid CVV format')
        else:
            validation_results['warnings'].append('CVV not provided')
        
        # Masked card number for response
        if len(card_number) >= 4:
            validation_results['masked_card'] = '*' * (len(card_number) - 4) + card_number[-4:]
        
        status_code = 200 if validation_results['valid'] else 400
        
        #hashing of the given card
        #validation_results["hashed_card"] =  card_hashing(card_number)

        return jsonify(validation_results), status_code
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
