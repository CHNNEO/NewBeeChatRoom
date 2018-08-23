'''
name:甘乐
date:2018.7.3
project:网络聊天室(图形界面)
        服务器端
tool:python3.5 mysql tkinter

'''

import socket
import select
import time
from mysql_python import *
import os
import sys


class ChatServer():
    def __init__(self):
        self.users = {} #oto聊天窗口udp用户字典,用户名：(ip,port)
        self.group_users = {} #otm聊天窗口udp用户字典，用户名：(ip,port)
        self.tcp_users = {} #存放已登录的用户的tcp套机字，用于命令的传输,用户名：套接字
        self.temp_msg = {} 

        self.db = Mysql_python("localhost", 3306, "chat_room_project", "root", "123456")

        print("launch threading")
        #tcp服务器绑定
        self.tcpServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcpServer.setblocking(False)
        self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        localIP = '127.0.0.1'
        serverPort = 8888

        #服务器地址绑定
        self.tcpServer.bind((localIP,serverPort))
        self.tcpServer.listen(10)

        #udp端口设置为9999
        self.udpPort = 9999
        self.udpServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udpServer.bind((localIP,self.udpPort))
        self.udpServer.setblocking(False)

        self.listSocket = [self.tcpServer,self.udpServer]

    def run(self):
        while True:
            try:
                print("开始select监听")
                rlist = select.select(self.listSocket,[],[])[0]
                for sock in rlist:
                    #如果是tcpServer表示有新的客户端发送请求
                    if sock is self.tcpServer:
                        print("等待连接")
                        client,addr = sock.accept()
                        self.listSocket.append(client)
                    #如果是udpServer表示是聊天信息
                    elif sock is self.udpServer:
                        data, addr = sock.recvfrom(1024)
                        msgList = data.decode('utf-8').split("&")
                        #单独聊天
                        if msgList[0] == "C":
                            self.do_chat(sock,msgList[1:])
                        #群聊
                        if msgList[0] == "GC":
                            self.do_group_chat(sock,msgList[1:])                          
                    else:
                        #如果是client表示是客户端(tcp)发送的命令
                        command = sock.recv(1024)
                        print("command:",command)
                        #解析命令
                        if command:
                            self.parse(sock,command)
                        else:
                            #command为空，即客户端断开连接，将其移出监听列表
                            self.listSocket.remove(sock)
            except ConnectionResetError:
                continue
        
    def parse(self,sock,command):
        # 注册登陆消息格式：标志 name,upasswd
        msgList = command.decode('utf-8').split('&')
        # print(msgList)
        #判断请求类型进行处理
        if msgList[0] == 'R': #注册
            self.do_register(sock, msgList[1:])

        elif msgList[0] == 'L': #登陆
            self.do_login(sock, msgList[1:])


        elif msgList[0] == 'RE':
            #获取资料列表消息格式：标志 name
            self.do_refresh(sock, msgList[1])

        elif msgList[0] == 'ST':           
        #修改登陆状态消息格式：标志 name 登陆状态
            self.do_change_state(sock,msgList[1:])

        #oto聊天窗口开启，将聊天窗口的套接字加入到字典中
        elif msgList[0] == "CO":
            name = msgList[-2]
            ip,port = msgList[-1].split(":")
            self.users[name] =(ip,int(port))
            print(self.users,"oto")
            
        #获取用户头像信息
        elif msgList[0] == "GI":
            self.do_get_img(sock,msgList[1])

        #添加好友
        elif msgList[0] == "ADD":
            self.do_add_friend(sock,msgList[1:])

        #创建好友分组
        elif msgList[0] == "NFG":
            self.do_create_friend_group(sock,msgList[1:])

        #otm聊天窗口开启
        elif msgList[0] == "GCO":
            name = msgList[-2]
            ip,port = msgList[-1].split(":")
            self.group_users[name] = (ip,int(port))
            print(self.group_users,'hello')

        #创建新群
        elif msgList[0] == "CNG":
            self.create_new_group(sock,msgList[1:])

        #添加群请求
        elif msgList[0] == "ADDG":
            self.add_group(sock,msgList[1:])
        #==========================================
        #扩展功能上传下载
        #共享文件列表
        elif msgList[0] == "WJLB":
            self.do_list(sock)
        #上传
        elif msgList[0] == 'SC':
            self.do_upLoading(sock,msgList[1:])
        #下载
        elif msgList[0] == 'XZ':
            self.do_downLoading(sock,msgList[1:])
        #==============================================   

        #客户端退出
        elif msgList[0] == 'Q':
            name = msgList[-1]
            try:
                del self.tcp_users[name]
                print(self.tcp_users)
            except:
                pass
            try:
                del self.users[name]
                print(self.users)
            except:
                pass

        elif msgList[0] == "AS":
            self.do_answer(msgList[1:])
    #=======================================================
    #功能扩展
    def do_list(self,sock):
        """向客户端发送共享文件列表
        """
        FILE_PATH ="./files/"
        #获取服务器中共享文件夹中的，文件列表
        file_list = os.listdir(FILE_PATH)
        print("开始判断")
        if not file_list:
            sock.send('601&文件库为空'.encode())
            time.sleep(0.1)
            return 
        else:
            sock.send(b'601&OK')
            time.sleep(0.1)

        filess = ""
        for i in file_list:
            if i[0] != '.' and \
            os.path.isfile(FILE_PATH + i):
                filess = filess + i + '#'
        #将文件列表用＃分隔符连接成一个长字符串，并加上前置　"401&"　标识符
        filess="601&"+filess
        sock.send(filess.encode())
        print("发送完成")


    def do_upLoading(self,sock,filenames):
        """接收客户端文件上传请求，并将上传的文件存储在默认路径下
            默认路径是当前文件夹上一级的files文件FILE_PATH ="./../files/"
        """
        FILE_PATH ="./files/"
        #filenames[0]为文件名，[1]为上传文件大小，[2]二进制数据流
        filename = filenames[0]
        #filenames长度小于３时，未开始传输数据
        if len(filenames) < 3:
            #如果服务器中共享文件列表中已经存在同名的文件
            if os.path.exists(FILE_PATH + filename):
                sock.send(b'602&NotOK')
                time.sleep(0.1)
            #否则创建一个空文件
            else:
                fd=open(FILE_PATH+filename,'w')
                fd.close()
                sock.send(b'602&OK')
                time.sleep(0.1)
        #filenames长度大于３时，开始传输数据
        if len(filenames) >= 3:
            #上传到服务器文件的大小为client_file_size
            client_file_size = int(filenames[1])
            #上传到服务器文件的［已经解码的］数据流为client_file_data
            client_file_data = filenames[2]
            #判断服务器中共享文件中存在同名文件的大小
            size = os.path.getsize(FILE_PATH + filename)  
            #如果文件大小与所上传文件名称大小都相等,不再追加
            if size >= client_file_size:
                pass
                #否则追加
            elif size < client_file_size:
                try:
                    fd = open(FILE_PATH + filename,'a')
                except:
                    sock.send("602&无法完成上传".encode())
                time.sleep(0.1)
                fd.write(client_file_data)
                fd.close()
    def do_downLoading(self,sock,filenames):
        """向客户端发送，对方请求所需的下载文件
        """
        filename = filenames[0]
        FILE_PATH ="./files/"
        #获取列表
        file_list = os.listdir(FILE_PATH)
        try:
            fd = open(FILE_PATH + filename,'r')
        except:
            sock.send("603&文件不存在".encode())
            time.sleep(0.1)
            return
        sock.send(b"603&OK")
        time.sleep(0.5) 
        #发送文件
        try:
            for line in fd:
                sock.send(('603&'+line).encode())
                time.sleep(0.1)
            fd.close()
        except Exception as e:
            print(e)
        time.sleep(0.1)
        sock.send(b'603&##')
        print("文件发送完毕")
#=====================================================             

    def do_register(self,sock, user_info):
        #从数据库获取用户信息
        sql = "select name from users_info"
        #从数据库获取所有用户的信息
        users = self.db.fetchall(sql)
        for i in users:
            if user_info[0] == i[0]:
                sock.send(b"103")
                time.sleep(0.1)
                break
        else:
            sock.send(b"104")
            self.listSocket.remove(sock)
            sql = "insert into users_info(name,password,headimg)\
                   values('%s','%s','%s')" %(user_info[0],user_info[1],user_info[2])
            self.db.handle(sql)
            #注册完毕即创建当前用户的个人好友列表
            my_flist = user_info[0] + "_" + "flist"
            c_sql = "create table %s select * from user_info_template" %my_flist
            self.db.handle(c_sql)
            insert_sql = "insert into %s(name,headimg) values('%s','%s')"%(my_flist,user_info[0],user_info[2])
            self.db.handle(insert_sql)

    def do_login(self, sock, user_info):
        name = user_info[0]
        upasswd = user_info[1]
        sql = "select password,headimg from users_info where name='%s'"%name
        users = self.db.fetchone(sql)
        if users:
            if upasswd == users[0]:
                info = "100&"+users[1]
                sock.send(info.encode('utf-8'))#登陆成功
                sql2 = "update users_info set isOnline='在线' where name='%s'"%name
                sql3 = "update %s set isOnline='在线' where name='%s'"%(name + "_flist",name)
                self.db.handle(sql2)
                self.db.handle(sql3)
                self.get_friend_list(sock,name)
                time.sleep(0.5)#防止好友列表和群列表的粘包
                self.get_group_list(sock,name)
                self.tcp_users[name]=sock#用户名：套接字
            else:
                sock.send(b"101&")
        else:
            sock.send(b"102&")
    
    def do_refresh(self,sock,name):
        self.get_friend_list(sock,name)
        time.sleep(0.1)
        self.get_group_list(sock,name)

    #获取好友列表
    def get_friend_list(self, sock, name):
        #查询当前登陆用户的好友列表
        tab_name = name + "_flist"
        # print(tab_name)
        sql = "select name,isOnline,headimg,friend_group from %s where isDelete='%s';" %(tab_name,'N')
        data = self.db.fetchall(sql)
        print(data)
        if data:
            sl = '105&'
            for i in data:
                for j in i:
                    sl += j
                    sl += '='
                sl += '#'
            sock.send(sl.encode('utf-8'))
            # print(sl)
        else:
            sock.send(b'200&')


    def do_chat(self,sock,msg):
        #从聊天窗口的udp用户中找到相应的用户,找到即用户聊天窗口开启，直接发送消息
        for name,addr in self.users.items():
            print(msg[1],name)
            if msg[-1] == name:
                info = msg[-2].encode('utf-8')
                sock.sendto(info,addr)
                break
        else:
            #此时用户聊天窗口未开启，需通过tcp套接字发送提醒
            self.temp_msg[(msg[-1])] = msg[-2]
    #修改数据库中用户的在线状态
    def do_change_state(self,sock,msg):
        name = msg[0]
        state = msg[1]
        # print(name,state)
        #此处sql语句还需修改
        sql = "update users_info set isOnline='%s' where name='%s'"%(state,name)
        sql2 = "update '%s' set isOnline='%s' where name='%s'"%(name+"_flist",state,name)
        self.db.handle(sql)
        self.db.handle(sql2)

    def do_get_img(self,sock,name):
        sql = "select headimg from users_info where name='%s'"%name
        img = self.db.fetchall(sql)[0][0]
        self.sock.send(img.encode('utf-8'))

    def do_add_friend(self,sock,msg):
        f_name = msg[0]
        name = msg[1]
        sql = "select name,headimg from users_info where name='%s'"%f_name
        info = self.db.fetchone(sql)
        # print(info)
        if info:
            friend_tcp = self.tcp_users.get(f_name,None)
            if friend_tcp:
                info = '201&' + name + '&' + info[1]
                friend_tcp.send(info.encode('utf-8'))
            #对方不在线
            elif info[0] != "在线":
                sock.send(b'203&')
                # print("离线中")
        #查无此人
        elif not info:
            sock.send(b'202&')


    def do_answer(self,msg):
        print(msg)
        flag = msg[0]
        f_name = msg[2]#答复方姓名
        u_name = msg[3]#请求方姓名
        # print(msg)
        tcpscok = self.tcp_users[u_name]
        if flag == "204":
            tcpscok.send(b'204')
        elif flag == "205":
            info = "205&"+ f_name
            tcpscok.send(info.encode('utf-8'))
            sql = "select name,isOnline,headimg from users_info where name='%s'"%f_name
            sql2 = "select name,isOnline,headimg from users_info where name='%s'"%u_name
            friend = self.db.fetchone(sql)
            mine = self.db.fetchone(sql2)
            
            f_tab_name = f_name + "_flist"
            sql3 = "insert into %s(name,isOnline,headimg,friend_group) values('%s','%s','%s','%s')"%(f_tab_name,mine[0],mine[1],mine[2],msg[1])
            sql4 = "insert into %s(name,isOnline,headimg) values('%s','%s','%s')"%(u_name+"_flist",friend[0],friend[1],friend[2])
            self.db.handle(sql3)
            self.db.handle(sql4)

            sql5 = "select friend_group from %s where name='%s'"%(f_tab_name,f_name)
            friend_group = self.db.fetchone(sql5)[0]
            print(friend_group)
            friend_group += " "
            friend_group += msg[1]
            print(friend_group)
            sql6 = "update %s set friend_group='%s' where name='%s'"%(f_tab_name,friend_group,f_name)
            self.db.handle(sql6)

        elif flag == "406":
            #同意入群申请　　　406 群名　群主名　请求人 请求人头像
            info = "406&" + msg[1]
            group_name = msg[1] + "_group"
            #将＇我＇的信息添加到群员信息登记表中
            sql = "insert into %s(name,headimg) values('%s','%s')"%(group_name,msg[3],msg[4])
            self.db.handle(sql)
            #将群名添加到＇我＇的好友列表列中的group_name列中
            sql2 = "select group_name from %s where name='%s'"%(msg[3]+"_flist",msg[3])
            data = self.db.fetchone(sql2)
            print(data[0],"查询结果",msg[3])
            if data[0]:
                groups_name = data[0]
                groups_name += " "
                groups_name += msg[1]
            else:
                groups_name = msg[1]
            sql3 = "update %s set group_name='%s'"%(msg[3]+"_flist",groups_name)
            self.db.handle(sql3)

            self.tcp_users[u_name].send(info.encode('utf-8'))
        elif flag == "407":
            #不同意入群申请
            info = "406&" + msg[1]
            self.tcp_users[u_name].send(info.encode('utf-8'))


    def do_create_friend_group(self,sock,msg):
        try:
            f_group_name = msg[0]
            uname = msg[1]
            tab_name = uname+"_flist"
            sql = "select friend_group from %s where name='%s'"%(tab_name,uname)
            data = self.db.fetchone(sql)
            if data:
                friend_group = data[0]
                friend_group += msg[0]
                friend_group += " "
            else:
                friend_group = msg[0] + " "
            # print(friend_group)
            sql2 = "update %s set friend_group='%s' where name='%s'"%(tab_name,friend_group,uname)
            self.db.handle(sql2)
            sock.send(b'300&')
        except:
            sock.send(b'301&')

    def create_new_group(self,sock,msg):
        u_name = msg[0]
        group_name = msg[1]
        group_tab_name = msg[1] + "_group"
        #从群列表中查询群名，判断是否重名
        sql = "select g_name from groups_info where g_name ='%s'"%group_name
        data = self.db.fetchone(sql)
        print(data,"群名查找哦啊结果")
        if data:
            #群名已存在
            info = "403&" + group_name
        else:
            #可以创建群
            sql2 = "create table %s select * from group_info_template"%group_tab_name
            self.db.handle(sql2)
            #将群名加入到群登记表中
            sql3 = "insert into groups_info(g_name,owner) values('%s','%s')"%(group_name,msg[0])
            self.db.handle(sql3)
            #将我自己的信息放入到所建的群中
            sql4 = "select name,headimg from users_info where name='%s'"%u_name
            info = self.db.fetchone(sql4)
            sql5 = "insert into %s(name,headimg) values('%s','%s')"%(group_tab_name,info[0],info[1])
            self.db.handle(sql5)
            #从好友列表中的群名字段中查询得到我的所有群名
            sql6 = "select group_name from %s where name='%s'"%(msg[0]+"_flist",msg[0])
            data = self.db.fetchone(sql6)
            print(data[0],"群列表")
            #将新建的群名加入到我的所有群名中
            if data[0]:
                    group_names = data[0]
                    group_names += " "
                    group_names += group_name
            else:
                group_names = group_name + " "
            sql7 = "update %s set group_name='%s' where name='%s'"%(msg[0]+"_flist",group_names,msg[0])
            self.db.handle(sql7)
            info = "402&" + group_name
        sock.send(info.encode('utf-8'))

    #获取群列表
    def get_group_list(self,sock,name):
        tab_name = name + '_flist'
        sql = "select group_name from %s where name='%s'"%(tab_name,name)
        data = self.db.fetchone(sql)
        # print(data[0],"群列表")
        if data[0]:
            info = '400&' + data[0]
            sock.send(info.encode('utf-8'))
        else:
            sock.send(b'401&')
    
    def get_group_member(self,sock,msg):
        group_name = msg.split('_')[0] + "_group"
        print(group_name)
        sql = "select name,isOnline,headimg from %s where isDelete='%s'"%(group_name,'N')
        data = self.db.fetchall(sql)
        group_friend_list = "404&"
        for friend_info in data:
            for item in friend_info:
                group_friend_list += item
                group_friend_list += '='
            group_friend_list += '#'
        sock.send(group_friend_list.encode('utf-8'))

    def do_group_chat(self,sock,msg):
        # print("群聊",msg)
        #msg : 消息 群名 用户名
        group_name = msg[1] + "_group"
        u_name = msg[2] #发送消息的用户名
        # 转发消息给所有群员的相应群聊窗口，接受信息中需包含群名和消息
        # 根据群名查找群内所有用户
        sql = "select name,headimg from %s"%group_name
        users = self.db.fetchall(sql)
        # print(users,'群成员')
        for infos in users:
            if infos[0] != u_name:
                name = msg[1] + "_" + infos[0]
                # 根据姓名查找群聊窗口开启的用户
                addr = self.users.get(name,None)
                #用户聊天窗口未开启
                tcpsock = self.tcp_users.get(name,None)
                if addr:
                    headimg = infos[1]
                    info = msg[0] + '&' + name + '&' + headimg 
                    print(info)
                    sock.sendto(info.encode('utf-8'),addr)
                    continue
                # elif tcpsock:
                #     #发送标志位
                #     tcpsock.send('utf-8')
                else:
                    #用户不在线，将聊天信息存入缓存区
                    pass
            else:
                continue

    def add_group(self,sock,msg):
        group_name = msg[1]
        request_name = msg[0]
        headimg = msg[2]
        # print(headimg)
        sql = "select owner from groups_info where g_name='%s'"%group_name
        owner = self.db.fetchone(sql)
        print(owner[0],"所有者")
        try:
            #找到群的创建者
            tcpsock = self.tcp_users[owner[0]]
            info = "405&" + request_name + "&" + group_name + "&" + headimg
            tcpsock.send(info.encode('utf-8'))
        except:
            pass

if __name__ == '__main__':
    server = ChatServer()
    server.run()