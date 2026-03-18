## Time decorators to measure the execution time of functions 
import time
def time_Req(func):
    def wrapper(*args, **kwargs):
        start_time=time.time()
        result=func(*args, **kwargs)
        end_time=time.time()
        print(f"Execution time: {end_time - start_time} seconds")
        return result
    return wrapper

@time_Req
def sum(n):
    total=0
    for i in range(n):
        total+=i
    return total

print(sum(253))