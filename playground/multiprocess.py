from multiprocessing import Process, Queue
import os

def worker(tasks, results):
    t = tasks.get()
    print t
    tasks.put( True )
    t = tasks.get()
    print t
    # result = t * 2
    # results.put([t, "->", result])

if __name__ == "__main__":
    n = 20
    my_tasks = Queue()
    my_results = Queue()

    worker = Process(target=worker, args=(my_tasks, my_results))

    worker.start()
    my_tasks.put( False )
    # result = my_results.get()
    # print(result)

    # for proc in workers:
        # proc.start()

    # for i in range(n):
    #     my_tasks.put(i)

    # for i in range(n):
    #     result = my_results.get()
    #     print(result)