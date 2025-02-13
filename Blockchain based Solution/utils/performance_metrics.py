import time

class PerformanceMetrics:
    def __init__(self):
        self.metrics = {
            "registration_times": [],
            "login_times": [],
            "transaction_times": []
        }

    def track_registration_time(self, start_time):
        end_time = time.time()
        self.metrics["registration_times"].append(end_time - start_time)

    def track_login_time(self, start_time):
        end_time = time.time()
        self.metrics["login_times"].append(end_time - start_time)

    def track_transaction_time(self, start_time):
        end_time = time.time()
        self.metrics["transaction_times"].append(end_time - start_time)

    def get_metrics(self):
        return self.metrics