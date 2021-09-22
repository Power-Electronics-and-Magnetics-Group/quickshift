from currentSharing_general import current_sharing_numeric
from currentSharing_general import current_sharing_symbolic

from stackups_michael import stackups

def loss(ff):
    loss_sum=0
    for term in ff:
        loss_sum = loss_sum + term**2 
        return loss_sum

if __name__ == "__main__":
    N = 5
    turnRatio = 3
    stacks = stackups(N,turnRatio)

    minLoss = 1000000000
    bestStack = 0
    failureTally = 0

    for stack in stacks:
        print(stack)
        solutionVector = list(current_sharing_numeric(N, stack[0], stack[1], .02, 1000000, .2, .001))
        #print(solutionVector)
        if (solutionVector == []):
            failureTally = failureTally + 1
        else:
            stackLoss = 0
            for i in range(N,3*N):
                stackLoss = stackLoss + (solutionVector[0][i]**2)
            #print(stackLoss)
            if (stackLoss < minLoss):
                minLoss = stackLoss
                bestStack = stack
    print(bestStack)
    print(minLoss)
    print(failureTally)
