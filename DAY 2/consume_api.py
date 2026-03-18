## Concume API using python
import requests
## GET REQUEST
res=requests.get("https://www.iana.org/help/example-domains")
print(res.status_code)
print(res.headers)
print(res.text)
print(res.content)