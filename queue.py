from multiprocessing import Process

import time

import os



def download(q):
    print(os.getpid(),'开始等待下载任务')
    while True:
        url = q.get()
        print('开始下载',url)
        time.sleep(5)

def main():
    #主进程
    queue = Queue(maxsize = 4)
    downloaderProcess = Process(target=download,args=(queue,))
    downloaderProcess.start()

    for i in range(20):
        url ='http://www.people.com.cn/'
        print('准备请求url',url)
        queue.put(url)

main()

