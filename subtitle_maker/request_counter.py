import time

_global_requests_current_minute = 0
_global_requests_current_ts = 0
_global_wait_started = False


class ProgressCounter:
    def __init__(self, name):
        self.total = 0
        self.current_requests = 0
        self.log_id = name
        self.report_every = 100
        self.limit_per_minute = 100

    def reset(self, total, limit_per_minute):
        self.current_requests = 0
        self.total = total
        self.limit_per_minute = limit_per_minute
        global _global_requests_current_minute
        _global_requests_current_minute = 0
        global _global_requests_current_ts
        _global_requests_current_ts = time.time()
        global _global_wait_started
        _global_wait_started = False

    def wait_for_limit(self):
        global _global_requests_current_minute
        global _global_requests_current_ts
        global _global_wait_started
        if _global_requests_current_minute > self.limit_per_minute:
            sleep_time = 60 - (time.time() - _global_requests_current_ts)
            if not _global_wait_started:
                _global_wait_started = True
                print(f'Waiting for ChatGPT rate limit to reset {int(sleep_time)}s')
            time.sleep(sleep_time)
            if _global_requests_current_minute > self.limit_per_minute:
                _global_requests_current_minute = 0
                _global_requests_current_ts = time.time()
                _global_wait_started = False
        _global_requests_current_minute += 1
        self.current_requests += 1
        if self.current_requests % self.report_every == 0:
            self.print_progress()

    def print_progress(self):
        print(f'{self.log_id}: {self.current_requests} / {self.total}')

