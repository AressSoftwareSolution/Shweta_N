import requests

# ## GET REQUEST
# res=requests.get("https://www.iana.org/help/example-domains")
# print(res.status_code) ## to print the status code of the response
# print(res.headers) ## to print the headers of the response
# print(res.text) ## it will prnt the html code of the response
# print(res.content) 

## POST REQUEST
data={"username":"john_doe","password":"123456"}
res=requests.post("https://jsonplaceholder.typicode.com/posts",data=data)
print(res.json())

