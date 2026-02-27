from langchain.tools import tool

@tool
def check_loungekey_exists(loungekey_number: str) -> str:
    '''
    Use this tool to check weather lounge_key exists or not
    '''
    import requests
    payload={
        "loungekey_number": loungekey_number
    }
    url=f'http://127.0.0.1:5000/loungekey'
    val=requests.post(url=url,json=payload)
    if val.status_code not in (200, 201):
        return {
            "status_code": val.status_code,
            "response_text": val.text
        }
    return val.json()
@tool
def validate_bin(bin_number : str) -> str:
    '''
    Use this tool get the card details by using the bin number
    '''
    import requests
    payload={
        "bin": bin_number
    }
    url='http://127.0.0.1:5000/bin_validation'
    val=requests.post(url=url,json=payload)
    if val.status_code not in (200, 201):
        return {
            "status_code": val.status_code,
            "response_text": val.text
        }
    return val.json()
@tool
def validate_card(card_number: str,expiry_month: str,expiry_year: str,cvv: str) -> str:
    '''
    Use this tool to vaildate the card details
    '''
    import requests
    payload={
        "card_number": card_number,
        "expiry_month": expiry_month,
        "expiry_year": expiry_year,
        "cvv": cvv
    }
    url='http://127.0.0.1:5000/validate'
    val=requests.post(url=url,json=payload)
    if val.status_code not in (200, 201):
        return {
            "status_code": val.status_code,
            "response_text": val.text
        }
    
