import json, hmac, hashlib
'''Simple script to compute HMAC signature for a JSON payload'''
def compute_signature(payload: dict, secret: str):
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    return hmac.new(secret.encode(), raw.encode(), hashlib.sha256).hexdigest()

secret = "MY_SUPER_SECRET"  # same secret your server uses

payload = {
    "event": "test",
    "data": {"message": "hello"}
}

signature = compute_signature(payload, secret)
print("RAW JSON:", json.dumps(payload, separators=(",", ":"), sort_keys=True))
print("SIGNATURE:", signature)
'''RAW JSON: {"data":{"message":"hello"},"event":"test"}
SIGNATURE: b6e52836306102a50bee2ccb61a4f39de56a3bc107a2a44a9814d22a6ad1bd06       '''