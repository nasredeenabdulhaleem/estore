import secrets
import requests
from django.conf import settings


def initializepay(email, total, ref):
    url = "https://api.paystack.co/transaction/initialize"

    headers = {
        "Authorization": "Bearer " + settings.PAYSTACK_SECRET_KEY,
        "Content-Type": "application/json",
    }

    body = {
        "email": email,
        "amount": total * 100,
        "reference": ref,
        "currency": "NGN",
    }

    get_response = requests.request("POST", url, headers=headers, json=body)
    response = get_response.json()
    return response


# res = initializepay("nabdulhaleem09@gmail.com", 40000, "6tr6rwu6et66db")
# print(res)
