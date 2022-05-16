import math
import time
import multiprocessing
import numpy
from itertools import repeat
from more_itertools import divide
from multiprocessing import Pool, cpu_count
from currentSharing import current_sharing_numeric
from currentSharing import current_sharing_symbolic
from stackups import stackups, parallelConnect, seriesConnect, parseStackup, turnPairs
from stackupClasses import Layer, SeriesNode, ParallelNode, Node, Stackup

def round_sig(x, sig=2):
    return round(x, sig-int(math.floor(math.log10(abs(x))))-1)

def solver(stack, b, f, l, r, N):
    d = math.sqrt(2*(1.68*math.pow(10,-8))/((2*math.pi*f)*(4*math.pi*pow(10,-7))))
    R = 1.68*math.pow(10,-8)*l/(d*b)
    stackLoss = 0

    try:
        solutionVector = list(current_sharing_numeric(stack, b, f, l, r))
        for i in range(N,3*N):
            stackLoss = stackLoss + .5*R*((b*solutionVector[i])**2)
    except numpy.linalg.LinAlgError:
        solutionVector = [100] * 3*N
        stackLoss = 9999

    return ([stack, stackLoss])

def solveIt(N, turnRatio, maxTurns, b, f, l, r, minTurns=1):
    stacks = stackups(N, turnRatio, maxTurns, minTurns)

    print(f'Analyzing {len(stacks)} options...')

    threadCount = multiprocessing.cpu_count() - 1

    with multiprocessing.Pool(processes=threadCount) as pool:
        results = pool.starmap(solver, zip(stacks, repeat(b), repeat(f), repeat(l), repeat(r), repeat(N)))

    minLoss = 1000000000
    bestStack = 0
    failureTally = 0
    failedStacks = []
    for result in results:
        loss = round_sig(result[1],5)
        if (loss < minLoss):
            minLoss = loss
            bestStack = [result[0]]
        elif (loss == minLoss):
            bestStack.append(result[0])
        if (loss == 9999):
            failureTally = failureTally + 1
            failedStacks.append(result[0])

    return [bestStack, minLoss, failureTally, failedStacks, len(stacks)]

def solveIt_list(N, turnRatio, maxTurns, b, f, l, r, minTurns=1, listQuantity=10):
    stacks = stackups(N, turnRatio, maxTurns, minTurns)

    print(f'Analyzing {len(stacks)} options...')

    threadCount = multiprocessing.cpu_count() - 1

    with multiprocessing.Pool(processes=threadCount) as pool:
        results = pool.starmap(solver, zip(stacks, repeat(b), repeat(f), repeat(l), repeat(r), repeat(N)))

    #print(type(results))
    minLoss = 1000000000
    bestStack = 0
    failureTally = 0
    failedStacks = []

    results.sort(key=lambda x: x[1])
    return [results[0:listQuantity], len(stacks)]

if __name__ == "__main__":
    # N = 4
    # turnRatio = 1
    # maxTurns = 4

    # b = .005
    # f = 10000000
    # l = .05
    # r = .0001
    #ans = solveIt_list(N,turnRatio,maxTurns, b, f, l, r, 1)
    #print(ans)


