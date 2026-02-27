from langchain.tools import tool

@tool
def api_get_order(order_id : str) -> str:
    '''
    Use this tool to check order status.
    '''
    import requests,json
    url=f'http://127.0.0.1:5000/payment/api/orders/{order_id}'
    val=requests.get(url)
    if val.status_code not in (200,201):
        return "error while fetching the order details"
    return json.dumps(val.json())

@tool
def api_create_order(user_id: str, token_fee: str,lounge_fee: str) ->str:
    '''
    Use this tool  when User confirms lounge booking or User clicks “Proceed to Pay” or You want an order_id
    '''
    import requests,json
    url=f'http://127.0.0.1:5000/payment/api/orders'
    payload={
        'user_id' : user_id,
        'token_fee':token_fee,
        'lounge_fee':lounge_fee
    }
    val=requests.post(url,json=payload)
    if val.status_code not in (200,201):
        return "error while creating the payment"
    return json.dumps(val.json())

@tool
def checkout(order_id : str) -> str:
    '''
    Use this tool to display amount, fees, order info or User is about to choose payment method
    '''
    import requests,json
    url=f'http://127.0.0.1:5000/payment/checkout/{order_id}'
    val=requests.get(url)
    if val.status_code not in (200,201):
        return "error while fetching order info"
    return json.dumps(val.json())