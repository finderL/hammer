import getopt
import sys
import time
import socket
import threading
import os
import re
#import threadpool
from lib import lib_TheardPool2



config={'-u':None,'-p':None,'-s':'','-t':1,'-f':'','-d':'','-h':None,'--failauth':'','--succauth':'','module':None}

def parseargs():
    try:
        opts,args=getopt.getopt(sys.argv[1:],'u:p:s:t:f:d:h',['help','failauth=','succauth='])
    except Exception:
        Use()
    
    for key,value in opts:
        if key in ('-h','--help'):
            Use()
        config[key]=value
    
    
def Use():
    print "hammer.py a brute force tool for many auth server"
    print "hammer.py {-u,-p,-s}[-d,-h]"
    print "-u FILE ,user username dict"
    print "-p FILE ,user password dict"
    print "-t 1-16, thead numbers"
    print "-s server,support server,it's can be [http ssh ftp telnet rdp]"
    print "-d data,data for server"
    print "-f data,read data from file"
    print "--succauth ,flag for succssfuly auth"
    print "--failauth ,flag for fail auth"
    print "-h,--help,display the help message"
    exit(1)


def getmodule():
    if not config['-s']:
        print "Please input vaild service like 'http[s]:// ssh://127.0.0.1:22  ftp://127.0.0.1:21'"
        Use()
    #dynamic load auth module
    if config['-s'][:5]=='https':
        module=__import__("core.https",fromlist=['core'])
    elif config['-s'][:4]=='http':
        module=__import__("core.http",fromlist=['core'])
    elif config['-s'][:4]=='https':
        module=__import__("core.ftps",fromlist=['core'])
    elif config['-s'][:3]=='ftp':
        module=__import__("core.ftp",fromlist=['core'])
    elif config['-s'][:3]=='ssh':
        module=__import__("core.ssh",fromlist=['core'])
    elif config['-s'][:3]=='rdp':
        module=__import__("core.rdp",fromlist=['core'])
    else:
        print "Please input vaild service like 'http[s]:// ssh://127.0.0.1:22  ftp://127.0.0.1:21'"
        Use()        
    return module

def authfunc(username,passwd,config):
    config['module'].auth(username,passwd,config)
    
def main():
    pool=lib_TheardPool2.threadpool(tmax=int(config['-t']))
    uname=open(config['-u'])
    upass=open(config['-p'])
    config['module']=getmodule()
    for nameline in uname:
        username=nameline.strip()
        for passline in upass:
            passwd=passline.strip()
            pool.addtask(authfunc,(username,passwd,config))
        upass.seek(0)
    pool.waitPoolComplete()
            
if __name__=="__main__":
    start=time.time()
    sys.path.append(sys.path[0]+'/lib')
    parseargs()
    #print config
    main()
    end=time.time()
    print "============%fs==============" %(end-start)
    
    
    