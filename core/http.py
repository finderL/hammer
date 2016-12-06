import os
import pycurl
import threading
import StringIO

mylock=threading.RLock()


def auth(username,passwd,config):
    auth4up(username,passwd,config)

def printstr(rs):
    mylock.acquire()
    print rs
    mylock.release()
    
    
def auth4up(username,passwd,config):
    c=pycurl.Curl()
    http=GetHttpDate(config['-f'])
    page_buf = StringIO.StringIO()
    head_buf = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, page_buf.write)
    c.setopt(pycurl.HEADERFUNCTION, head_buf.write)
    c.setopt(pycurl.HTTPHEADER,http['httphead'])
    if http['act']=="POST":
        c.setopt(pycurl.URL, config['-s']+http['url'])
    if http['act']=="GET":
        url=http['url'].replace("$USER$",username)
        url=url.replace("$PASS$",passwd)
        c.setopt(pycurl.URL, config['-s']+url)
        c.perform()
        
    elif http['act']=='POST':
        post=http['httpost'].replace("$USER$",username)
        post=post.replace("$PASS$",passwd)
        c.setopt(pycurl.POSTFIELDS,post)
        c.perform()
    # get page data    
    
    if verify(head_buf.getvalue(),config):
        printstr("Vaild  %s/%s ===================" %(username,passwd))
    else:
        printstr("Invail %s/%s" %(username,passwd))
        

def verify(data,config):
    if config['--succauth']:
        if data.find(config['--succauth'])>=0:
            return True
        return False
    
    if config['--failauth']:
        if data.find(config['--failauth'])>=0:
            return False
        return True
    
def GetHttpDate(fname):
    http={'act':'','url':'','httphead':[],'httpost':'','version':''}
    f=open(fname)
    flag=0
    http['act'],http['url'],http['version']=f.readline().strip().split(' ',2)
    for l in f:
        l=l.strip()
        if flag:
            http['httpost']=l
            break
        if l:
            http['httphead'].append(l)
        else:
            flag=1
    return http
    
    