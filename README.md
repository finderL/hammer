#hammer-一个支持多种协议的暴力破解攻击
###Author:yixuanzi
###Data:2015-12-6
###Email:yeying0311@126.com
###Version:1.1.0
```
    hammer.py a brute force tool for many auth server
    hammer.py {-u,-p,-s}[-d,-h]
    -u FILE ,user username dict
    -p FILE ,user password dict
    -t 1-16, thead numbers
    -s server,support server,it's can be [http(s) ssh ftp telnet rdp]
    -d data,data for server
    -f data,read data from file
    --succauth ,flag for succssfuly auth
    --failauth ,flag for fail auth
    -h,--help,display the help message
```
--------
Example
<pre>
login.txt 登录数据包
hammer -u user.txt  -p pass.txt -t 4 -f login.txt --succauth='index.php' -s http://192.168.31.24 
</pre>
