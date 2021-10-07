from currentSharing_general import current_sharing_numeric
from currentSharing_general import current_sharing_symbolic

from stackups_michael import stackups

def loss(ff):
    loss_sum=0
    for term in ff:
        loss_sum = loss_sum + term**2 
        return loss_sum

if __name__ == "__main__":
    #stack = (2, ['s', 1, ['s', ['p', 3, 5], ['p', 4, 6]]])
    #a=current_sharing_symbolic(6, stack[0], stack[1])
    #b=current_sharing_numeric(6, stack[0], stack[1], .02, 10000000, .2, .001)
    #c=current_sharing_numeric_workaround(6, stack[0], stack[1], .02, 10000000, .2, .001)
    #b=current_sharing_numeric(6, stack[0], stack[1], 1, 10000000, .2, .01) #issues in parsing b and r
    #current_sharing_numeric(N, pl, sl, b, f, l, r, N_turns = 1, Ip = 1)
    #print(a)
    #print(b)
    #print(c)
    #print(b.subs(tau0,0))


    N = 8
    turnRatio = 3
    stacks = stackups(N,turnRatio)
    print(len(stacks))

    minLoss = 1000000000
    bestStack = 0
    failureTally = 0

    for stack in stacks:
        #print(failureTally)
        #print(stack)
        solutionVector = list(current_sharing_numeric(N, stack[0], stack[1], .02, 1000000, .2, .001))
        #print(solutionVector)
        if (solutionVector == []):
            failureTally = failureTally + 1
        else:
            stackLoss = 0
            for i in range(N,3*N):
                stackLoss = stackLoss + (solutionVector[i]**2)
            #print(stackLoss)
            if (stackLoss < minLoss):
                minLoss = stackLoss
                bestStack = stack
    print(bestStack)
    print(minLoss)
    print(failureTally)

    #solutionVector = list(current_sharing_numeric(8, ['s', 1, ['p', 2, ['p', 3, 4]]], ['s', 5, ['p', 8, ['p', 6, 7]]], .02, 1000000, .2, .001))
