#!/usr/bin/env python
# -*- encoding:utf8 -*-
#
__author__ = 'vivi'

"""
http://docs.sqlalchemy.org/en/rel_0_8/orm/tutorial.html#connecting
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import random

_CHARS = 'abcdefghijklmnopqrstuvwxyz+-/=ABCDEFGHIJKLMNOPQRSTUVWXYZ'

engine = create_engine('sqlite:///sqlite3.db', echo=True)
#engine = create_engine('mysql://vivi:password@localhost:3306/test?charset=utf8')
Session = sessionmaker()
Session.configure(bind=engine)

Base  = declarative_base()
class User(Base):
    """
    definition of table users
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    fullname = Column(String(32)) # can specify the length of the string field
    password = Column(String(32))

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return '<User(%s, %s, %s, %s)>' % (self.id, self.name, self.fullname, self.password)

class Pastebin(Base):
    """
    for test
    """
    __tablename__ = 'pastebin'
    id = Column(Integer, primary_key=True)
    content = Column(String(4096), nullable=False)

    def __init__(self, content):
        self.content = content
        self.createtime = datetime.datetime.today().ctime()

    def __repr__(self):
        return '<Pastebin id=%s, content=%s>' % (self.id, self.content)

def user_operation():
    user = User('vivi', 'weiqiang.yang', 'shitpass')
    print user
    Base.metadata.create_all(engine) # seems like it won't create table if the table already exists

    session = Session()
    session.add(user)
    session.commit()

    query_user = session.query(User).first()
    print query_user

    # something like hibernate, change to the entity will be update to the database
    query_user.password = 'change_password'
    print session.dirty
    session.commit()

    # separate insert statements are generated
    session.add_all([
        User('name1', 'realname', 'password'),
        User('name2', 'realname2', 'password2'),
        ])
    print session.new
    session.commit()

    # filter_by
    count = session.query(User).count()
    print count
    user_list = session.query(User).order_by(User.id)
    for user in user_list:
        print user.id, user.name

    # pagination using OFFSET and LIMIT
    total_count = 0
    limit = 10
    offset = 0
    user_list = session.query(User)[offset:offset+limit] # not the same as offset:limit but offset:offset+limit
    while len(user_list) > 0:
        total_count += len(user_list)
        offset += limit
        print offset, limit
        user_list = session.query(User)[offset:offset+limit]
    print 'total count = ', total_count

    # execute the plain sqls
    sql = """
        SELECT name, COUNT(name) AS c FROM users
            WHERE id > :id
            GROUP BY name
            ORDER BY c DESC
            LIMIT :limit OFFSET :offset
        """
    result_proxy = session.execute(sql, {'id':0, 'limit':10, 'offset':0})
    print result_proxy.fetchall()
    # deal with the ResultProxy: http://docs.sqlalchemy.org/en/rel_0_8/core/connections.html#sqlalchemy.engine.ResultProxy

def random_string(length=10):
    """
    generates the random string
    """
    import random
    _buff = []
    _count = len(_CHARS)
    for i in xrange(0, length, 1):
        _buff.append(_CHARS[random.randint(0, _count-1)]) # randint generates [min,max]
    return ''.join(_buff)

def create_pastebin(content):
    """
    insert a record, is there a simpler way?
    """
    pastebin = Pastebin(content)
    session = Session()
    session.add(pastebin)
    session.commit()
    session.close()

def delete_pastebin(id):
    """
    delete shit by id
    """
    session = Session()
    tobedel = session.query(Pastebin).filter(Pastebin.id == id).first() # one() will throw a exception if the record not exists
    print ' to be delete :', tobedel
    if tobedel is not None:
        session.delete(tobedel)
        session.commit()
    else:
        print '%s is not exist.' % id
    session.close()

def paste_operation():
    create_pastebin(random_string(20))
    delete_pastebin(10)

if __name__ == '__main__':
#    paste_operation()
    user_operation()