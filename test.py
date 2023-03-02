import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image
from datetime import datetime
import os

baseUrl = 'http://127.0.0.1:5500/tester'
url = 'http://127.0.0.1:5500/tester/1.html'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
anchorTags = soup.find_all('a')
driver = webdriver.Chrome()
start = str(datetime.now().timestamp()).split('.')[0]
os.mkdir(f'screenshots/{start}')
visited = []
first = True



# Anchor tag and html forms
# should avoid going to other websites
# avoid visiting same links again


def isVisited(url):
    for link in visited:
        if(link==url):
            return True
    return False

def checkLink(anchorTags):
    
    global first
    if(len(anchorTags)==0):
        return False
    for elem in anchorTags:
        url =elem.get("href") 
        try:
            if(url.find(baseUrl)):
                if(url.find('http')>-1):
                    print("other "+url)
                    continue
                url = f'{baseUrl}/{url}'
        except Exception as e:
            print(e)
        if(isVisited(url)):
            continue  
        res = requests.get(url)
        visited.append(url)
        # print(f'{url} status :{res.status_code}')
        if(res.status_code==200):
            first =False
            soup = BeautifulSoup(res.text,'html.parser')
            anchorTags = soup.find_all('a')
            errorElem = checkLink(anchorTags)
            if(errorElem):
                href = errorElem.get('href')
                driver.get(url)
                driver.execute_script(f'''document.querySelectorAll("a[href='{href}']")[0].style.border="5px solid red"''')
                name =str(datetime.now().timestamp())
                driver.save_screenshot(f'screenshots/{start}/{name}.png')
                
        else:
            print(url)
            return elem
            
            
        
errorElem = checkLink(anchorTags)
if(errorElem):
    href = errorElem.get('href')
    driver.get(url)
    driver.execute_script(f'''document.querySelectorAll("a[href='{href}']")[0].style.border="5px solid red"''')
    name =str(datetime.now().timestamp())
    driver.save_screenshot(f'screenshots/{start}/{name}.png')
# print(visited)
# print(len(visited))