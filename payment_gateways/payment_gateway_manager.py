from typing import Dict

from constants import (
    MIN_SUCCESS_RATE,
    PAYU_API_KEY,
    PAYU_WEIGHT,
    RAZORPAY_API_KEY,
    RAZORPAY_WEIGHT,
    STRIPE_API_KEY,
    STRIPE_WEIGHT,
)
from payment_gateways.gateway_clients.payu import PayU
from payment_gateways.gateway_clients.razorpay import Razorpay
from payment_gateways.gateway_clients.stripe import Stripe
from payment_gateways.payment_gateway import PaymentGateway


class PaymentGatewayManager:
    def __init__(self):
        self._gateways: Dict[str, PaymentGateway] = {}

    def register_payment_gateway(self, gateway: PaymentGateway):
        self._gateways[gateway.id] = gateway

    def remove_gateway(self, gateway_id: str):
        del self._gateways[gateway_id]

    def choose_gateway(self) -> PaymentGateway:
        max_accum = -1
        chosen_gateway = None
        for key, gateway in self._gateways.items():
            print(vars(gateway), gateway.check_health())
            # check if disabled
            if gateway.is_disabled:
                continue
            # check health of the gateway
            if not gateway.check_health():
                continue
            # check success rate
            if gateway.get_success_rate() < MIN_SUCCESS_RATE:
                continue

            print("coming here")
            # logic for choosing the gateway
            if gateway.accum >= max_accum:
                max_accum = gateway.accum
                chosen_gateway = gateway
        if chosen_gateway:
            self._gateways[chosen_gateway.id].accum -= 100

            for _, gateway in self._gateways.items():
                self._gateways[gateway.id].accum += gateway.load
            return chosen_gateway

    def initialize_gateways(self):
        razorpay_obj = Razorpay(RAZORPAY_API_KEY, RAZORPAY_WEIGHT)
        payu_obj = PayU(PAYU_API_KEY, PAYU_WEIGHT)
        stripe_obj = Stripe(STRIPE_API_KEY, STRIPE_WEIGHT)
        self.register_payment_gateway(razorpay_obj)
        self.register_payment_gateway(payu_obj)
        self.register_payment_gateway(stripe_obj)

    def update_gateway_on_status(self, gateway_id: str, status: str):
        curr_gateway = self._gateways[gateway_id]
        if status == "success":
            curr_gateway.record_success()
        else:
            curr_gateway.record_failure()
