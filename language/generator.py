import time 

def yield_abc():
    for ch in "ABC":
        time.sleep(1)
        yield ch 


for ch in yield_abc():
    print(ch)