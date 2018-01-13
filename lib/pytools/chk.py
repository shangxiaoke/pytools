#/usr/bin/env python
#coding:utf-8

import os,commands

#IP合法检测
def ipchk(addr):
    b=addr.split('.')
    if len(b) == 4 and b[0] != '0' and b[3] != '0':
        try:
            if 255 > int(b[0]) and int(b[1]) and int(b[2]) and int(b[3]) >= 0:
                return True
        except:
            return False
    else:
        return False

#IP传递方法，列表或者IP文件
def ipc(ip):
    if type(ip) is list:
        for i in ip:
            yield i
    elif os.path.isfile(ip):
        with open(ip,'r') as f:
            for b in f.readlines():
		lb=b.strip()
		if not len(lb)==0 and not lb.startswith('#'):
                    yield lb.strip('\n')

################################远程命令引用################################

#使cmd参数支持列表或文件
def cmdc(cmd):
    if type(cmd) is list:
	for i in cmd:
	    yield i
    elif os.path.isfile(cmd):
        with open(cmd,'r') as rf:
	    for l in rf.readlines():
		ll=l.strip()
		if not len(ll)==0 and not ll.startswith('#'):
		    yield ll.strip('\n')
        rf.close()

###############################upload引用###################################
def dtree(path):
    lis=commands.getoutput('find %s -type d' % path)
    return lis.split('\n')

def ftree(path):
    lis=commands.getoutput('find %s -type f' % path)
    return lis.split('\n')

def dirname(path):
    de=commands.getoutput('dirname %s' % path)
    return de.split('\n')
