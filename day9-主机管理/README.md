####Day9作业--Fabric主机管理
#### 江飞
####[博客地址,点击URL](http://www.cnblogs.com/bigberg/category/1097785.html)
####一.作业需求
    1. 运行程序列出主机组或者主机列表
    2. 选择指定主机或主机组
    3. 选择让主机或者主机组执行命令或者向其传输文件（上传/下载）
    4. 充分使用多线程或多进程
    5. 不同主机的用户名密码、端口可以不同
 
####二、需求分析

    1.在配置文件setting.ini中定义主机组信息
    2.利用configparser读取配置文件信息
    3.读取的主机组信息以列表形式
    4.登入完成后输出主机组和主机信息
    5.利用paramiko模块实现具体功能
    6.定义一个ssh类，包含连接、执行命令、上传和下载功能
    7.利用queue队列接收多线程中的输入
    
####三、使用说明

    1. 程序启动在 /bin/start.py
    2. 需要修改主机信息以供测试，在conf/setting.ini文件
    3. 选择编号来确定所需要主机组或主机
    4. 0 代表选择该主机组中所以主机
    6. 下载文件请使用单线程
    7. 执行命令 cmd df(需要加  cmd)
    8. 上传文件  put  G：\ftp\test.txt /tmp/test.txt
    9. 下载文件  get  /tmp/test.txt G:\ftp\t111.txt
    
####四、测试用例
    
    1. 登入用户 admin / admin

####五、测试过程

#####5.1 登入

    请输入用户名:admin
    请输入密码:admin
    Welcome Admin.
    1  :  group_test2
    2  :  group_test1
    请输入编号选择主机组:
    
#####5.2 选择主机组

    请输入编号选择主机组:2
    1 : host1--->172.16.200.143
    2 : host2--->172.16.200.160
    请输入编号选择主机,0表示所有主机:
    
#####5.3 选择全部主机
    
    请输入编号选择主机,0表示所有主机:0
    
#####5.4 执行命令

    >>:cmd df
    -----host2-----
    Filesystem     1K-blocks    Used Available Use% Mounted on
    /dev/sda2       17941892 9768424   7239020  58% /
    devtmpfs         2005724       0   2005724   0% /dev
    tmpfs            2015184       0   2015184   0% /dev/shm
    tmpfs            2015184    8816   2006368   1% /run
    tmpfs            2015184       0   2015184   0% /sys/fs/cgroup
    /dev/sda1         487634  133008    324930  30% /boot
    tmpfs             403040       0    403040   0% /run/user/0
    
    -----host1-----
    文件系统          1K-块     已用     可用 已用% 挂载点
    /dev/sda2      49106596 17200088 29388956   37% /
    devtmpfs         490220        0   490220    0% /dev
    tmpfs            499960        0   499960    0% /dev/shm
    tmpfs            499960    13116   486844    3% /run
    tmpfs            499960        0   499960    0% /sys/fs/cgroup
    /dev/sda1        289285   137873   131956   52% /boot
    tmpfs             99992        0    99992    0% /run/user/0
   
#####5.5 上传文件

    >>:put G:\ftp\test.txt /tmp/test456.txt
    -----host2-----
    需要上传的文件：G:\ftp\test.txt
    存放文件的路径:/tmp/test456.txt
    上传完成!
    -----host1-----
    需要上传的文件：G:\ftp\test.txt
    存放文件的路径:/tmp/test456.txt
    上传完成!
    
##### 5.6 下载文件（单线程）

    >>:get /tmp/test456.txt G:\ftp\test567.txt
    -----host1-----
    下载的文件：/tmp/test456.txt
    存放文件的路径:G:\ftp\test567.txt
    下载完成!
    
##### 5.7 选择单点主机操作同上

##### 5.8 退出
    
    exit