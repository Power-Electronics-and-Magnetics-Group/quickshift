import math
import time
import multiprocessing
import numpy
from itertools import repeat
from more_itertools import divide
from multiprocessing import Pool, cpu_count
from currentSharing import current_sharing_numeric
from currentSharing import current_sharing_symbolic
from stackups import stackups, parallelConnect, seriesConnect, parseStackup
from stackupClasses import Layer, SeriesNode, ParallelNode, Node, Stackup

def solver(stack, b, f, l, r, N):
    d = math.sqrt(2*(1.68*math.pow(10,-8))/((2*math.pi*f)*(4*math.pi*pow(10,-7))))
    print(d)
    R = 1.68*math.pow(10,-8)*l/(d*b)
    print(R)
    stackLoss = 0

    try:
        solutionVector = list(current_sharing_numeric(stack, b, f, l, r))
        print(solutionVector)
        for i in range(N,3*N):
            print(.5*R*((b*solutionVector[i])**2))
            stackLoss = stackLoss + .5*R*((b*solutionVector[i])**2)
    except numpy.linalg.LinAlgError:
        solutionVector = [100] * 3*N
        stackLoss = 9999

    return ([stack, stackLoss])

def solveIt(N, turnRatio, maxTurns, b, f, l, r):
    stacks = stackups(N, turnRatio, maxTurns)

    print(f'Analyzing {len(stacks)} options...')

    threadCount = multiprocessing.cpu_count() - 1

    with multiprocessing.Pool(processes=threadCount) as pool:
        results = pool.starmap(solver, zip(stacks, repeat(b), repeat(f), repeat(l), repeat(r), repeat(N)))

    minLoss = 1000000000
    bestStack = 0
    failureTally = 0
    failedStacks = []
    for result in results:
        if (result[1] < minLoss):
            minLoss = result[1]
            bestStack = [result[0]]
        elif (result[1] == minLoss):
            bestStack.append(result[0])
        if (result[1] == 9999):
            failureTally = failureTally + 1
            failedStacks.append(result[0])

    return [bestStack, minLoss, failureTally, failedStacks, len(stacks)]

if __name__ == "__main__":
    # N = 7
    # turnRatio = 3
    # maxTurns = 3

    # b = .02
    # f = 3000000
    # l = .2
    # r = .001
    # #r = [.001, .002, .002, .002, .001]
    # ans = solveIt(N,turnRatio,maxTurns, b, f, l, r)
    # print(f'Optimized {ans[0]}')
    # print(f'Loss (with 1A on high-current winding): {ans[1]:3f} W')
    # if (ans[2] == 0):
    #     print(f'No failed stacks.')
    # else:
    #     print(f'Failed Stacks: {ans[3]}')
    prim = "(P,[L2,1T],(P,[L4,1T],[L6,1T]))"
    sec = "(S,(S,(S,[L1,1T],[L3,1T]),[L5,1T]),[L7,1T])"

    b = .004
    f = 12000000
    l = .066
    r = .00025
    N = 7

    stack = parseStackup(prim,sec,N)

    ans = solver(stack, b, f, l, r, N)
    print(ans)
