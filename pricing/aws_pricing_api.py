
import requests

def get_live_price(instance_type):
    fallback = {
        "t3.micro": 9,
        "t3.small": 18,
        "t3.medium": 36
    }

    return fallback.get(instance_type, 25)
