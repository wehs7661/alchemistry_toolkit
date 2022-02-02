from memory_profiler import memory_usage
def my_func(a, b=1):
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a

if __name__ == '__main__':
    memor_usage((my_func
