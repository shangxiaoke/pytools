#!/usr/bin/python
#coding:utf-8

import paramiko
class ressh(object):
    def __init__(self):
	pass

#建立连接
	self.__sftp=''
	self.__ssh=''
    def conn(self,ip,uname,userpwd):
	ssh=paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip,22,uname,userpwd)
	sftp=ssh.open_sftp()
	self.__ssh=ssh
	self.__sftp=sftp

#ssh远程命令正确返回结果
    def reout(self,cmd):
	re=[]
	stdin,stdout,stderr=self.__ssh.exec_command(cmd)
	for i in stdout.readlines():
	    re.append(i.rstrip('\n'))
	return re

#ssh内置函数引用
    def close(self):
	self.__ssh.close()

#远程创建目录
    def mkdir(self,path):
	self.__ssh.exec_command('mkdir -p %s' % path)

#远程目录递归路径列表
    def dtree(self,path):
	return ressh.reout(self,'find %s -type d' % path)

#远程目录内文件列表
    def ftree(self,path):
	return ressh.reout(self,'find %s -type f' % path)

#文件或目录的dirname
    def dirname(self,path):
	return ressh.reout(self,'dirname %s' % path)

#引用sftp内置函数
    def get(self,mv_path,load_path):
	self.__sftp.get(mv_path,load_path)

    def put(self,mv_path,load_path):
	self.__sftp.put(mv_path,load_path)

#判断文件或目录状态
    def restat(self,load_path):
	try:
	    self.__sftp.stat(load_path)
	    return True
	except:
	    return False

#判断是否可切换路径，不能切换则为文件，可切换则为目录
    def isfile(self,path):
	if ressh.restat(self,path):
	    try:
		self.__sftp.chdir(path)
		return False
	    except:
		return True
	else:
	    return False

    def isdir(self,path):
	if ressh.restat(self,path):
	    try:
		self.__sftp.chdir(path)
		return True
	    except:
		return False
	else:
		return False
