from currentSharing import current_sharing_numeric
from currentSharing import current_sharing_symbolic
from stackups import stackups
import math

def loss(ff):
    loss_sum=0
    for term in ff:
        loss_sum = loss_sum + term**2 
        return loss_sum

if __name__ == "__main__":
    N = 5
    turnRatio = 1.5
    maxTurns = 4
    stacks = stackups(N, turnRatio, maxTurns)
    print(len(stacks))

    b = .02
    f = 1000000
    l = .2
    r = .001

    minLoss = 1000000000
    bestStack = 0
    failureTally = 0

    for stack in stacks:
        #print(stack)
        #print(failureTally)
        #print(stack)
        solutionVector = list(current_sharing_numeric(stack, b, f, l, r))
        #print(solutionVector)
        if (solutionVector == []):
            failureTally = failureTally + 1
        else:
            stackLoss = 0
            d = 2*(1.68*math.pow(10,-8))/((2*math.pi*f)*(4*math.pi*pow(10,-7)))
            R = 1.68*math.pow(10,-8)*l/(d*b)
            for i in range(N,3*N):
                stackLoss = stackLoss + .5*R*((b*solutionVector[i])**2)
            #print(stackLoss)
            if (stackLoss < minLoss):
                minLoss = stackLoss
                bestStack = stack
    print(bestStack)
    print(minLoss)
    print(failureTally)