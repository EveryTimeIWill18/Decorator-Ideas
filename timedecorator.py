from time import time
from functools import wraps, reduce
import numpy as np

def iterations_(it=1000):
    """calculate runtime metrics"""
    def time_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            runtime_log = []
            for _ in range(it):
                start = time()
                func = f(*args, **kwargs)
                end = time()
                runtime_log.append(end-start)
            return {"Number of iterations: {}".format(it): runtime_log,
                    "Average Runtime": np.mean(np.array(runtime_log)),
                    "Max Runtime": np.max(np.array(runtime_log)),
                    "Min Runtime": np.min(np.array(runtime_log))}
        return wrapper
    return time_decorator

@iterations_(10)
def g(a):
    return int(a)**2

if __name__ == '__main__':
    print(g(10))
