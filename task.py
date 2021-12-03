from task_process import *
import pymongo
import logging

def connect_col():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["taskman"]
    col = db["taskman"]
    return col

def check_key(key):
    col = connect_col()
    task_count = col.count_documents({"key":key})
    if task_count > 0:
        return True
    else:
        return False

class Task():
    def __init__(self):
        self.key = None
        self.cmd = 'echo'

    def start(self):
        pid = submit_process(self.cmd)
        col = connect_col()
        if self.key == None:
            return "please set a key(string)"
        else:
            if check_key(self.key):
                return "There is already an identical task running"
            else:
                record = {"key":self.key,"pid":pid}
                col.insert(record)
                return "ok"

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
    pid = col.find({"key":key})[0]["pid"]
    state = get_process_state(pid)
    return state

def kill_task(key):
    col = connect_col()
    if check_key(key):
        record = col.find({"key":key})[0]
        kill_process(record["pid"])
        logging.debug("killed")
    else:
        logging.debug("no such task")
