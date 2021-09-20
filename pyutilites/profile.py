"""
profile.py

Module contain decorators for profiling
- timestamp: Function execution time
"""


import time


__start_time = None         # timestamp when program has started
__FILENAME = "time.txt"  # file name for writing logs


def timestamp_init():
    """
    Function initializes start_time (program begin time)
    :return: None
    """
    global __start_time
    f = open(__FILENAME, 'w')
    f.write("{0}: start\n".format(
        time.strftime("%H:%M:%S", time.localtime())
    ))
    f.close()
    __start_time = time.time()
timestamp_init()


def timestamp(filename: str = __FILENAME):
    """
    Calculates function execution time (decorator).
    :param filename: file name of log (default __FILENAME)
    :return:

    Example:
        from profile import timestamp

        @timestamp()
        def foo():
            print("I'm foo")

        foo(4)
        foo(5, 6)

    Output (file: time.txt):
        23:08:03: start
        0.000008583	:      0.014066696 ms: foo((4,))->None:
        0.000083923	:      0.004291534 ms: foo((5,))->None:

    """
    def params(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            res = func(*args, **kwargs)
            end_time = time.time()
            with open(filename, 'a') as f:
                duration = end_time - start_time
                param = ""
                if args:
                    param = "{}".format(args)
                if kwargs:
                    param += ", {}".format(kwargs)
                f.write("{0:.9f}\t: {3:16.9f} ms: {1}({2})->{4}:\n".format(
                    start_time - __start_time,
                    func.__name__, param,
                    duration * 1000.0,
                    res
                ))
            return res
        return wrapper
    return params


def main():

    @timestamp()
    def foo(*args):
        for arg in args:
            print(arg)

    res = foo(4)
    res = foo(5, 6)

    timestamp.count = 2
    dirs = dir(timestamp)
    for dir_ in dirs:
        print(dir_)
    print(timestamp.count)

if __name__ == "__main__":
    main()


