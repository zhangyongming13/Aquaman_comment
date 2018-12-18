# coding=utf-8


import asyncio
import logging; logging.basicConfig(level=logging.INFO)
import aiomysql
from www.orm import Model, StringField, integerField


@asyncio.coroutine
def create_pool(loop, **kw):  # **kw关键字参数，多个参数传入之后自动组合成dict
    logging.info('create database connection pool...')
    global __pool
    __pool = yield from aiomysql.create_pool(  # 创建数据库连接池
        # dict中的get()函数的方法get(key, default)，返回dict中指定键的值，不存在则返回默认的值
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf-8'),
        autocommit=kw.get('autocommit', True),  # 自动提交数据给数据库
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )


@asyncio.coroutine
def select(sql, args, size = None): # args是sql命令
    log(sql, args)
    global __pool
    with (yield from __pool) as conn:
        # 使用aiomysql的cursor创建cursor
        cur = yield from conn.cursor(aiomysql.DictCursor)
        # mysql中的占位符是%s，sql中是？要将sql转化为mysql的占位符
        yield from cur.execute(sql.replace('?', '%s'),  args or ())
        if size:
            # 如果有传入size就获取size数量的记录fetchamany
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returned: %s' % len(rs))


@asyncio.coroutine
def execute(sql, args):
    log(sql)
    global __pool
    with (yield from __pool) as conn:
        try:
            cur = conn.cursor()
            yield from cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount  # 影响的行数
            yield from cur.close()
        except BaseException as e:
            raise
        return affected


class User(Model):  # 继承了Model的所有功能
    __table__ = 'users'

    id = IntegerField(primary_key=True)
    name = StringField()


# Model继承了dict，所有也有dict的所有功能，又实现哦特殊方法__getattr__()和__setattr__()
# 所以又像普通字段这样写
class Model(dict, metaclass = ModelMetaclass):

    def __init__(self, **kw):
        # super用来解决多重继承的问题
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappins__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

