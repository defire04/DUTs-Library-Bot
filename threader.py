import threading
import random;
from time import sleep





def run_one_by_one (func1, func2, finish):
    result1 = func1()
    func2(result1)
    finish()

class Task: 
    def __init__ (self, taskFunction, callback, name = 'unnamed_task'):
        self.function = taskFunction
        self.callback = callback
        self.name = name

class Threader:
    def __init__ (self, threads_count):
        self.threads_count = threads_count
        self.currnet_running_count = 0
        self.tasks = []
        self.total = 0
    def add_task (self, func, callback, title):
        print('Added task ' + str(title))
        self.tasks.append( Task(func, callback) )
        if self.currnet_running_count < self.threads_count:
            self.run_new_task()
    
    def run_new_task (self):
        if len(self.tasks):
            task = self.tasks.pop(0)
            self.currnet_running_count += 1
            thread = threading.Thread(target=run_one_by_one, args=(task.function, task.callback, self.on_finish))
            thread.start()
    def on_finish (self):
        self.currnet_running_count -= 1
        self.total += 1
        print(str((self.total / 1942) * 100) + '%\t' + str(self.total))
        if self.currnet_running_count < self.threads_count:
            self.run_new_task()




