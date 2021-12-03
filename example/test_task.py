import time
import os
ss = ''
pid = os.getpid()
with open('/home/res/breton/dev/monitor/demo_t3/txt','w') as f:
    f.write(ss)

for i in range(100):
    ss = str(i)+'\n'
    with open('/home/res/breton/dev/monitor/demo_t3/txt','a') as f:
        f.write(ss)
    time.sleep(1.5)