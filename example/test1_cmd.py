import sys
sys.path.append('..')
from task_process import *
from task import *
import time

cmd = 'python3 ./test_task.py'
task = Task()
task.task = cmd
task.key = "test1"
task.start()

time.sleep(5)
print(get_task_state("test1"))
time.sleep(5)
kill_task("test1")