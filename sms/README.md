####Day11作业--学员管理系
#### 江飞
####[博客地址,点击URL](http://www.cnblogs.com/bigberg/category/1136977.html)
####一.作业需求
    用户角色，讲师＼学员， 用户登陆后根据角色不同，能做的事情不同，分别如下
    讲师视图
        管理班级，可创建班级，根据学员qq号把学员加入班级
        可创建指定班级的上课纪录，注意一节上课纪录对应多条学员的上课纪录， 即每节课都有整班学员上， 为了纪录每位学员的学习成绩，需在创建每节上课纪录是，同时         为这个班的每位学员创建一条上课纪录
        为学员批改成绩， 一条一条的手动修改成绩
    学员视图
         提交作业
        查看作业成绩
        一个学员可以同时属于多个班级，就像报了Linux的同时也可以报名Python一样， 所以提交作业时需先选择班级，再选择具体上课的节数
        附加：学员可以查看自己的班级成绩排名

####二、需求分析
    1.使用sqlalchemy进行数据库处理
    2.设计数据库表结构
    3.教师登入使用教师编号，学生使用qq号
    4.教师作为管理员，在程序最初运行时，可以先初始化，生成一部分数据
    5.每条上课记录要对应课程、日期和学员
    6.只有创建了上课记录才能提交作业和修改成绩
    7.教师创建一条上课记录，全班学员状态为 已签到
    8.学员提交作业后，上课记录中的提交状态变为 已提交
    9.教师只能修改作业状态为已提交的成绩
    10.老学员新增课程时，原有课程不在选择之列

####三、使用说明
    1.新建数据库和表，数据库名称为sms, 数据库默认编码utf-8
    2.新建表，运行/data/db_tables_create.py
    3.初始化数据 /bin/initialize.py ,第一次使用该程序使用，不然没有登入用户
    4.启动文件在 /bin目录下
    5.数据库engine设置在config/setting.py中，需修改为自己的数据库连接地址
    6.初始化的数据在 /data/sms_data.py中
    7.role.py中主要是教师类的方法
    8.学生类的方法在studentrole.py中
    9.教师编号类似 T0001、T0002,学员qq类似 10001、10002、10003    

####四、测试

#####教师测试
######1）登入
    请输入用户名:T0001
    请输入密码:111111
    
    **************************
    *   欢迎使用学员管理系统   *
    **************************
    
       1. 创建新课程
       2. 新增教师
       3. 新增学员
       4. 老学员新增课程
       5. 增加课程日期
       6. 新增课程记录
       7. 评分
       8. 退出
    -----------------------
    输入编号选择您所需的功能:
    
######2）新建课程
    输入编号选择您所需的功能:1
    -------- 创建课程--------
    课程名称:Docker第一期
    1 : 教师编号:T0001 教师姓名:Jack
    2 : 教师编号:T0002 教师姓名:Henry
    请选择教师:2
    新课程添加完成!
    新增课程: Docker第一期
    授课教师: [教师编号:T0002 教师姓名:Henry]
    
######3）新增学员
    输入编号选择您所需的功能:3
    --------新增学生---------
    学生qq号:10009
    学生姓名:Steve
    输入密码:111111
    --------选择班级---------
    1 : Python第一期
    2 : Mysql第一期
    3 : Linux第一期
    4 : Docker第一期
    选择班级，多个班级以','分开:3,4
    该学生选择的课程如下:
    Linux第一期
    Docker第一期
    信息注册完成!

######4）新增教师
    输入编号选择您所需的功能:2
    --------新增教师---------
    教师编号:T0003
    教师姓名:Peter
    输入密码:111111
    新教师添加完成!

######5）老学员新增课程
    --------添加学员---------
    学生qq号:10008
    1 : Docker第一期
    2 : Python第一期
    3 : Mysql第一期
    选择班级:1
    学员: 10008
    所选课程: Docker第一期
    学员信息更新完毕
 
######6）增加课程日期
    输入编号选择您所需的功能:5
    day1
    day2
    day3
    day4
    课程日期(like:day1):day4
    该日期已经建立,不能重复
    课程日期(like:day1):day5
    新日期创建完成
    
######7）创建课程记录
    --------选择课程---------
    请选择班级
    1 : Python第一期
    2 : Linux第一期
    请选择班级:1
    该班的学生如下:
    QQ:10001 姓名:Harry
    QQ:10002 姓名:Potter
    QQ:10005 姓名:Maro
    --------选择日期---------
    1 : day1
    2 : day2
    3 : day3
    4 : day4
    5 : day5
    选择日期(Q/q退出):1
    初始化[Python第一期][day1]完成!
    

######8）评分
    输入编号选择您所需的功能:7
    --------选择课程---------
    请选择班级
    1 : Python第一期
    2 : Linux第一期
    请选择班级:1
    该班的学生如下:
    QQ:10001 姓名:Harry
    QQ:10002 姓名:Potter
    QQ:10005 姓名:Maro
    --------选择日期---------
    1 : day1
    2 : day2
    3 : day3
    4 : day4
    5 : day5
    选择日期(Q/q退出):1
    10001 Harry 已提交 0
    10002 Potter 未提交 0
    10005 Maro 未提交 0
    为已提交学员评分
    10001 Harry
    请为学员评分(0-100):94
    该次已提交学员成绩评分完成


#####学员测试
######1）登入
    请输入用户名:10001
    请输入密码:111111
    **************************
    *   欢迎使用学员管理系统   *
    **************************
    
      1. 提交作业
      2. 查询排名
      3. 退出
    
    -----------------------
   
######2）提交作业
    输入编号选择您所需的功能:1
    --------选择课程---------
    1 : Python第一期
    2 : Mysql第一期
    选择班级:1
    ----选择提交作业的日期---
    1 : day1
    2 : day2
    3 : day3
    4 : day4
    5 : day5
    选择日期:1
    本次作业提交完成
   
######2）查询排名
    输入编号选择您所需的功能:2
    --------选择课程---------
    1 : Python第一期
    2 : Mysql第一期
    选择班级:1
    10001 Harry
    94
    10002 Potter
    92
    10005 Maro
    99
    10001 Harry 排名为: 2