from multiprocessing import Pool
import time
import random
import os


def runTask(t):
    """"""
    print('child {}'.format(t))
    t = random.random() * t
    time.sleep(t)
    print('stoping child {}'.format(t))

if __name__ == '__main__':
    print(u'Parent Process {} start'.format(os.getpid()))
    p = Pool()  # 默认设置Pool同时开启4个进程
    for i in range(5):
        p.apply_async(runTask, args=(i,))
    p.close()   # 不能再添加新的进程
    # 强行阻塞在这里
    print('Parent ending')
