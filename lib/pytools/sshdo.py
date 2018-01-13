#!/usr/bin/python
#coding:utf-8

import paramiko,chk,time,kernel
class sshdo(object):
    def run(self,ip,uname,userpwd,cmd):
        for i in chk.ipc(ip):
            ip=str(i)
            if chk.ipchk(ip):
            	print '>>> %s <<<' % ip
            	try:
                    self.__ssh=paramiko.SSHClient()
                    self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    self.__ssh.connect(ip,22,uname,userpwd,timeout=10)
                    self.__sussh=self.__ssh.invoke_shell()
                    time.sleep(0.1)
		    
                    if uname == 'root':
                        self.__sussh.send('%s\n' % 'export PS1="[\u@\h \W]# "')
                        #time.sleep(0.1)
                        for m in chk.cmdc(cmd):
                            time.sleep(0.1)
                            self.__sussh.send('%s\n' % m)
                            time.sleep(0.1)

                        resp=self.__sussh.recv(-1)
                        while not resp.endswith('#'):
                            rep=self.__sussh.recv(-1)
                            resp+=rep
                        print resp
                        self.__ssh.close()

                    else:
                        self.__sussh.send('%s\n' % 'export PS1="[\u@\h \W]\$ "')
                        #time.sleep(0.1)
                        for m in chk.cmdc(cmd):
                            time.sleep(0.1)
                            self.__sussh.send('%s\n' % m)
                            time.sleep(0.1)

                        resp=self.__sussh.recv(-1)
                        while not resp.endswith('$'):
                            rep=self.__sussh.recv(-1)
                            resp+=rep
                        result=resp
                        print result
                        self.__ssh.close()
                    
                except Exception,e:
                    print "%s\n" % e
            else:
                print 'IP ERROR\n'
