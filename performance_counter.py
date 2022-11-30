import time


class PerformanceCounter:
    def __init__(self):
        self.total = 0
        self.start_time = 0

    def start(self):
        self.time_start = time.time()

    def end(self):
        self.total += time.time() - self.time_start

    def printResult(self):
        print(str(self.total / 60) + 's')
