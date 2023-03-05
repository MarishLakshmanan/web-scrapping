import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image
from datetime import datetime
import os

baseUrl = 'http://books.toscrape.com/index.html'
url = 'http://books.toscrape.com/index.html'
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

def findTheSkip(txt):
    txt = txt.split('/')
    count = 0
    tolink = []
    for link in txt:
        if(link==".."):
            count+=1
        else:
            tolink.append(link)
    return (count,"/".join(tolink))

def splitandjoin(base,count,url):
    if(base[-1]=="/"):
        base = base[0:-1]
        print(base)
    base = base.split('/')
    base = base[0:-(count+1)]
    base = "/".join(base)
    return f'{base}/{url}'

def checkLink(anchorTags,currentUrl):
    
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
                print(currentUrl+" sdf "+url)
                res = findTheSkip(url)
                url = splitandjoin(currentUrl,res[0],res[1])
        except Exception as e:
            print("error"+e)
        if(isVisited(url)):
            continue  
        res = requests.get(url)
        visited.append(url)
        print(f'{url} status :{res.status_code}')
        if(res.status_code==200):
            first =False
            soup = BeautifulSoup(res.text,'html.parser')
            anchorTags = soup.find_all('a')
            errorElem = checkLink(anchorTags,url)
            if(errorElem):
                href = errorElem.get('href')
                driver.get(url)
                driver.execute_script(f'''document.querySelectorAll("a[href='{href}']")[0].style.border="5px solid red"''')
                name =str(datetime.now().timestamp())
                driver.save_screenshot(f'screenshots/{start}/{name}.png')
                pass
                
        else:
            print(url)
            return elem
            
            

        
errorElem = checkLink(anchorTags,url)
if(errorElem):
    # href = errorElem.get('href')
    # driver.get(url)
    # driver.execute_script(f'''document.querySelectorAll("a[href='{href}']")[0].style.border="5px solid red"''')
    # name =str(datetime.now().timestamp())
    # driver.save_screenshot(f'screenshots/{start}/{name}.png')
    pass
# print(visited)
# print(len(visited))