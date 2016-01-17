import os
import sys
import threading

class hello_thread(threading.Thread):
    def __init__(self, name, pl):
        threading.Thread.__init__(self)
        self.name = name
        self.counter = 0
        self.command = "none"
        self.lock = threading.Lock()
        self.printLock = pl
        
    def run(self):
        pl.acquire()
        print(self.name + " is running")
        sys.stdout.flush()
        pl.release()
        
        while(self.command != "stop"):
            if self.command=="step":
                self.step()
        pl.acquire()
        print(self.name + " is completed")
        sys.stdout.flush()
        pl.release()
        
    def step(self):
        self.lock.acquire()
        self.counter = self.counter +1

        pl.acquire()
        print(self.name + ":")
        print(self.counter)
        sys.stdout.flush()
        pl.release()
        
        self.command = "none"
        self.lock.release()

if (__name__ == "__main__"):
    pl = threading.Lock()
    t1 = hello_thread("One", pl)
    t2 = hello_thread("Two", pl)
    

    t1.start()
    t2.start()
    while (t1.counter + t2.counter<20):
        if t1.lock.acquire(False):
            t1.command="step"
            t1.lock.release()
    
        if t2.lock.acquire(False):
            t2.command="step"
            t2.lock.release()
    
    t1.lock.acquire(True)
    t1.command="stop"
    t1.lock.release()
    
    t2.lock.acquire(True)
    t2.command="stop"
    t2.lock.release()
