from langchain.tools import tool

@tool
def get_flight(flight_number : str) -> str:
    '''
    Use this tool to get the flight details when user requested for flight details
    '''
    import requests,json
    url=f'http://127.0.0.1:5000/api/flight/{flight_number}'
    val=requests.get(url)
    if val.status_code not in (200,201):
        return "error while fetching the flight details"
    return json.dumps(val.json())

@tool
def validate_flight(flight_number : str) ->str:
    '''
    Use this tool to get the flight details are vaild or not
    '''
    import requests,json
    url=f'http://127.0.0.1:5000/api/flight/'
    payload={
        'flight_number' : flight_number
    }
    val=requests.post(url,json=payload)
    if val.status_code not in (200,201):
        return "error while fetching the flight details"
    return json.dumps(val.json())

@tool
def flight_depart(flight_number : str) -> str:
    '''
    Use this tool to get the flight depart
    '''
    import requests,json
    url=f'http://127.0.0.1:5000/api/depart/{flight_number}'
    val=requests.get(url)
    if val.status_code not in (200,201):
        return "error while fetching the flight details"
    return json.dumps(val.json())