import re

text="hello world,i am learning regex in python and it is very useful for text processing. i have 2 years of experience in python programming and i want to enhance my skills in regex."
##Implementing common Regex functions

result=re.match(r"hello",text)   ##re.match() check for a match at the beginning of the string
print(result)

result=re.search(r"world",text)  ##re.search() search for the first occurrence of the pattern anywhere in the string
print(result)

result=re.findall("\d",text) ## re.findall() find all occurrences of the pattern in the string and return them as a list
print(result)

result=re.sub(r"python","java",text) ## re.sub() replace occurrences of the pattern with a specified replacement string
print(result)

results=re.split("\s",text) ## re.split() split the string into a list based on the specified pattern
print(results)

## Removing extra spaces
text="   hello world"
result=re.sub("\s+"," ",text)
print(result)

## Extracting email
text="smaple@gmail.com"
pattern="[a-zA-Z0-9._]+@[a-zA-Z0-9._]+\.[a-zA-Z]{2,}"
email=re.search(pattern,text)
print(email)