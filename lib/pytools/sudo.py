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

                        #root用户和普通用户默认提示符设置
			ps1 = 'export PS1="[\u@\h \W]# "'
			ps2 = 'export PS1="[\u@\h \W]\$ "'

			l = [ps2 ,'su - root']
			for i in l:
                            self.__sussh.send('%s\n' % i)
                            time.sleep(0.1)

                        resp = self.__sussh.recv(-1)
                        #中文环境或英文环境下不同密码输入返回
			while not (resp.endswith('密码：') or resp.endswith('Password:')):
                            rep = self.__sussh.recv(-1)
                            resp += rep

                        self.__sussh.send('%s\n' % rootpwd)
                        time.sleep(0.1)
                        self.__sussh.send('%s\n' % ps1)
                        time.sleep(0.1)

                        for m in chk.cmdc(cmd):
                            time.sleep(0.1)
                            self.__sussh.send('%s\n' % m)
                            time.sleep(0.1)

                        resp = self.__sussh.recv(-1)
                        while not resp.endswith('#'):
                            rep = self.__sussh.recv(-1)
                            resp += rep

                        #命令返回结果str转list
			re = resp.splitlines()

                        #结果处理，排除自定义和杂项
			for i in re:
			    if i != ' ' and i != '' and ps1 not in i:
				print i
                        self.__ssh.close()

                except Exception,e:
                    print "%s\n" % e
            else:
                print 'IP ERROR\n'
