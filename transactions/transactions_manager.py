from typing import Dict

from transactions.transaction import Status, Transaction


class TransactionsManager:
    _instance = None

    def __init__(self):
        self._initialized = True
        self._records: Dict[str, Transaction] = {}

    @classmethod
    def get_instance(cls):
        return cls()

    def add(self, data: dict):
        transaction_data = Transaction(data)
        self._records[transaction_data.order_id] = transaction_data

    def update_status(self, id, status: str, reason: str = ""):
        curr_transaction = self._records[id]
        if status == "success":
            curr_transaction.update_status(Status.SUCCESS.value)
        else:
            curr_transaction.update_status(Status.FAILURE.value)
            curr_transaction.add_failure_reason(reason)

    def add_payment_gateway_info(self, id, gateway_info: str):
        curr_transaction = self._records[id]
        curr_transaction.add_gateway_details(gateway_info)

    def get_records(self):
        return self._records

    def get_record(self, order_id: str):
        return self._records[order_id]
