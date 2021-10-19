from currentSharing import current_sharing_numeric
from currentSharing import current_sharing_symbolic
from stackups import stackups
from stackupClasses import Layer, SeriesNode, ParallelNode, Node, Stackup
import math
import time
import numpy

def loss(ff):
    loss_sum=0
    for term in ff:
        loss_sum = loss_sum + term**2 
        return loss_sum

if __name__ == "__main__":
    #[Stack: Primary - [L1,1T]; Secondary - (P,(S,[L4,1T],[L6,1T]),(S,[L5,1T],(P,[L2,1T],[L3,1T]))), 
    # N = 6
    # p = Layer(1,1)
    # s = ParallelNode(SeriesNode(Layer(4,1),Layer(6,1)), SeriesNode(Layer(5,1), ParallelNode(Layer(2,1),Layer(3,1))))

    # stack = Stackup(p,s,N)

    # b = .02
    # f = 1000000
    # l = .2
    # r = .001

    #solutionVector = list(current_sharing_numeric(stack, b, f, l, r))
    # solutionVector = list(current_sharing_symbolic(stack))
    # print(solutionVector)

    N = 8
    turnRatio = 2
    maxTurns = 1
    print(f'Optimizing {N} layers, {turnRatio}:1 turns ratio, with maximum {maxTurns} turns/layer')
    tic = time.perf_counter()
    stacks = stackups(N, turnRatio, maxTurns)
    print(f'Analyzing {len(stacks)} options...')
    tic1 = time.perf_counter()

    b = .02
    f = 1000000
    l = .2
    r = .001

    minLoss = 1000000000
    bestStack = 0
    failureTally = 0
    failedStacks = []
    for stack in stacks:
        #print(stack)
        #print(failureTally)
        #print(stack)
        try:
            solutionVector = list(current_sharing_numeric(stack, b, f, l, r))
        except numpy.linalg.LinAlgError:
            solutionVector = [100] * 3*N
            failureTally = failureTally + 1
            failedStacks.append(stack)
        
        stackLoss = 0
        d = math.sqrt(2*(1.68*math.pow(10,-8))/((2*math.pi*f)*(4*math.pi*pow(10,-7))))
        R = 1.68*math.pow(10,-8)*l/(d*b)

        for i in range(N,3*N):
            stackLoss = stackLoss + .5*R*((b*solutionVector[i])**2)
        #print(stackLoss)
        if (stackLoss < minLoss):
            minLoss = stackLoss
            bestStack = stack
    toc = time.perf_counter()

    print(f'Optimized Stackup: {bestStack}')
    print(f'Minimum Loss (for 1A on high current winding): {minLoss:0.4f} W')
    print(f"Stackup Generation Time: {tic1 - tic:0.4f} seconds")
    print(f"Calculation Time: {toc - tic1:0.4f} seconds")
    print(f"Total Optimization Time: {toc - tic:0.4f} seconds")
    print(f'Failed Stacks: {failedStacks}. Count {failureTally}')