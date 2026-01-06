from abc import ABC, abstractmethod
from datetime import datetime, timedelta

THRESHOLD = 5


class PaymentGateway(ABC):
    def __init__(self, id: str, name: str, load: int):
        self.id = id
        self.name = name
        self.load = load
        self.accum = load
        self.is_disabled = False
        self.failures = []
        self.total_ops = 0
        self.success_rate = 100

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_accum(self):
        return self.accum

    def get_load(self):
        return self.load

    def choose(self):
        self.accum -= 100

    def add_load(self):
        self.accum += self.load

    def enable(self):
        self.is_disabled = False

    def disable(self):
        self.is_disabled = True

    def get_success_rate(self):
        return self.success_rate

    def compute_success_rate(self):
        # keeping success rate as 100 for first 2 transactions since gateway might work perfectly inspite of initial failures
        if self.total_ops > 2:
            self.success_rate = (1 - len(self.failures)) / self.total_ops
        else:
            self.success_rate = 100

    def check_failures(self):
        fifteen_mins_ago = datetime.now() - timedelta(minutes=15)
        failures_fifteen_mins_ago = list(
            filter(lambda item: item > fifteen_mins_ago, self.failures)
        )
        if len(failures_fifteen_mins_ago) >= THRESHOLD:
            self.disable()

    def record_success(self):
        self.total_ops += 1
        self.compute_success_rate()

    def record_failure(self):
        self.total_ops += 1
        self.failures.append(datetime.now())
        self.compute_success_rate()
        self.check_failures()

    @abstractmethod
    def check_health(self) -> bool:
        pass

    @abstractmethod
    def initiate_transaction(self, payload: dict) -> str:
        pass
