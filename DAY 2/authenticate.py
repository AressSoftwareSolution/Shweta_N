## Manual Authentication 
user={"username":"admin","password":"admin123"}
def authenticate(username,password):
    if username==user["username"] and password==user["password"]:
        return "Authentication successful"
    else:
        return "Authentication failed"

username=input("enter your user name:")
password=input("enter your password:")
result=authenticate(username,password)
print(result)

## API Authentication
import requests
data={"userId:1"}
res=requests.post("https://jsonplaceholder.typicode.com/posts",data=data)
print(res.json())
