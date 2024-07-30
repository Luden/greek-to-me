class ProgressCounter:
    def __init__(self, name):
        self.total = 0
        self.current = 0
        self.log_id = name
        self.report_every = 100

    def reset(self, total):
        self.current = 0
        self.total = total

    def increment_and_report(self):
        self.current += 1
        if self.current % self.report_every == 0:
            self.print_progress()

    def print_progress(self):
        print(f'{self.log_id}: {self.current} / {self.total}')

