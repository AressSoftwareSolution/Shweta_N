import threading
import time

print("function based threading example")
def thread_func(name):
    print(f"The Thread {name} is starting")
    time.sleep(2)
    print(f"The Thread {name} is ending")


t1=threading.Thread(target=thread_func, args=("Thread-1",))
t2=threading.Thread(target=thread_func, args=("Thread-2",))
t1.start()
t2.start()
t1.join()
t2.join()
print("All threads have finished execution")


print("Class based Threading example")

class thread_class(threading.Thread):
    def run(self):
        print("the thread is starting")
        time.sleep(2)
        print("the thread is ending")
    
t3=thread_class()
t3.start()
t3.join()

print("Thread Pooling")
from concurrent.futures import ThreadPoolExecutor

def thread_pool(name):
    print(f"The Thread {name} is starting")
    time.sleep(2)
    print(f"The Thread {name} is ending")

with ThreadPoolExecutor(max_workers=2) as e:
    e.submit(thread_pool,"t1")
    e.submit(thread_pool,"t2")
