demarcators = ['s','p']
def stackupTree(listKind,seriesFlag,parallelFlag):
    x = []
    if (seriesFlag):
        if(len(listKind)==2):
            x.append(demarcators[0])
            x.append(listKind[0])
            x.append(listKind[1])
            return x
        else:
            x.append(demarcators[0])
            x.append(listKind[0])
            f = stackupTree(listKind[1:],1,0)
            x.append(f)
    elif(parallelFlag):
        if(len(listKind)==2):
            x.append(demarcators[1])
            x.append(listKind[0])
            x.append(listKind[1])
            return x
        else:
            x.append(demarcators[1])
            x.append(listKind[0])
            f=stackupTree(listKind[1:],0,1)
            x.append(f)
print(stackupTree([1,2,3,4],1,0))

