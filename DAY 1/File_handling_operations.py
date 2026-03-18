## Open a file 
file = open("sample.txt", "r") 
## Read the file
cont=file.read()
print(cont)
## Close File
file.close()


## write to a file
file2=open("sample2.txt", "w")
file2.write("New content added to sample2.txt")
file2.close()

file2=open("sample2.txt", "r")
cont=file2.read()
print(cont)
file2.close()

## Append to a file
file3=open("sample2.txt", "a")
file3.write("\n Content Appended.")
file3.close()
file3=open("sample2.txt", "r")
cont=file3.read()
print(cont)
file3.close()

## Best Practice: Using "with" statment

with open("sample.txt", "r") as f:
    content = f.read()
    print(content)