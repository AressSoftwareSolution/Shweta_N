from bs4 import BeautifulSoup as bs
import requests

url="https://www.iana.org/help/example-domains"
response=requests.get(url)
soup= bs(response.text,"html.parser")
print(soup.get_text()) ## to print the text of the webpage without the html tags
print("\n")
print(soup.title) ## to print the title of the webpage
print("\n")
print(soup.a) ## to print the first anchor tag of the webpage
print("\n")
print(soup.find_all("a")) ## to print all the anchor tags of the webpage
print("\n")
print(soup.h1)
