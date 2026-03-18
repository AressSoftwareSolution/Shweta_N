def square(n):
    i=1
    while i<=n:
        yield i*i
        i+=1

sqr=square(5)

print(list(sqr))  ## Print Complete List of Squares
## After the above line, the generator is exhausted, and there are no more values to yield.

# print(next(sqr))  ## This will raise StopIteration error as the generator is exhausted.

## Creating A new generator to get squares again
sqr=square(12)
print(list(sqr))

## Solution: if resuse is needed,convert the generator to a list and store it in a variable, then you can access the values multiple times without exhausting the generator.
sqr=square(5)
sqr_list=list(sqr)  ## Convert the generator to a list and store it in
print(sqr_list)  ## Print the list of squares
print(sqr_list)  ## You can print the list again without any issues as it is
