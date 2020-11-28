import time, pandas
from typing import Callable, Dict, Tuple
from matplotlib import pyplot as plot

def benchmark(trials:int):
    """ Testing decorator for the fibonacci class' methods """
    def benchmark_method(function:Callable[[int],int]) -> Callable[[int],Tuple[float,str]]:
        def time_wrapper(*args) -> Tuple[float,str]:
            """ Return the time taken to run a fibonacci method in microseconds """
            t1 = time.time()
            for _ in range(trials):
                function(*args)
            return ((time.time()-t1)/trials) * 1e6, function.__name__
        return time_wrapper
    return benchmark_method

class fibonacci():
    """ A class to explore one basic idea of Dynamic Programming, memorization of otherwise repeated work. """

    def __init__(self):
        self.known : Dict[int,int]= dict()

    def clear(self):
        self.known = dict()

    
    @staticmethod
    def fib(n:int) -> int:
        """ Calculate the fibonacci number at the nth index using the basic exponential time algorithm. \n
            Time complexity, T(n), is (I'm told) equal to Phi^n, or much simpler to verify, T(n) >= 2^(n/2) 
        """
        if n<= 2:
            return 1
        else:
            return fibonacci.fib(n-1) + fibonacci.fib(n-2)

    @benchmark(10000)
    def top_down_mem_fib(self, n:int) -> int:
        """ Calculate the nth fibonacci number using a top down memorizing algorithm. \n
            Reduces time complexity to O(n) 
        """
        if n in self.known.keys():
            return self.known[n]
        
        if n <= 2:
            return 1

        ret = self.top_down_mem_fib(n-1) + self.top_down_mem_fib(n-2)
        self.known[n] = ret
        return ret

    ## The bottom up apporach avoids recursion, avoiding the standard python protection that
    ## stops any program reaching a high level of recursions 
    ## (1000 calls standard, but there are ways to subvert it)
    @benchmark(10000)
    def bottom_up_mem_fib(self, n:int) -> int:
        """ Calculate the nth fib number using a memorizing algorithm with a single function call """
        if n in self.known.keys():
            return self.known[n]

        for i in range(n + 1):
            if i <= 2:
                r = 1
            else:
                r = self.known[i-1] + self.known[i-2]
            self.known[i] = r

        return self.known[n]

    @benchmark(10000)
    def pruned_bottom_up_mem_fib(self, n:int) -> int:
        """ Calculate the nth fib number using linear time with less function calls, 
            while restricting the memory to the last two values found. 
        """
        if n in self.known.keys():
            return self.known[n]

        for i in range(n + 1):
            if i <= 2:
                r = 1
            else:
                r = self.known[i-1] + self.known[i-2]
                del self.known[i-2]

            self.known[i] = r

        return self.known[n]

def test():
    """ Render plots showing the performance of the different approaches to calculating the fibonacci sequence """
    df = pandas.DataFrame()
    fib = fibonacci()
    for N in [25,50,100,200, 400]:
        time, name = fib.top_down_mem_fib(N)
        df.loc[N,name] = time
        fib.clear()
        time, name = fib.bottom_up_mem_fib(N)
        df.loc[N,name] = time
        fib.clear()
        time, name = fib.pruned_bottom_up_mem_fib(N)
        df.loc[N,name] = time
        fib.clear()

    df.plot.line(ylim=0)
    plot.rcParams["font.size"] = 15
    plot.xlabel("N")
    plot.ylabel("Microseconds")
    plot.savefig("top_down_dominates.png")
    df.drop('top_down_mem_fib',axis=1).plot.line(ylim=0)
    plot.rcParams["font.size"] = 15
    plot.xlabel("N")
    plot.ylabel("Microseconds")
    plot.savefig("a_fair_fight.png")
    print('This one example demonstrates the gains that can be had in reducing function calls.')
    print('A hidden benefit is the amount of memory being saved in the stack as well, regardless of pruning.')

    

## TODO: add graph showing memory taken
if __name__ == "__main__":
    test()




