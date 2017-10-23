####Day4作业
#### 江飞
####[博客地址,点击URL](http://www.cnblogs.com/bigberg/p/6626074.html)
####一.作业需求
    1、1,Alex Li,22,13651054608,IT,2013-04-01
    2、现需要对这个员工信息文件，实现增删改查操作
    3、可进行模糊查询，语法至少支持3种
    4、查到的信息，打印后，最后面还要显示查到的条数
    5、可创建新员工纪录，以phone做唯一键，staff_id需自增
    6、可删除指定员工信息纪录，输入员工id，即可删除
    7、使用update语句增加记录
    
####二.需求分析
    1.所有的输入都要以sql语句进行，除了delete操作
    2.可以先定义一个函数，用来判断sql语句进行的是什么操作（select、insert、delete、update）
    3.该函数可以分解输入的sql语句，并将有用的信息存入一个字典中，方便提取和使用
    4.输出形式要和mysql相似，则需要定义一些函数来打印 外框
    5.将所有员工信息存在一个txt文中，用来读写操作
    6.操作可能涉及到员工信息的每一个元素，可以先定义一个函数，能将每条信息存入一个列表中
    7.staff_id要实现自增，预先定义一个函数，用来读取最大的staff_id，并以字典形式存入json文件中
    8.phone这个函数是唯一键，insert和update操作需要判断phone是否有冲突
    9.用字段名的 index 来实现检索 字段名的时候可以不按顺序

####三.使用说明
    1.运行bin目录下的staff.py,主程序在core/main.py
    2.除delete外，请输入完整的sql语句，不用加分号（；），查询值的引号需要
    3.表格名称没有做判断，固定为staff_table
    4.module文件夹下有使用到的各个模块，模块内有功能说明
    5.员工信息记录在了config/staff_info.txt中
    6.updat操作没有 !=
    7.insert操作不需要插入staff_id，程序自动会插入一个比现有staff_id大1的值
    8.删除直接输入 delete
    9.exit 退出程序
    10.staff_info文件最后一行为空，否则会报错，没有做空行的判断
####四.程序测试
#####4.1测试样例
     1. select * from staff_table
     2. select * from staff_table where name = "Alex Li"
     3. select name,age,phone from staff_table 
     4. select name,phone,staff_id from staff_table where name like "Li"
     5. select * from staff_table where age > 25
     6. select name,age,phone from staff_id where enroll_date < "2015-01-01"
     7. insert into staff_table (name,age,phone,dept,enroll_date) values ("Li Si",33,"13811314321",'Doctor',"2015-08-23")
     8. delete
     9. update staff_table set name = "Wang Wu" where staff_id = "1"
     10. update staff_table set dept = "Docter" where name like "Wan"
   
#####4.2测试内容
     测试结果无法插入md文件中，以上sql语句可以查看测试结果。