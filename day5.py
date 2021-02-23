#task 1.Make a generator to perform the same functionality of the iterator
def GeneratorDemo(num):
    for x in num:
        yield(x*X)
Res= GeneratorDemo([10,20,30,40,50])
print(Res)
print(next(Res))
print(next(Res))
print(next(Res))
print(next(Res))
print(next(Res))

	 

#task 2.Try overwriting some default dunder methods and manipulate their default behavior
class Test:
    def __init__(self, name,question):
        self.name = name
        self.question = question
    def __str__(self):
        return "Hello there!!,  Dear {}, {}".format(self.name, self.question)
test = Test('AV', ,"how are you?" )
print(test)



#Task 3.Write a decorator that times a function call using timeit start a timer before func call end the timer after func call print the time diff
from functools import wraps
import time
def Demo(func):
    @wraps(func)
    def timeitwrapper(*args, **kwargs):
        starttime = time.perf_counter()
        print(f"Start time {starttime}")
        func(*args, **kwargs)
        endtime = time.perf_counter()
        print(f"end time {endtime}")
        print(f"time spent is {endtime-starttime}")
    return timeitwrapper
@Demo
def Hello():
    print('Hello there!! ')
@Demo
def Hello1(name,question):
    print(f"Hello {name} , {question}")
Hello()
Hello1("AV","How are you?")