from multiprocessing import Process
from multiprocessing import Pool
def worker(num):
    print("there are",num,"workers")

def square(num):
    return num*num

if __name__ =="__main__":

    p1=Process(target=worker,args=(5,))
    p1.start()
    p1.join()

    p2=Process(target=worker,args=(3,))
    p2.start()
    p2.join()

    p3=Process(target=worker,args=(2,))
    p4=Process(target=worker,args=(4,))
    p3.start()
    p4.start()
    p3.join()
    p4.join()

    print("all processes have finished execution")
    print("\n")
    print("Using Process Pooling")

    with Pool(2) as pool:
        result=pool.map(square,[2,4,6,8])
        print(result)


