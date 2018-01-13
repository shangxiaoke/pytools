#!/usr/bin/python
#coding:utf-8

import paramiko,chk,time

class sudo(object):
    def run(self,ip,uname,userpwd,rootpwd,cmd):
        for i in chk.ipc(ip):
            ip=str(i)
            print '>>> %s <<<' % ip
            if chk.ipchk(ip):
                try:
		    if uname != 'root':
                        self.__ssh=paramiko.SSHClient()
                        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())        
                        self.__ssh.connect(ip,22,uname,userpwd,timeout=10)
                        self.__sussh=self.__ssh.invoke_shell()
                        time.sleep(0.1)
			
			l = ['unset LANG','export PS1="[\u@\h \W]\$ "','su - root']
			for i in l:
                            #time.sleep(0.1)
                            self.__sussh.send('%s\n' % i)
                            #time.sleep(0.1)

                        resp = self.__sussh.recv(-1)
                        while not resp.endswith(':'):
                            rep = self.__sussh.recv(-1)
                            resp += rep

                        self.__sussh.send('%s\n' % rootpwd)
                        time.sleep(0.2)
                        self.__sussh.send('%s\n' % 'export PS1="[\u@\h \W]# "')
                        #time.sleep(0.1)

                        for m in chk.cmdc(cmd):
                            time.sleep(0.1)
                            self.__sussh.send('%s\n' % m)
                            time.sleep(0.1)

                        resp = self.__sussh.recv(-1)
                        while not resp.endswith('#'):
                            rep = self.__sussh.recv(-1)
                            resp += rep
                        print resp.lstrip()
                        self.__ssh.close()

                except Exception,e:
                    print "%s\n" % e
            else:
                print 'IP ERROR\n'
