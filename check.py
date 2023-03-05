
link = 'hello/there/leys'
base = 'www.google.com/1/2/3/4/5/6/7/'

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

res = findTheSkip(link)

print(splitandjoin(base,res[0],res[1]))