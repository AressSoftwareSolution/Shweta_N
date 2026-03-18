
import requests
from bs4 import BeautifulSoup as bs
import threading
def web_data(url):
    res=requests.get(url)
    soup=bs(res.text,"html.parser")
    print(soup.title)
    print(soup.a)
url1="https://www.iana.org/help/example-domains"
url2="https://www.iana.org/protocols"
t1=threading.Thread(target=web_data,args=(url1,))
t1.start()
t1.join()
t2=threading.Thread(target=web_data,args=(url2,))
t2.start()
t2.join()



