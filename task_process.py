import subprocess
import os
import re
import signal

# # 定义一个进程的类
# class Process():
#     def __init__(self):
#         self.cmd = 'echo' #定义任务命令

# 提交并运行该任务，返回该任务对应的进程ID(pid)
def submit_process(cmd):
    p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE)#,stdout=subprocess.PIPE)
    return p.pid

# 获取进程树中所有父进程
def get_process_ppid(pid):
    CMD = "pstree -p "+str(pid)
    res = os.popen(CMD).read()
    re_arr = re.findall('\(([0-9]+)\)',res)
    ppid_arr = []
    for i in re_arr:
        if i != str(pid):
            ppid_arr.append(int(i))
    return ppid_arr

# 获取进程状态
def get_process_state(pid):
    state = {}
    ppid = get_process_ppid(pid)
    if len(ppid) >0:
        CMD='ps -aux|grep '+str(pid)+'|awk \'{if($2 == \''+ str(pid) +'\')print $0}\''
        try:
            info = os.popen(CMD).read().strip()
            arr = re.split(r"[ ]+", info)
            state["user"] = arr[0]
            state["pid"] = arr[1]
            state["ppid"] = ppid
            state["cpu_pct"] = arr[2]
            state["mem_pct"] = arr[3]
            state["vsz"] = arr[4]
            state["rss"] = arr[5]
            state["tty"] = arr[6]
            state["state"] = arr[7]
            state["start"] = arr[8]
        except:
            pass
    else:
        pass
    return state

# 结束进程
def kill_process(pid):
    ppid_arr = get_process_ppid(pid)
    for ppid in ppid_arr:
        if isinstance(ppid,int):
            if(1):
                os.kill(ppid,signal.SIGKILL)
            else:
                pass
