import threading
import time

def bucle1():
    for i in range(5):
        print(f"\rBucle 1: {i}")
        time.sleep(1)

def bucle2():
    for i in range(5):
        print(f"\rBucle 2: {i}")
        time.sleep(1)

t1 = threading.Thread(target=bucle1)
t2 = threading.Thread(target=bucle2)

t1.start()
t2.start()

t1.join()
t2.join()