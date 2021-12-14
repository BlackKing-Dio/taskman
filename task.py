from task_process import *
import pymongo
import logging
import psutil
import types

def connect_col():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["taskman"]
    col = db["taskman"]
    return col

def check_key(key):
    col = connect_col()
    counts = col.find({"key":key}).count()
    if counts > 0:
        return True
    else:
        return False

class Task():
    def __init__(self):
        self.key = None
        self.task = None

    def start(self,*args,**kargs):
        #检测到task为字符串类型(视为shell命令)
        if isinstance(self.task,str):
            pid = submit_command(self.task)
            col = connect_col()
            if self.key == None:
                return "please set a key(string)"
            else:
                if check_key(self.key):
                    # return "There is already an identical task running"
                    col.delete_many({"key":self.key})
                record = {"key":self.key,"pid":pid}
                col.insert(record)
                return "ok"

        #检测到task为方法类型
        elif isinstance(self.task,types.FunctionType):
            pid = submit_function(self.task,*args,**kargs)
            print('func',pid)
            col = connect_col()
            if self.key == None:
                return "please set a key(string)"
            else:
                if check_key(self.key):
                    # print("There is already an identical task running")
                    col.delete_many({"key":self.key})
                    # col.update_one({"key":self.key},{"$set":{"pid":pid}})
                record = {"key":self.key,"pid":pid}
                col.insert(record)
                return "ok"

        #检测到task为函数类型
        elif isinstance(self.task,types.MethodType):
            pid = submit_function(self.task,*args,**kargs)
            print('method',pid)
            col = connect_col()
            if self.key == None:
                return "please set a key(string)"
            else:
                if check_key(self.key):
                    # return "There is already an identical task running"
                    col.delete_many({"key":self.key})
                record = {"key":self.key,"pid":pid}
                col.insert(record)
                return "ok"
        #不支持的类型
        else:
            return "invalid task type"

def update_task_state(pid):
    state = get_process_state(pid)
    col = connect_col()
    if state == {}:
        col.delete_many({"pid":pid})
        return "none"
    else:
        col = connect_col()
        record = col.find({"pid":pid})[0]
        newvalues = {"$set": state}
        col.update_one({"pid":pid}, newvalues)
        return "updated"

def get_task_state(key):
    col = connect_col()
    if check_key(key):
        pid = col.find({"key":key})[0]["pid"]
        state = get_process_state(pid)
        return state
    else:
        return None

def kill_task(key):
    col = connect_col()
    if check_key(key):
        print(check_key(key))
        pid = col.find({"key":key})[0]["pid"]
        kill_process(pid)
        logging.debug("killed")
    else:
        logging.debug("no such task")
