# 1 概述
    本模块用于linux进程管理，目前只支持linux shell命令的本地任务管理
    每个任务在投递前需要自定义一个key(字符串类型)，在投递后，该key值是任务的唯一识别号，建议定义成与程序有关的一些字符组合，它可以在其他程序中，通过对Mongodb中的"taskman"数据库的taskman表的交互，从而实现任务管理

# 2.安装部署
## 2.1 依赖
```bash
# python >= 3.8.10
ubuntu自带

# mongodb >= 4.4.10
## 使用以下命令安装MongoDB
sudo apt install mongodb-org
## 开启mongo
sudo systemctl start mongod.service
## 开机自启
sudo systemctl enable mongod

# pymongo >= 3.12.1
pip3 install pymongo
```

## 2.2 部署自启项
    echo "python3 /本模块绝对路径/task_monitor.py" > taskman_monitor.sh
    然后把taskman_monitor.sh这个脚本放入自启项中
    该脚本中的参数interval是刷新时间间隔，默认为3秒，可根据需要改为其他数值

# 3 任务管理
    可查看test.py中对命令"python test_task.py"的任务投递用例

## 3.1 任务创建
    具体使用步骤：
    from task_process import *
    from task_monitor import *

    cmd = 'python3 ./test_task.py'
    task = Task()
    task.cmd = cmd
    task.key = "test"

## 3.2 任务投递
    task.start()

## 3.3 查看任务状态
```python
print(get_task_state("test")) # 这个key是任务创建时自定义的字符串
```
返回数据：
```json
{
    "user" : "res",  //所属用户
    "pid" : "528979",  //进程id
    "ppid": [528980],  //父进程id(由进程数中提取)
    "cpu_pct": "0.0",  //cpu使用率(%)
    "mem_pct": "0.0",  //内存使用率(%)
    "vsz": "2620",  //该进程使用的虚拟內存量（KB）
    "rss": "548",  //该进程占用的固定內存量（KB）
    "tty": "pts/6", //该进程在終端上运行（登陆者的終端位置），若与终端无关，则显示（？）。若为pts/0等，则表示由网络连接主机进程
    "state": "S+",  //进程的状态 
    "start": "16:05" //该进程被触发启动时间
}
```
    其中state状态位常见的状态字符有
    D      //无法中断的休眠状态（通常 IO 的进程）； 
    R      //正在运行可中在队列中可过行的； 
    S      //处于休眠状态； 
    T      //停止或被追踪； 
    W      //进入内存交换 （从内核2.6开始无效）； 
    X      //死掉的进程 （基本很少见）； 
    Z      //僵尸进程； 
    <      //优先级高的进程 
    N      //优先级较低的进程 
    L      //有些页被锁进内存； 
    s      //进程的领导者（在它之下有子进程）； 
    l      //多线程，克隆线程（使用 CLONE_THREAD, 类似 NPTL pthreads）； 
    +      //位于后台的进程组；

## 3.4 结束任务
    kill_task(key) # 这个key是任务创建时自定义的字符串