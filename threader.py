import threading
import random;
from time import sleep





def run_one_by_one (func1, func2, finish, link):
    result1 = func1()
    func2(link)
    finish()

class Threader:
    def __init__ (self, threads_count):
        self.threads_count = threads_count
        self.currnet_running_count = 0
        self.tasks = []
    def add_task (self, func, callback, link):
        self.tasks.append( [func, callback, link] )
        if self.currnet_running_count < self.threads_count:
            self.run_new_task()
    
    def run_new_task (self):
        if len(self.tasks):
            task = self.tasks.pop(0)
            self.currnet_running_count += 1
            thread = threading.Thread(target=run_one_by_one, args=(task[0], task[1], self.on_finish, task[2]))
            thread.start()
    def on_finish (self):
        self.currnet_running_count -= 1
        if self.currnet_running_count < self.threads_count:
            self.run_new_task()




