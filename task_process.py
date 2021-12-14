import subprocess
import os
import re
import signal
import psutil
from multiprocessing import Pool

# 提交并运行该任务(命令行)，返回该任务对应的进程ID(pid)
def submit_command(cmd):
    p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE)#,stdout=subprocess.PIPE)
    return p.pid


# 提交并运行该任务(方法/函数)，返回该任务对应的进程ID(pid)
# def submit_function(func,*args,**kargs):
    
#     pool = Pool(1) # run 3 process simultaneously
#     pool.apply_async(func, *args,**kargs)
#     pid = os.getpid()
#     pool.close()
#     pool.join()
#     return pid

def submit_function(func,*args,**kargs):
    ret = os.fork()
    if ret == 0:
        #子进程
        func(*args,**kargs)
        return None
        # return os.getpid()
    else:
        #父进程
        return os.getpid()

# 获取进程树中所有父进程
def get_process_ppid(pid):
    p = psutil.Process(pid)
    return p.ppid()

# 获取进程状态
# def get_process_state(pid):
#     state = {}
#     ppid = get_process_ppid(pid)
#     if len(ppid) >0:
#         CMD='ps -aux|grep '+str(pid)+'|awk \'{if($2 == \''+ str(pid) +'\')print $0}\''
#         try:
#             info = os.popen(CMD).read().strip()
#             arr = re.split(r"[ ]+", info)
#             state["user"] = arr[0]
#             state["pid"] = arr[1]
#             state["ppid"] = ppid
#             state["cpu_pct"] = arr[2]
#             state["mem_pct"] = arr[3]
#             state["vsz"] = arr[4]
#             state["rss"] = arr[5]
#             state["tty"] = arr[6]
#             state["state"] = arr[7]
#             state["start"] = arr[8]
#         except:
#             pass
#     else:
#         pass
#     return state

# 结束进程
def kill_process(pid):
    p = psutil.Process(pid)
    for i in p.children():
        # c = psutil.Process(i.pid)
        # for j in c.children():
        #     print(j.pid)
        # print(i.pid)
        os.kill(i.pid,signal.SIGKILL)
    # os.kill(p.children()[-1].pid,signal.SIGKILL)

def get_process_state(pid):
    if pid == None:
        return {}
    p = psutil.Process(pid)
    # pp = psutil.Process(p.pid)
    # ppid = get_process_ppid(pid)
    # # if pp.is_running():
    # if len(ppid) >0:
    # print('33',pid)
    CMD='ps -aux|grep '+str(pid)+'|awk \'{if($2 == \''+ str(pid) +'\')print $0}\''
    # print(pid)
    if(1):
        info = os.popen(CMD).read().strip()
        # print('info',info)
        arr = re.split(r"[ ]+", info)
        state = {}
        state["user"] = arr[0]
        state["pid"] = pid
        state["ppid"] = p.ppid()
        state["children"] = p.children()
        state["cpu_pct"] = arr[2]
        state["mem_pct"] = arr[3]
        state["vsz"] = arr[4]
        state["rss"] = arr[5]
        state["tty"] = arr[6]
        state["state"] = arr[7]
        state["start"] = arr[8]
        return state
    else:
        return {}
    # else:
    #     return {}
# def kill_process(pid):
#     p = psutil.Process(pid)
#     p.kill()
    #p.terminate() #与p.kill()一样

#暂停
def suspend_process(pid):
    p = psutil.Process(pid)
    p.suspend()

#继续
def resume_process(pid):
    p = psutil.Process(pid)
    p.resume()