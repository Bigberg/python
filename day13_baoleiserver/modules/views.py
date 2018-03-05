# -*- coding: UTF-8 -*-

from models import models
from config import setting
from modules.db_conn import create_engine, session
from modules.utils import print_err, yaml_parser
from modules import ssh_login
from sqlalchemy import and_


def auth():
    '''
    do the user login authentication
    :return:
    '''
    count = 0
    while count < 3:
        username = input("\033[32;1mUsername:\033[0m").strip()
        if len(username) == 0:
            continue
        password = input("\033[32;1mPassword:\033[0m").strip()
        if len(password) == 0:
            continue
        user_obj = session.query(models.UserProfile).filter(models.UserProfile.username == username,
                                                            models.UserProfile.password == password).first()
        if user_obj:
            return user_obj
        else:
            print("wrong username or password, you have %s more chances." % (3-count-1))
            count += 1
    else:
        print_err("too many attempts.")


def welcome_msg(user):

    WELCOME_MSG = '''\033[32;1m
    ------------- Welcome [%s] login successfully -------------
    \033[0m''' % user.username
    print(WELCOME_MSG)


def log_recording(user_obj,bind_host_obj,logs):
    '''
    flush user operations on remote host into DB
    :param user_obj:
    :param bind_host_obj:
    :param logs: list format [logItem1,logItem2,...]
    :return:
    '''
    print("\033[41;1m--logs:\033[0m", logs)

    session.add_all(logs)
    session.commit()


def start_session(argvs):
    print('going to start sesssion ')
    user = auth()
    if user:
        welcome_msg(user)
        print(user.bind_hosts)
        print(user.host_groups)
        exit_flag = False
        while not exit_flag:
            if user.bind_hosts:
                print('\033[32;1mz.\tungroupped hosts (%s)\033[0m' % len(user.bind_hosts))
            for index, group in enumerate(user.host_groups):
                print('\033[32;1m%s.\t%s (%s)\033[0m' % (index, group.name,  len(group.bind_hosts)))

            choice = input("[%s]:" % user.username).strip()
            if len(choice) == 0:
                continue
            if choice == 'z':
                print("------ Group: ungroupped hosts ------")
                for index, bind_host in enumerate(user.bind_hosts):
                    print("  %s.\t%s@%s(%s)" % (index,
                                                bind_host.remoteuser.username,
                                                bind_host.host.hostname,
                                                bind_host.host.ip,
                                                ))
                print("----------- END -----------")
            elif choice.isdigit():
                choice = int(choice)
                if choice < len(user.host_groups):
                    print("------ Group: %s ------" % user.host_groups[choice].name)
                    for index, bind_host in enumerate(user.host_groups[choice].bind_hosts):
                        print("  %s.\t%s@%s(%s)" % (index,
                                                    bind_host.remoteuser.username,
                                                    bind_host.host.hostname,
                                                    bind_host.host.ip,
                                                    ))
                    print("----------- END -----------")

                    # host selection
                    while not exit_flag:
                        user_option = input("[(b)back, (q)quit, select host to login]:").strip()
                        if len(user_option) == 0:
                            continue
                        if user_option == 'b':
                            break
                        if user_option == 'q':
                            exit_flag = True
                        if user_option.isdigit():
                            user_option = int(user_option)
                            if user_option < len(user.host_groups[choice].bind_hosts):
                                print('host:', user.host_groups[choice].bind_hosts[user_option])
                                print('audit log:', user.host_groups[choice].bind_hosts[user_option].audit_logs)
                                ssh_login.ssh_login(user,
                                                    user.host_groups[choice].bind_hosts[user_option],
                                                    session, log_recording)
                else:
                    print("no this option..")


def create_hosts(argvs):
    '''
    create hosts
    :param argvs:
    :return:
    '''
    if '-f' in argvs:
        hosts_file = argvs[argvs.index("-f") + 1]
    else:
        print_err("invalid usage, should be:\ncreate_hosts -f <the new hosts file>",
                  quit=True)
    source = yaml_parser(hosts_file)
    if source:
        # print(source)
        for key, val in source.items():
            print(key, val)
            obj = models.Host(hostname=key, ip=val.get('ip'), port=val.get('port') or 22)
            session.add(obj)
        session.commit()


def create_remoteusers(argvs):
    '''
    create remoteusers
    :param argvs:
    :return:
    '''
    if '-f' in argvs:
        remoteusers_file = argvs[argvs.index("-f") + 1]
    else:
        print_err("invalid usage, should be:\ncreate_remoteusers -f <the new remoteusers file>", quit=True)
    source = yaml_parser(remoteusers_file)
    if source:
        for key, val in source.items():
            print(key, val)
            obj = models.RemoteUser(username=val.get('username'),
                                    auth_type=val.get('auth_type'), password=val.get('password'))
            session.add(obj)
        session.commit()


def create_users(argvs):
    '''
    create little_finger access user
    :param argvs:
    :return:
    '''
    if '-f' in argvs:
        user_file = argvs[argvs.index("-f") + 1]
    else:
        print_err("invalid usage, should be:\ncreateusers -f <the new users file>", quit=True)

    source = yaml_parser(user_file)
    if source:
        for key, val in source.items():
            print(key, val)
            obj = models.UserProfile(username=key, password=val.get('password'))
            # if val.get('groups'):
            #     groups = session.query(models.HostGroup).filter(models.HostGroup.name.in_(val.get('groups'))).all()
            #     if not groups:
            #         print_err("none of [%s] exist in group table." % val.get('groups'), quit=True)
            #     obj.groups = groups
            # if val.get('bind_hosts'):
            #     bind_hosts = common_filters.bind_hosts_filter(val)
            #     obj.bind_hosts = bind_hosts
            # print(obj)
            session.add(obj)
        session.commit()


def create_groups(argvs):
    '''
    create groups
    :param argvs:
    :return:
    '''
    if '-f' in argvs:
        group_file = argvs[argvs.index("-f") + 1]
    else:
        print_err("invalid usage, should be:\ncreategroups -f <the new groups file>",quit=True)
    source = yaml_parser(group_file)
    if source:
        for key, val in source.items():
            print(key, val)
            obj = models.HostGroup(name=key)
            # if val.get('bind_hosts'):
            #     bind_hosts = common_filters.bind_hosts_filter(val)
            #     obj.bind_hosts = bind_hosts
            #
            # if val.get('user_profiles'):
            #     user_profiles = common_filters.user_profiles_filter(val)
            #     obj.user_profiles = user_profiles
            session.add(obj)
        session.commit()


def create_bindhosts(argvs):
    '''
    create bind hosts
    :param argvs:
    :return:
    '''
    if '-f' in argvs:
        bindhosts_file = argvs[argvs.index("-f") + 1]
    else:
        print_err("invalid usage, should be:\ncreate_hosts -f <the new bindhosts file>", quit=True)
    source = yaml_parser(bindhosts_file)
    if source:
        for key, val in source.items():
            # print(key,val)
            host_obj = session.query(models.Host).filter(models.Host.hostname == val.get('hostname')).first()
            assert host_obj
            for item in val['remote_users']:
                print(item)
                assert item.get('auth_type')
                if item.get('auth_type') == 'ssh-password':
                    remoteuser_obj = session.query(models.RemoteUser).filter(
                                                        models.RemoteUser.username == item.get('username'),
                                                        models.RemoteUser.password == item.get('password')
                                                    ).first()
                else:
                    remoteuser_obj = session.query(models.RemoteUser).filter(
                                                        models.RemoteUser.username == item.get('username'),
                                                        models.RemoteUser.auth_type == item.get('auth_type'),
                                                    ).first()
                if not remoteuser_obj:
                    print_err("RemoteUser obj %s does not exist." % item, quit=True)
                bindhost_obj = models.BindHost(host_id=host_obj.id, remoteuser_id=remoteuser_obj.id)
                session.add(bindhost_obj)
                # for groups this host binds to
                if source[key].get('groups'):
                    group_objs = session.query(models.HostGroup).filter(models.HostGroup.name.in_(
                        source[key].get('groups'))).all()
                    assert group_objs
                    print('groups:', group_objs)
                    bindhost_obj.host_group = group_objs
                # for user_profiles this host binds to
                if source[key].get('user_profiles'):
                    userprofile_objs = session.query(models.UserProfile).filter(models.UserProfile.username.in_(
                        source[key].get('user_profiles')
                    )).all()
                    assert userprofile_objs
                    print("userprofiles:", userprofile_objs)
                    bindhost_obj.user_profile = userprofile_objs
                # print(bindhost_obj)
        session.commit()


def syncdb(argvs):
    print("Syncing DB....")
    engine = create_engine(setting.ConnParams, echo=True)
    # 创建所有表结构
    models.Base.metadata.create_all(engine)


def show_logs(argvs):
    user_objs = session.query(models.UserProfile).filter(
        and_(models.UserProfile.id > 0, models.UserProfile.username != 'admin')).all()
    # print(user_objs)
    choice_list = []
    for i in range(len(user_objs)):
        print(i+1, ':', user_objs[i])
        choice_list.append(i+1)
    while True:
        choice = input('输入编号:').strip()
        if choice.isdigit() is False or int(choice) not in choice_list:
            print('\033[31;1m编号选择有误,请重新输入\033[0m')
            continue
        else:
            log_objs = session.query(models.AuditLog).filter(
                models.AuditLog.user_id == user_objs[int(choice) - 1].id).all()
            for i in range(len(log_objs)):
                print(log_objs[i].user_profile.username, log_objs[i].bind_host.host.ip,
                      log_objs[i].bind_host.remoteuser.username, log_objs[i])
            break

if __name__ == '__main__':
    pass
