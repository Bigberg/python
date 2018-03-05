####Day13作业--堡垒机
#### 江飞
####[博客地址,点击URL](http://www.cnblogs.com/bigberg/archive/2018/01.htmll)
####一.作业需求
    所有的用户操作日志要保留在数据库中

    每个用户登录堡垒机后，只需要选择具体要访问的设置，就连接上了，不需要再输入目标机器的访问密码
    
    允许用户对不同的目标设备有不同的访问权限，例:
    
    对10.0.2.34 有mysql 用户的权限
    
    对192.168.3.22 有root用户的权限
    
    对172.33.24.55 没任何权限
    
    分组管理，即可以对设置进行分组，允许用户访问某组机器，但对组里的不同机器依然有不同的访问权限　
    
####二.需求分析
    1.使用sqlalchemy对数据库操作
    2.设计相应表结构
    3.分堡垒机用户和远程用户，堡垒机用户登入堡垒机，远程用户登入远程主机
    4.为堡垒机用户绑定可使用的远程用户和主机地址，即权限
    5.将堡垒机用户和主机组绑定，同时主机组和远程主机、远程用户绑定
    6.将堡垒机用户所有操作，包括登入的远程主机，只有的远程用户和操作命令等记录到数据库
    7.验证堡垒机用户登入，登入成功后直接调用ssh_login登入远程主机
    8.数据库连接信息在config/setting.py,先创建数据库
####三.使用说明
    1.开始入口在bin/job_start.py
    2.所有功能在视图views中，视图在modules下
    3.数据库表在models中的models中
    4.运行python job_start.py 查看可以使用的方法
    
####四.测试
#####4.1 生成表
    1.生成表
        python bin\job_start.py syncdb
        
    2.生成堡垒机用户
        python bin\job_start.py create_users -f share\example\new_user_profile.yml
    
    3.生成host主机表
        python bin\job_start.py create_users -f share\example\new_host.yml
        
    4.生成远程用户表
        python bin\job_start.py create_users -f share\example\new_remote_user.yml
       
    5.生成绑定主机表
        python bin\job_start.py create_users -f share\example\new_bindhosts.yml
        
#####4.2 运行堡垒机
    1.登入
        python bin\job_start.py start_session
        
        Username:jack
        Password:jack123
        
            ------------- Welcome [jack] login successfully -------------
        
        [172.16.60.30 root, 172.16.200.161 bigberg]
        [bj_group]
        z.      ungroupped hosts (2)
        0.      bj_group (3)
        [jack]:
        
    2. 选择主机
        [bj_group]
        z.      ungroupped hosts (2)
        0.      bj_group (3)
        [jack]:0
        ------ Group: bj_group ------
          0.    root@nginx-server(172.16.60.30)
          1.    bigberg@server1(172.16.200.161)
          2.    root@server2(172.16.60.150)
        ----------- END -----------
        [(b)back, (q)quit, select host to login]:1
        
    3.执行命令(如果要保存命令，需在linux服务器上运行)
        [bigberg@docker ~]$ ls
        ls
        [bigberg@docker ~]$ cd /data
        cd /data
       
    4. 查看操作日志
        G:\python\github\pythonstudy\day13_baoleiserver>python bin\job_start.py show_logs
        G:\python\github\pythonstudy\day13_baoleiserver
        1 : alex
        2 : jack
        3 : rain
        输入编号:2
        jack 172.16.60.30 root 2018-02-05 10:52:17 Choice(code=login, value=Login) None
        jack 172.16.60.30 root 2018-02-05 10:52:23 Choice(code=cmd, value=CMD) ls
        jack 172.16.60.30 root 2018-02-05 10:52:24 Choice(code=cmd, value=CMD) pwd
        jack 172.16.60.30 root 2018-02-05 10:52:27 Choice(code=cmd, value=CMD) clear
        jack 172.16.60.30 root 2018-02-05 10:52:29 Choice(code=cmd, value=CMD) pwd
        jack 172.16.60.30 root 2018-02-05 10:52:32 Choice(code=cmd, value=CMD) cd
        jack 172.16.60.30 root 2018-02-05 10:52:35 Choice(code=cmd, value=CMD) cd /da   ta/
        jack 172.16.60.30 root 2018-02-05 10:52:36 Choice(code=cmd, value=CMD) ls
        jack 172.16.60.30 root 2018-02-05 10:52:38 Choice(code=cmd, value=CMD) cd ..
        jack 172.16.60.30 root 2018-02-05 10:52:39 Choice(code=cmd, value=CMD) cd
        jack 172.16.200.161 bigberg 2018-02-05 14:20:12 Choice(code=login, value=Login) None