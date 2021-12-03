from task import *
import time
interval = 3

while True:
    time.sleep(interval)
    col = connect_col()
    records = col.find()
    for record in records:
        pid = record["pid"]
        update_task_state(pid)
