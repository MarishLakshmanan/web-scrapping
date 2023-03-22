from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image
from datetime import datetime
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'browser':'ALL' }
chrome_options = Options()
# chrome_options.add_argument('--headless'-]ok
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
baseUrl = 'http://localhost:5500/tester/1.html'
url = 'http://localhost:5500/tester/1.html'
driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options,desired_capabilities=d)
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
anchorTags = soup.find_all('a')
start = str(datetime.now().timestamp()).split('.')[0]
os.mkdir(f'screenshots/{start}')
visited = []
first = True



# Anchor tag and html forms
# should avoid going to other websites
# avoid visiting same links again

def checkSite(url):
    driver.get(url)
    err = driver.get_log('browser')
    if(len(err)!=0):
        try:
            msg = ''
            for error in err:
                msg = msg+error['message']+", "
            print('werer',msg)
            driver.execute_script("elem = document.createElement('div');elem.innerHTML='<h4>"+msg+"</h4>';elem.style.cssText = 'position:absolute;top:0;left:0;background-color:rgba(0,0,0,.6);width:100%;height:100vh;color:white;display:flex;justify-content:center;align-items:center;z-index:7189237918;font-family:sans-serif;';document.getElementsByTagName('body')[0].appendChild(elem);")
        except Exception as e:
            print(e)
        
        print("logError: "+url)
        name =str(datetime.now().timestamp())
        driver.save_screenshot(f'screenshots/{start}/{name}logError.png')

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
    checkSite(currentUrl)
    if(len(anchorTags)==0):
        return False
    for elem in anchorTags:
        url =elem.get("href") 
        
        try:
            if(url.find(baseUrl)):
                if(url.find('http')>-1):
                    print("other "+url)
                    continue
                # print(currentUrl+" sdf "+url)
                res = findTheSkip(url)
                url = splitandjoin(currentUrl,res[0],res[1])
                print("Error url ",url)
        except Exception as e:
            print("error"+e)
        if(isVisited(url)):
            continue  
        goodTogo = True
        try:
            driver.get(url)
        except Exception as e:
            print(e)
            goodTogo = False
        visited.append(url)

        if(goodTogo==True):
            first =False
            soup = BeautifulSoup(driver.page_source,'html.parser')
            anchorTags = soup.find_all('a')
            errorElem = checkLink(anchorTags,url)
            if(errorElem):
                print(url)
                href = errorElem.get('href')
                driver.get(url)
                driver.execute_script(f'''document.querySelectorAll("a[href='{href}']")[0].style.border="5px solid red"''')
                name =str(datetime.now().timestamp())
                driver.save_screenshot(f'screenshots/{start}/{name}.png')
                
                
        else:
            print("urlError: "+url)
            return elem

        
errorElem = checkLink(anchorTags,url)
if(errorElem):
    href = errorElem.get('href')
    print(url)
    driver.get(url)
    driver.execute_script(f'''document.querySelectorAll("a[href='{href}']")[0].style.border="5px solid red"''')
    name =str(datetime.now().timestamp())
    driver.save_screenshot(f'screenshots/{start}/{name}.png')

print(visited)
print(len(visited))
driver.quit()