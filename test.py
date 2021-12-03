from task_process import *
from task import *
import time

cmd = 'python3 ./test_task.py'
task = Task()
task.cmd = cmd
task.key = "test"
task.start()

time.sleep(7)
print(get_task_state("test"))
time.sleep(70)
print(get_task_state("test"))
time.sleep(3)
kill_task("test")