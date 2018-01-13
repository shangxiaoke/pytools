#!/usr/bin/python
#coding:utf-8

import chk,os,kernel,time

def put(conn_ip,uname,userpwd,mv_path,load_path):
    for i in chk.ipc(conn_ip):
	ip=str(i)
	print '>>> %s <<<' % ip
	if chk.ipchk(ip):
	    try:
	        sftp=kernel.ressh()
	        sftp.conn(ip,uname,userpwd)

	        load_path=load_path.rstrip('/')
                dme=chk.dirname(mv_path)[0]
	        remv_path=mv_path.replace(dme,load_path)

	        #如果本地移动对象为文件：
	        if os.path.isfile(mv_path):
		    #本地文件--远程文件，判断远程文件是否存在：
		    if sftp.isfile(load_path):
                        x_while = True
                        while x_while:
                            readin=raw_input('文件已存在，是否覆盖(y/n): ')
                            if readin == 'y':
                                x_while=False
                                sftp.put(mv_path,load_path)
                            elif readin=='n':
                                x_while=False
                                pass

		    #本地文件--远程目录
		    elif sftp.isdir(load_path):
		        #判断目录下是否存在同名文件
		        if sftp.isfile(remv_path):
                            a_while = True
                            while a_while:
                                readin=raw_input('文件已存在，是否覆盖(y/n): ')
                                if readin=='y':
                                    a_while = False
                                    sftp.put(mv_path,remv_path)
                                elif readin=='n':
                                    a_while = False
                                    pass
                        else:
                            sftp.put(mv_path,remv_path)
		    #本地文件--远程文件重命名
		    else:
		        sftp.put(mv_path,load_path)
			   
	        #如果本地移动对象为目录:
	        elif os.path.isdir(mv_path):
		    dls=chk.dtree(mv_path)
                    fls=chk.ftree(mv_path)
                    dme=chk.dirname(mv_path)[0]
                    dir0=dls[0].replace(dme,load_path)

		    #本地目录--远程目录，目录重名判断
		    if sftp.isdir(dir0):
		        b_while=True
                        while b_while:
                            readin=raw_input('目录已存在，是否覆盖(y/n):')
                            if readin=='y':
                                b_while=False
                                for n in dls:
                                    n=n.replace(dme,load_path)
                                    sftp.mkdir(n)
                                time.sleep(0.5)
                                for k in fls:
                                    re_k=k.replace(dme,load_path)
                                    sftp.put(k,re_k)
                            elif readin == 'n':
                                b_while=False
                                pass

		    #目录不存在，创建并上传
		    elif not sftp.isdir(dir0):
                        for n in dls:
                            n=n.replace(dme,load_path)
                            sftp.mkdir(n)
			time.sleep(0.5)
		        for k in fls:
			    re_k=k.replace(dme,load_path)
			    sftp.put(k,re_k)

	    except Exception,e:
                print '%s\n' % e
	else:
	    print 'IP ERROR\n'
