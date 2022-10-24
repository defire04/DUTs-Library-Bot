import threading
import random;
from time import sleep


def test ():
    delay = random.randint(1, 4)
    sleep(delay)
    print('working ' + str(delay))
def finish ():
    print('finish')
    





def run_one_by_one (func1, func2, finish):
    func1()
    func2()
    finish()

class Threader:
    def __init__ (self, threads_count):
        self.threads_count = threads_count
        self.currnet_running_count = 0
        self.tasks = []
    def add_task (self, func, callback):
        self.tasks.append( [func, callback] )
        if self.currnet_running_count < self.threads_count:
            self.run_new_task()
    
    def run_new_task (self):
        if len(self.tasks):
            task = self.tasks.pop(0)
            thread = threading.Thread(target=run_one_by_one, args=(task[0], task[1], self.on_finish))
            thread.start()
            self.currnet_running_count += 1
    def on_finish (self):
        self.currnet_running_count -= 1
        if self.currnet_running_count < self.threads_count:
            self.run_new_task()




threader = Threader(100)
for i in range(1, 100):
    threader.add_task(test, finish)
