from langchain.tools import tool
@tool
def get_lounge_details(lounge_id: str) -> str:
    '''
    Use this tool to get lounge details when user provide their lounge_id
    '''
    import requests,json
    url=f'http://127.0.0.1:5000/lounge/{lounge_id}'
    val=requests.get(url)
    if val.status_code not in (200, 201):
        return {
            "error": "Failed to create lounge",
            "status_code": val.status_code,
            "response_text": val.text
        }

    return json.dumps(val.json())      
@tool
def get_sessions(lounge_id : str) -> str:
    '''
    Use this tool to get the details of sessions when user provide their lounge_id and asked for session details
    '''
    import requests
    url=f'http://127.0.0.1:5000/lounge/{lounge_id}/sessions'
    val=requests.get(url)
    if val.status_code not in (200, 201):
        return {
            "error": "Failed to create lounge",
            "status_code": val.status_code,
            "response_text": val.text
        }

    return val.json()
    
@tool 
def lounge_checkin(lounge_id: str,user_id: str) -> str:
    '''
    use this tool to checkin into the lounge
    '''
    import requests,json
    payload={
        "lounge_id":lounge_id,
        "user_id":user_id
    }
    response = requests.post(
    "http://127.0.0.1:5000/lounge/checkin",
    json=payload
    )
    if response.status_code not in (200, 201):
        return {
            "error": "Failed to create lounge",
            "status_code": response.status_code,
            "response_text": response.text
        }
    return json.dumps(response.json())
    
@tool 
def lounge_checkout(session_id: str) -> str:
    '''
    use this tool to checkout from the lounge
    '''
    import requests,json
    payload={
      "session_id": session_id
    }
    response = requests.post(
    "http://127.0.0.1:5000/lounge/checkout",
    json=payload
    )
    if response.status_code not in (200, 201):
        return json.dumps({
            "error": "Failed to create lounge",
            "status_code": response.status_code,
            "response_text": response.text
        })
    return response.json()
@tool 
def lounge_waitlist(lounge_id: str,user_id: str) -> str:
    '''
    use this tool to see waitlist in lounge
    '''
    import requests,json
    payload={
        "lounge_id":lounge_id,
        "user_id":user_id
    }
    response = requests.post(
    "http://127.0.0.1:5000/lounge/waitlist",
    json=payload
    )
    if response.status_code not in (200, 201):
        return {
            "error": "Failed to create lounge",
            "status_code": response.status_code,
            "response_text": response.text
        }
    return json.dumps(response.json())
@tool 
def promote_waitlisted_user(lounge_id: str) -> str:
    '''
    use this tool to Promote first WAITING user from lounge waitlist
    '''
    import requests
    payload={
        "lounge_id":lounge_id
    }
    url=f'http://127.0.0.1:5000/lounge/{lounge_id}/promote'
    response = requests.post(
    url
    )
    if response.status_code not in (200, 201):
        return {
            "error": "Failed to create lounge",
            "status_code": response.status_code,
            "response_text": response.text
        }
    return response.json()