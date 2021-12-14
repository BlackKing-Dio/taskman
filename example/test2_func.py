import sys
sys.path.append('..')
from task_process import *
from task import *
import test_task
import time
import psutil


task = Task()
task.task = test_task.txt_num
task.key = "test2"
task.start()

time.sleep(5)
print(get_task_state("test2"))
# time.sleep(5)
# print(get_task_state("test2"))
time.sleep(5)
kill_task("test2")