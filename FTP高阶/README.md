####Day8作业--高级FTP
#### 江飞
####[博客地址,点击URL](http://www.cnblogs.com/bigberg/category/1097785.html)
####一.作业需求
    1. 用户加密认证
    2. 多用户同时登陆
    3. 每个用户有自己的家目录且只能访问自己的家目录
    4. 对用户进行磁盘配额、不同用户配额可不同
    5. 用户可以登陆server后，可切换目录
    6. 查看当前目录下文件
    7. 上传下载文件，保证文件一致性
    8. 传输过程中现实进度条
    9. 支持断点续传
 
####二.需求分析
    1.验证过程加密认证，用户db中密码用md5保存，登入时要输入的密码做MD5再与用户db中的记录比较
    2.多用户同时登入时 server_forever()
        1)用户由服务端程序来创建
        2)在创建用户时定义一个配额大小，默认10M
    3.只能访问自己的家目录
        1）在setting中定义ftp home 目录
        2）所有用户目录以用户名的形式存放在ftp home目录
        3）要实现类似ssh客户端功能，可以输入命令返回结果
        4）设置一个变量能记录当前工作目录
        5）切换目录时，与当前工作目录对比，不在自己家目录下则禁止
        6）切换目录成功，输入端显示当前工作目录，否则显示原先的工作目录
        7）切换目录只是目录名称改变
    4. 对磁盘配额可以在用户创建时配置，在setting.ini中设置一个默认值
        1）在上传前要验证目录中空间是否足够，所以要获取目录剩余空间值和文件大小
        2）定义一个模块能遍历 家目录中所以文件，计算使用空间
    5. 用md5来验证文件的一致性
    6. 上传和下载中设置进度条
    7. 在下载过程中实现了断点续传：
        1)记录一个seek值，如果该值不为0，则从该值处续传
        2)下载的文件先命名为filename + .temp,如果全部传完，再将.temp去掉
    8. 客户端能从服务端获取当前工作目录很重要，这个变量可以用来判断和简化程序
        1）是否在家目录中
        2）文件上传和下载的位置
        3） pwd 的显示
        4) ls 的显示内容
   
####三.使用说明
    1.客户端启动程序：my_ftp_client/bin/client_start.py
    2.客户端主程序：my_ftp_client/core/ftp_client.py
    3.服务端：
        1)创建用户启动：my_ftp_server/bin/newuser.py
        2)创建用户主程序:  my_ftp_server/core/create_user.py
        3)服务端启动: my_ftp_server/bin/server_start.py
        4)服务端主程序: my_ftp_server/core/ftp_server.py
    4.服务端配置文件：my_ftp_server/config/setting.ini
    5.服务端模块：my_ftp_server/modules
    6.用户数据: my_ftp_server/db
    
####四.测试说明
    1.重要：请先在服务端配置文件 setting.ini中设置 ftp home 目录
    2.重要： 在断点续传中，无法用ctl+c 打断程序，需要关闭服务端中断文件传输
    3.上传文件 put + 文件全路径，可以上传任何目录的文件
    4.其余操作命令和 linux一致 
    5.断点续传时，需要和上一个未传完的文件保存在同一个目录下，否则就是新下载
    5.下载文件  get filename
    
####五.测试用例
    1. 用户名/密码：bigberg / 123123
                   aliex  /  123456
                   
####六.测试
   1. 新建用户
    
    输入用户名:eric
    输入密码:123123
    请重新输入密码:123123
    请输入磁盘配额,默认10M[Y/y]：Y   # 可以自己输入 单位 K,M,G
    
   2.登入
    
    请输入用户名:eric
    请输入密码:123123
    登入成功
    [root@ftp_server eric]$:   # 登入成功显示家目录
    
   3.help查看功能
   
    ls  -  列出该目录下所有文件和文件夹
    pwd -  显示当前工作目录
    cd  -  cd .  当前工作目录
           cd .. 上一级工作目录
           cd dirname  切换到当前工作目录下的dirname目录

    get -  get filename  下载文件
    put -  put G:/ftp/home/***.txt  上传文件
    mkdir - mkdir dirname 创建目录
   
   4. 创建一个目录 + ls显示
   
    [root@ftp_server eric]$:mkdir test
    makedir successfully.
    [root@ftp_server eric]$:ls
    test
    
   5.切换目录
    
    [root@ftp_server eric]$:cd test
    [root@ftp_server test]$
   
   6. 尝试切换出家目录
   
    [root@ftp_server test]$:cd ../..
    403,禁止切换到家目录以外
    [root@ftp_server test]$:
    
   7.上传文件
   
    [root@ftp_server test]$:put G:\ftp\home\MySQL5.7安装文档.doc
    [>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100%
    file upload successfully
    [root@ftp_server test]$:ls
    123
    MySQL5.7安装文档.doc
    
   8.下载文件
   
    [root@ftp_server test]$:get MySQL5.7安装文档.doc
    输入保存文件的位置:G:\ftp
    [>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100%
    
   9.断点续传（大文件测试）
     
     测试和上例一致，只是需要在传输过程中停止客户端或者服务端，在重新下载