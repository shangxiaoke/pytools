#!/usr/bin/python
#coding:utf-8

import chk,os,kernel,time

def get(conn_ip,uname,userpwd,mv_path,load_path):
    for i in chk.ipc(conn_ip):
	ip=str(i)
	print '>>> %s <<<' % ip
	if chk.ipchk(ip):
	    try:
		sftp=kernel.ressh()
                sftp.conn(ip,uname,userpwd)

		load_path=load_path.rstrip('/')
                #获取远程移动对象的绝对路径头目录:如：'/root'
                mv_dirname=sftp.dirname(mv_path)[0].strip('\n')
		remv_path=mv_path.replace(mv_dirname,load_path)

                #远程检测移动对象为文件：
                if sftp.isfile(mv_path):
                    #如果目标已存在同名文件：
                    if os.path.isfile(load_path):
                        x_while = True
                        while x_while:
                            readin=raw_input('文件已存在，是否覆盖(y/n): ')
                            if readin == 'y':
                                x_while=False
                                sftp.get(mv_path,load_path)
                            elif readin=='n':
                                x_while=False
                                pass

                    #如果目标为目录，则拼接
                    elif os.path.isdir(load_path):
			if os.path.isfile(remv_path):
			    a_while = True
                            while a_while:
                                readin=raw_input('文件已存在，是否覆盖(y/n): ')
                                if readin=='y':
                                    a_while = False
                                    sftp.get(mv_path,remv_path)
                                elif readin=='n':
                                    a_while = False
                                    pass
                        else:
                            sftp.get(mv_path,remv_path)
                    else:
                        sftp.get(mv_path,load_path)
			
                #远程检测移动对象为目录:
                elif sftp.isdir(mv_path):
		    #远程文件目录列表dir_lis和文件列表file_lis
                    dir_lis=sftp.dtree(mv_path)
                    file_lis=sftp.ftree(mv_path)
                    #获取远程移动对象的相对首目录：如：'/root/mvdir'
                    mv_dir0=dir_lis[0].strip('\n')
                    #拼接本地下载首目录绝对路径
                    ld_dir0=mv_dir0.replace(mv_dirname,load_path)

                    #如果目标为目录：递归传输目录中的文件，由最外层文件开始传输
                    if os.path.isdir(load_path):
			#本地检测下载首目录如果存在
			if os.path.isdir(ld_dir0):
			    b_while=True
                            while b_while:
                                readin=raw_input('目录已存在，是否覆盖(y/n): ')
                                if readin == 'y':
                                    b_while=False
                                    for i in dir_lis:
                                        i=i.rstrip('\n')
                                        ld_dir=i.replace(mv_dirname,load_path)
                                        os.makedirs(ld_dir)
                                    time.sleep(0.5)
                                    for a in file_lis:
                                        a=a.rstrip('\n')
                                        ld_file=a.replace(mv_dirname,load_path)
                                        sftp.get(a,ld_file)
                                elif readin == 'n':
                                    b_while=False
                                    pass

			#本地检测下载目录不存在，则创建后下载
			elif not os.path.isdir(ld_dir0):
			    for i in dir_lis:
                                i=i.rstrip('\n')
                                ld_dir=i.replace(mv_dirname,load_path)
                                os.makedirs(ld_dir)
			    time.sleep(0.5)	
			    for a in file_lis:
				a=a.rstrip('\n')
				ld_file=a.replace(mv_dirname,load_path)
				sftp.get(a,ld_file)

	    except Exception,e:
		print '%s\n' % e
	else:
	    print 'IP ERROR\n'
