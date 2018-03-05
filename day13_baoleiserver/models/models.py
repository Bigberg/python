# -*- coding: UTF-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, UniqueConstraint, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType


Base = declarative_base()

# 堡垒机用户和远程主机的关联
user_m2m_bindhost = Table("user_m2m_bindhost", Base.metadata,
                          Column("id", Integer, primary_key=True),
                          Column('user_profile_id', Integer, ForeignKey("user_profile.id")),
                          Column('bind_host_id', Integer, ForeignKey("bind_host.id")))

# 远程主机和主机组关联
bindhost_m2m_hostgroup = Table("bindhost_m2m_hostgroup", Base.metadata,
                               Column("id", Integer, primary_key=True),
                               Column('host_groups_id', Integer, ForeignKey("host_groups.id")),
                               Column('bind_host_id', Integer, ForeignKey("bind_host.id")))

# 堡垒机用户和主机组关联
user_m2m_hostgroup = Table("user_m2m_hostgroup", Base.metadata,
                           Column("id", Integer, primary_key=True),
                           Column('user_profile_id', Integer, ForeignKey("user_profile.id")),
                           Column('host_group_id', Integer, ForeignKey("host_groups.id")))


class Host(Base):
    # 主机表
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True)
    hostname = Column(String(64), unique=True)
    ip = Column(String(64), unique=True)
    port = Column(Integer, default=22)

    def __repr__(self):
        return self.hostname


class HostGroup(Base):
    # 主机组表
    __tablename__ = 'host_groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    function = Column(String(64))

    bind_hosts = relationship('BindHost', secondary='bindhost_m2m_hostgroup',
                              backref='host_group')

    def __repr__(self):
        return self.name


class RemoteUser(Base):
    # 远程用户表
    __tablename__ = 'remote_user'
    # 联合唯一
    __table_args__ = (UniqueConstraint("auth_type", "username", "password", name="_user_password_uc"), )
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(128))

    # 第1个值存数据库，第2个值是sqlalchemy显示的
    AuthTypes = [
        ("ssh-password", "SSH/Password"),
        ("ssh-key", "SSH/KEY")
    ]  # 设置枚举值
    auth_type = Column(ChoiceType(AuthTypes))

    def __repr__(self):
        return self.username


class BindHost(Base):
    '''
    绑定主机组、主机和远程用户
    '''
    __tablename__ = 'bind_host'
    __table_args__ = (UniqueConstraint("host_id", "remoteuser_id", name="_host_remoteuser"),)
    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey('host.id'))
    remoteuser_id = Column(Integer, ForeignKey('remote_user.id'))
    host = relationship('Host', backref='bind_hosts')
    remoteuser = relationship('RemoteUser', backref='bind_hosts')

    def __repr__(self):
        return "%s %s" % (self.host.ip, self.remoteuser.username)


class UserProfile(Base):
    # 堡垒机用户表
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    password = Column(String(128))

    bind_hosts = relationship("BindHost", secondary='user_m2m_bindhost', backref='user_profile')
    host_groups = relationship("HostGroup", secondary='user_m2m_hostgroup', backref='user_profile')

    def __repr__(self):
        return self.username


class AuditLog(Base):
    # 日志表
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'))
    bind_host_id = Column(Integer, ForeignKey('bind_host.id'))
    action_choices = [
        (0, 'CMD'),
        (1, 'Login'),
        (2, 'Logout'),
        (3, 'GetFile'),
        (4, 'SendFile'),
        (5, 'Exception'),
    ]
    action_choices2 = [
        (u'cmd', u'CMD'),
        (u'login', u'Login'),
        (u'logout', u'Logout'),
        # (3,'GetFile'),
        # (4,'SendFile'),
        # (5,'Exception'),
    ]
    action_type = Column(ChoiceType(action_choices2))
    # action_type = Column(String(64))
    cmd = Column(String(255))
    date = Column(DateTime)

    user_profile = relationship("UserProfile", backref='audit_logs')
    bind_host = relationship("BindHost", backref='audit_logs')

    def __repr__(self):
        return "%s %s %s" % (self.date, self.action_type, self.cmd)

if __name__ == '__main__':
    pass
