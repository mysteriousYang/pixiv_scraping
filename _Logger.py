# -*- coding: utf-8 -*-
import datetime
from conf import LOG_SAVE_PATH
'''
#神兽保佑 风调码顺
# ┏┓　    ┏┓
#┏┛┻━━━━━━┛┻━┓
#┃　　　 　　 ┃
#┃　┳┛　┗┳　  ┃
#┃　　　　　　┃
#┃　　　┻　　┃
# ┗━┓ xxxx┏━┛
#　　┃  　 ┃
#　　┃　 　┃
#　  ┃　 　┗━━━┓
#　　┃      　  ┣┓
#　　┃        ┏┛
#　　┗┓┓┏━━┳┓┏┛
#　 　┃┫┫　┃┫┫
#　　 ┗┻┛　┗┻┛
import datetime
import conf
'''
def console_log(func):
    '''
    A Log Decorator to log message in console\n
    Args: 
       func : the function to be log
    '''
    def inner(*args , **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        res = func(*args,**kwargs)
        print(f"[{timestamp}] ({func.__name__}) output:: {res}")
        return res
    return inner

def disk_log(func):
    '''
    A Log Decorator to log message on Local disk\n
    Args: 
        func : the function to be log
    '''
    def inner(*args , **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        res = func(*args,**kwargs)
        with open(LOG_SAVE_PATH,'a') as Log:
            Log.write(f">[{timestamp}] ({func.__name__}) output:: {res}\n")
        print(f"[{timestamp}] ({func.__name__}) output:: {res}")
        return res
    return inner

