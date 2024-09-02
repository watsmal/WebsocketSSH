# -*- coding: utf-8 -*-
from __future__ import print_function
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket 
#import commands
import subprocess
import os
import re
from paramiko import util
from paramiko import SSHClient
from paramiko import AutoAddPolicy
import paramiko

class SimpleEcho(WebSocket):
    def handleMessage(self):
        # echo message back to client
        print("#######111111########")
        print('[%s] - Get:%s' % (self.address,self.data))
        # 屏蔽exit
        if 'exit' in self.data:
            self.data=self.data.replace('exit','\n')
        #处理第一次连接，接收ssh数据建立连接
        elif self.data.startswith('[first-start-connection#@1]'): #构建一个 "self.data=[first-start-connection#@1]10.0.21.51"
            print('client firstly connect,start ssh connection')
            IP=self.data.split('[first-start-connection#@1]')[1]
            Port=22
            UserName='watsmal' #root
            Password='123456' #root
            print('IP='+IP)
            self.FirstLogin=False
            #连接ssh
            # 设置记录日志
            log_file = 'centos_ssh.log'
            util.log_to_file(log_file)
            # 生成ssh客户端实例
            self.ssh = SSHClient()
            self.ssh.set_missing_host_key_policy(AutoAddPolicy())
            print('get ssh client')
            self.ssh.connect(IP,Port,UserName,Password) # 如果建立失败，立马closed
            print('ssh login successfully') 
            self.chan=self.ssh.invoke_shell()
            print('get invoke_shell successfully')
            self.chan.settimeout(1000)
            # 刚进入linux服务器等待一会，否则直接通过chan.recv获取的信息不完整
            #
            second=1  # 拖时间
            for a in range(second):
                for i in range(3):
                    for j in range(15):
                        for k in range(10):
                            u=i*j
            #
            print('sleep 1s waiting for some no need info')
            LoginInfo=self.chan.recv(2048)	 # Welcome to Ubuntu 16.04.6 LTS..等登录信息
            print(LoginInfo)
            self.EndSymbol=['$ ','# ','> ','* ','[J']	# 设置我们定义的结束符
            print('start transport')
            self.data='ls' # 尝试命令
        # 执行命令
        result=self.runCommand(self.data) # 执行命令

        # -----------------------------------------
        self.sendMessage(result)
        print('[%s] - Send:%s' % (self.address,result))

    def handleConnected(self):
        try:
            print("#######2#######")
            self.FirstLogin = True
            print(self.address, 'connected')
        except Exception as e:
            print("Error during connection handling:", e)
        # self.FirstLogin=True
        # print(self.address, 'connected')
    def handleClose(self):
        print("#######3#######")

        print(self.address, 'closed')

    #接收指令的方法
    def runCommand(self,Command):
        print("#######4#######")
        print('exec command:'+Command)
        self.chan.send(Command+'\n')
        print("1111")	# 指令后加 '\n' 表示换行
        Result=''
        print('waiting for reply')
        while True:
            Temp=self.chan.recv(4096) # temp是byte类型
            print("Temp",Temp)

            #-------------------------------------------
            # 解码为字符串
            decoded_data = Temp.decode('utf-8')

            # 去掉 ANSI 转义序列
            clean_data = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', decoded_data)
            # ------------------------------------------

            Result+=clean_data # string+string no can string !+ byte[]

            print("result=" , Result ,len(Result))
            if len(Result)!=0:
                print('test--------------------'+Result[-2:]+'-----------------'+Result)
            if Result[-2:] in self.EndSymbol:		# 判断最后两个字符是否是我们定义的结束符
                break
        Final=Result.split('\n')[1:]	# 第一行是我们输入的指令，没用丢弃
        print('\n'.join(Final),end='')
        return '\n'.join(Final) # 最后一行是linux的SP1输入提示符，没用丢弃
def console(**kwargs):
    print('start listening')
    server = SimpleWebSocketServer('0.0.0.0', 9900, SimpleEcho)
    # server = SimpleWebSocketServer('192.168.113.5', 6789, SimpleEcho)
    server.serveforever()
if __name__ == "__main__":
    console()
