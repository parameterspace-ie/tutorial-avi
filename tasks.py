import os
from django.conf import settings

# Class used for creating pipeline tasks
from pipeline.classes import (
    AviTask,
    AviParameter, AviLocalTarget,
)


def fib(n):
    if n == 1:
        return 1
    elif n == 0:   
        return 0            
    else:                      
        return fib(n-1) + fib(n-2)


class CalcFib(AviTask):
    fib_num = AviParameter()

    def output(self):
        return AviLocalTarget(os.path.join(
            settings.OUTPUT_PATH, 
            "fib_%s.txt" % self.fib_num
        ))

    def run(self):
        fib_result = fib(self.fib_num)
        with open(self.output().path, 'wb') as out:
            print fib_result
            out.write("%s number in fib sequence is %s" % (self.fib_num, fib_result))
