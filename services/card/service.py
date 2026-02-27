import hashlib
from .models import BIN_DATABASE,LOUNGEKEY_DATABASE
from datetime import datetime

def bin_hashing(card):
    card_num = card['card_number']
    merchant_key = "1234567899"
    salt= "23e2e3r4r4r3"
    url = "https://example.in/merchant"
    command="check_Bin"

    hash_string = f"{merchant_key}|{command}|{card_num}|{url}|{salt}"
    hash_value = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()
    return hash_value


def luhn_algorithm(card_number):
    """Validate card number using Luhn algorithm"""
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    # for testing #return True
    return checksum % 10 == 0
    
# issue is card domestic or international first check for domestic then international bank
def get_card_type(card_number):
    """Determine card type from BIN"""
    card_number = str(card_number)
    home_country = 'IN'
    # Check longest prefixes first (6 digits, then 4, then 2, then 1)
    for length in [6, 4, 3, 2, 1]:
        prefix = card_number[:length]
        if prefix in BIN_DATABASE:
            if BIN_DATABASE[prefix]['country'] == home_country:
                return BIN_DATABASE[prefix]
            else:
                return BIN_DATABASE[prefix]
    
    return None

def validate_expiry(expiry_month, expiry_year):
    """Validate expiry date"""
    try:
        month = int(expiry_month)
        year = int(expiry_year)
        
        if month < 1 or month > 12:
            return False, "Invalid month"
        
        # Handle 2-digit or 4-digit year
        if year < 100:
            year += 2000
        
        current_date = datetime.now()
        expiry_date = datetime(year, month, 1)
        
        if expiry_date < current_date:
            return False, "Card has expired"
        
        return True, "Valid expiry date"
    except (ValueError, TypeError):
        return False, "Invalid date format"

def validate_cvv(cvv, card_type):
    """Validate CVV/CVC"""
    cvv_str = str(cvv)
    
    # AMEX uses 4-digit CVV, others use 3-digit
    if card_type == 'AMEX':
        return len(cvv_str) == 4 and cvv_str.isdigit()
    else:
        return len(cvv_str) == 3 and cvv_str.isdigit()
