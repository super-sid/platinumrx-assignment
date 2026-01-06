import random

from payment_gateways.payment_gateway import PaymentGateway


class PayU(PaymentGateway):
    def __init__(self, api_key: str, load: int):
        self.name = "Pay U"
        self.accum = load
        self.id = "payu"
        self.load = load
        self.api_key = api_key
        self.is_disabled = False
        self.failures = []
        self.total_ops = 0
        self.success_rate = 100

    def check_health(self):
        random_number = random.randint(1, 100)
        return True if random_number < 95 else False

    def initiate_transaction(self, payload: dict):
        link = "https://dummylink2.com"
        return link
