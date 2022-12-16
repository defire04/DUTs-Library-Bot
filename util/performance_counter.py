import time


class PerformanceCounter:
    def __init__(self):
        self.time_start = 0
        self.total = 0

    def start(self):
        self.time_start = time.time()

    def end(self):
        self.total += time.time() - self.time_start

    def printResult(self):
        print(("{:.3}".format((self.total % 3600) / 60) + ' min'))

