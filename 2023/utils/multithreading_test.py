import multiprocessing
from utils.utils import timeit


@timeit
def parallel_processing(func, start, data_size, threads_num):
    processes = []
    thread_data_size = int(data_size / threads_num)
    queue = multiprocessing.Queue()
    ret = {'foo': False}
    queue.put(ret)

    for i in range(threads_num):
        data_start = start + thread_data_size*i
        data_end = data_start + thread_data_size

        process = multiprocessing.Process(target=func, args=(data_start, data_end, queue))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    print(queue.get())

def power(start, end, queue):
    total_sum = 0
    for i in range(start, end, 1):
        total_sum += i*i

    print(start, end, total_sum)
    ret = queue.get()
    ret[start] = total_sum
    queue.put(ret)
@timeit
def solo_power(start, end):
    total_sum = 0
    for i in range(start, end, 1):
        total_sum += i*i

    print(start, end, total_sum)
    return total_sum

if __name__ == "__main__":
    parallel_processing(power, start=0, data_size=1000000000, threads_num=15)
    # solo_power(start=0, end=1000000000)#

# 18 - 7.9878 seconds
# 17 - 7.9778 seconds
# 16 - 7.6413 seconds
# 15 - 7.5930 seconds
# 14 - 7.7149 seconds
# 12 - 7.9878 seconds
# 10 - 8.1973 second
# 8 - 9.0096 seconds
# 6 - 11.1163 seconds
# 4 - 15.7764 seconds
# 1 - 59.7981 seconds