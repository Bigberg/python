####Day11作业--rpc 主机管理
#### 江飞
####[博客地址,点击URL](http://www.cnblogs.com/bigberg/category/1136977.html)
####一.作业需求
    可以对指定机器异步的执行多个命令
    例子：
    >>:run "df -h" --hosts 192.168.3.55 10.4.3.4 
    task id: 45334
    >>: check_task 45334 
    >>:
    注意，每执行一条命令，即立刻生成一个任务ID,不需等待结果返回，
    通过命令check_task TASK_ID来得到任务结果 
 
####二.需求分析
    1.使用rabbitmq的rpc功能
    2.消息细分，将命令发送不同的机器，可以使用exchange的topic
      根据ip来发送到不同的queue
    3.设置routing_key = ip
    4. 返回的结果存在一个字典中，key为corr_id,value 为返回的结果
    5. 使用subprocess模块执行命令

####三.使用说明
    1. 启动程序在bin目录下
    2. 客户端可以使用help查看功能
    3. 命令：
       run "df -h" --host 192.168.0.2 10.0.0.1
       check_task id
    4. "df -h" 请使用双引号
    5. 服务端如果在linux上运行，get_ip的函数需要填写网卡
       如： host_addr = get_ip('eth0'),在windows上不要加参数
   
####四.测试
#####4.1 服务端在单台windows 机器
    >>:run "dir" --host 172.16.200.109
    task_id: 56922
    >>:check_task 56922
    from host 172.16.200.109
    驱动器 G 中的卷是 文档
    卷的序列号是 0002-E248

    G:\python\github\pythonstudy\day11_rpc\server\bin 的目录

    2018/01/10  13:45    <DIR>          .
    2018/01/10  13:45    <DIR>          ..
    2018/01/10  11:35               217 rpc_server_start.py
    2018/01/10  13:44                23 __init__.py
                2 个文件            240 字节
                2 个目录 181,944,434,688 可用字节

    >>:

#####4.2 服务端在多台linux机器
    >>:run "df -h" --host 172.16.200.49 172.16.200.161
    task_id: 53501
    >>:check_task 53501
    from host 172.16.200.49
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sda2        47G  7.6G   37G  17% /
    tmpfs           491M   72K  491M   1% /dev/shm
    /dev/sda1       283M   55M  214M  21% /boot

    from host 172.16.200.161
    文件系统                 容量  已用  可用 已用% 挂载点
    /dev/mapper/centos-root   18G  2.2G   16G   13% /
    devtmpfs                 478M     0  478M    0% /dev
    tmpfs                    489M     0  489M    0% /dev/shm
    tmpfs                    489M  6.8M  482M    2% /run
    tmpfs                    489M     0  489M    0% /sys/fs/cgroup
    /dev/sda1                497M  155M  343M   32% /boot
    tmpfs                     98M     0   98M    0% /run/user/0

    >>:run "ls" --host 172.16.200.49 172.16.200.161
    task_id: 36825
    >>:check_task 36825
    from host 172.16.200.49
    __init__.py
    rpc_server.py

    from host 172.16.200.161
    __init__.py
    rpc_server.py   