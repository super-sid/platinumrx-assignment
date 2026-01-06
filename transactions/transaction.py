from datetime import datetime
from enum import Enum
from uuid import uuid4


class Status(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class Transaction:
    def __init__(self, data):
        self.id = uuid4()
        self.order_id = data.get("order_id")
        self.status = Status.PENDING.value
        self.amount = data.get("amount")
        self.currency = data.get("currency")
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        payment_instrument = data.get("payment_instrument")
        self.currency = data.get("payment_instrument").get("currency")
        self.payment_instrument = payment_instrument
        self.gateway_info = None
        self.failure_reason = None

    def update_status(self, status):
        self.status = status
        self.updated_at = datetime.now().isoformat()

    def add_gateway_details(self, gateway):
        self.gateway_info = gateway
        self.updated_at = datetime.now().isoformat()

    def add_failure_reason(self, reason: str):
        self.failure_reason = reason
        self.updated_at = datetime.now().isoformat()
