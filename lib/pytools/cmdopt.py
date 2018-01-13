#!/usr/bin/python
#coding:utf-8

import sys,os
class cmdopt(object):
    def __init__(self,short=None,long=None,type=None,show=None,argv=sys.argv):
        self.__short=short
        self.__long=long
        self.__type=type
        self.__help=show
        self.__argv=argv
        
    def run(self,target=None):
        args=cmdopt.optparser(self)
        target(*args)

    #命令行输入解析
    def optparser(self):
        x=[]
        try:
            if len(self.__argv[1:][0]) > 2:
                lout=cmdopt.optlong(self)
                for i in range(len(lout)):
                    n=cmdopt.typeform(self,i,lout[i])
                    x.append(n)
                return x
        
            elif len(self.__argv[1:][0]) == 2:
                sout=cmdopt.shortform(self)
                for i in range(len(sout)):
                    b=cmdopt.typeform(self,i,sout[i])
                    x.append(b)
                return x
        except Exception,e:
            return e
            cmdopt.usage(self)

    #sys.argv[1:] : ['--ip=[]','']
    #输入长选项检测，如果与定义选项相同，则返回除选项外的参数的列表
    def optlong(self):
        x=[]
        try:
            if self.__argv[1:][0] == '--help':
                cmdopt.man(self)
            elif len(self.__argv[1:]) > 1:
                #命令行长参数格式化
                lout=cmdopt.longform(self)
                #判断长长选项是否与定义选项一致
                for i in lout:
                    if i[0] in self.__long:
                        x.append(i[1])
                return x
        except Exception,e:
            return e
            cmdopt.usage(self)

    #选项判断完成后，根据定义type格式化返回的参数
    #长选项判断和短选项判断共用
    def typeform(self,i,a):
        if self.__type[i] == 'str':
            return a
        elif self.__type[i] == 'list':
            return cmdopt.lis(self,a)
        elif self.__type[i] == 'file,dir' or self.__type[i] =='dir,file':
            return a
        elif self.__type[i] == 'list,file' or self.__type[i] =='file,list':
            if os.path.isfile(a):
                return a
            else:
               return cmdopt.lis(self,a)
        else:
            raise cmdopt.usage(self)
    
    #str转list
    def lis(self,a):
        x=a.strip('[]')
        return x.split(',')
    
    #当输入为long格式时，格式化sys.argv列表内容为:[('--ip', [1,2,3]), ('--uname', 'shangxiaoke')]        
    def longform(self): 
        key=[]
        value=[]
        for i in self.__argv[1:]:
            na=i.split('=')
            key.append(na[0])
            value.append(na[1])
            nd=zip(key,value)
        return nd
    
    #如果是短格式选项，格式化命令行选项和参数为两个列表
    #sys.argv[1::2] : ['-i','-u','-p','-c']
    #sys.argv[2::2] : [1,2,3,4]  
    def shortform(self):
        try:
            if self.__argv[1:][0] == '-h':
                cmdopt.usage(self)
            elif len(self.__argv[1:]) > 1:
                if self.__argv[1::2] == self.__short:
                    return self.__argv[2::2]
        except Exception,e:
            return e
            cmdopt.usage(self)

    #man函数，返回帮助手册
    def man(self):
        cmdopt.usage(self)
        i=0
        while i < len(self.__short):
            print self.__short[i],self.__long[i],self.__type[i],self.__help[i]
            i+=1

    #错误输入时，返回帮助信息
    def usage(self):
        print "%s: python option -- h" % self.__argv[0]
        print self.__short
        print self.__long
