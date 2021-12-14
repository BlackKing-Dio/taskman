import time
import os

def txt_num():
    ss = ''

    with open('txt','w') as f:
        f.write(ss)

    for i in range(100):
        ss = str(i)+'\n'
        with open('txt','a') as f:
            f.write(ss)
        time.sleep(0.2)

if __name__ == "__main__":
    txt_num()