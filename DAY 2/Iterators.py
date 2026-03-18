List=[1,2,3,4,5]

iterator=iter(List)
print(iterator)
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))
# print(next(iterator)) # This will raise StopIteration error as there are no more elements in the list.

class Iterator:
    def __init__(self,data):
        self.data=data
        self.index=0

    def __iter__(self):
        return self
    def __next__(self):
        if self.index< len(self.data):
            res=self.data[self.index]
            self.index+=1
            return res
        else:
            raise StopIteration

lists=[10,20,30,40,50]
iterator=Iterator(lists)
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))
# print(next(iterator)) # This will raise StopIteration error as there are no more elements in
print("For Loop Execution Started\n")
for i in iterator:
    print(i)
 ## The above for loop will not print anything as the iterator is already exhausted.

