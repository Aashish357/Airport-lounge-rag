import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PAYMENT_GATEWAY_KEY = os.getenv("PAYMENT_GATEWAY_KEY", "")
    PAYMENT_GATEWAY_SECRET = os.getenv("PAYMENT_GATEWAY_SECRET", "")
