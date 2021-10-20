import math
import time
import multiprocessing
import numpy
from more_itertools import divide
from currentSharing import current_sharing_numeric
from currentSharing import current_sharing_symbolic
from stackups import stackups
from stackupClasses import Layer, SeriesNode, ParallelNode, Node, Stackup
# def loss(ff):
#     loss_sum=0
#     for term in ff:
#         loss_sum = loss_sum + term**2
#         return loss_sum

def solver(queue, stacks, b, f, l, r, N):
    minLoss = 1000000000
    bestStack = 0
    d = math.sqrt(2*(1.68*math.pow(10,-8))/((2*math.pi*f)*(4*math.pi*pow(10,-7))))
    R = 1.68*math.pow(10,-8)*l/(d*b)
    failureTally = 0
    failedStacks = []

    for stack in stacks:
        try:
            solutionVector = list(current_sharing_numeric(stack, b, f, l, r))
        except numpy.linalg.LinAlgError:
            solutionVector = [100] * 3*N
            failureTally = failureTally + 1
            failedStacks.append(stack)
        stackLoss = 0
        for i in range(N,3*N):
            stackLoss = stackLoss + .5*R*((b*solutionVector[i])**2)
        if stackLoss < minLoss:
            minLoss = stackLoss
            bestStack = stack

    queue.put([bestStack, minLoss, failureTally, failedStacks])


if __name__ == "__main__":
    N = 5
    turnRatio = 3
    maxTurns = 3
    print(f'Optimizing {N} layers, {turnRatio}:1 turns ratio, with maximum {maxTurns} turns/layer')
    tic = time.perf_counter()
    stacks = stackups(N, turnRatio, maxTurns)
    print(f'Analyzing {len(stacks)} options...')
    tic1 = time.perf_counter()

    b = .02
    f = 1000000
    l = .2
    r = .001

    # minLoss = 1000000000
    # bestStack = 0
    # failureTally = 0
    # failedStacks = []
    # for stack in stacks:
    #     #print(stack)
    #     #print(failureTally)
    #     #print(stack)
    #     try:
    #         solutionVector = list(current_sharing_numeric(stack, b, f, l, r))
    #     except numpy.linalg.LinAlgError:
    #         solutionVector = [100] * 3*N
    #         failureTally = failureTally + 1
    #         failedStacks.append(stack)
        
    #     stackLoss = 0
    #     d = math.sqrt(2*(1.68*math.pow(10,-8))/((2*math.pi*f)*(4*math.pi*pow(10,-7))))
    #     R = 1.68*math.pow(10,-8)*l/(d*b)

    #     for i in range(N,3*N):
    #         stackLoss = stackLoss + .5*R*((b*solutionVector[i])**2)
    #     #print(stackLoss)
    #     if (stackLoss < minLoss):
    #         minLoss = stackLoss
    #         bestStack = stack
    # toc = time.perf_counter()

    # print(f'Optimized Stackup: {bestStack}')
    # print(f'Minimum Loss (for 1A on high current winding): {minLoss:0.4f} W')
    print(f"Stackup Generation Time: {tic1 - tic:0.4f} seconds")
    # print(f"Calculation Time (asynchronous): {toc - tic1:0.4f} seconds")
    # print(f"Total Optimization Time: {toc - tic:0.4f} seconds")
    # print(f'Failed Stacks: {failedStacks}. Count {failureTally}')

    tic = time.perf_counter()
    queue = multiprocessing.Queue()
    threadCount = multiprocessing.cpu_count()
    stacksDivided = divide(threadCount, stacks)
    stacksDividedList = [list(s) for s in stacksDivided]
    #print(stacksDividedList)
    #print(len(stacksDividedList))
    solvers = [multiprocessing.Process(target=solver, args=(queue, s, b, f, l, r, N)) for s in stacksDividedList]
    for s in solvers:
        s.start()

    for s in solvers:
        s.join()

    results = [queue.get() for _ in solvers]
    minLoss = 1000000000
    bestStack = 0
    failureTally = 0
    failedStacks = []
    for result in results:
        if result[1] < minLoss:
            minLoss = result[1]
            bestStack = result[0]
        failureTally = failureTally + result[2]
        failedStacks.extend(result[3])


    toc = time.perf_counter()
    print(f"Calculation Time (paralleled): {toc-tic:0.4f} seconds")
    print(f'Optimized Stackup: {bestStack}')
