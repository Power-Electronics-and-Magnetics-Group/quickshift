demarcators = ['s','p']
def func(listKind,value,seriesFlag,parallelFlag):

    x = []
    z = value
    while (z < len(listKind)-1):
        if(seriesFlag):
            x.append(demarcators[parallelFlag])
            x.append(listKind[value])
            z+=1
            x.append(func(listKind,z,1,0))
            print(x)
        elif(parallelFlag):
            x.append(demarcators[parallelFlag])
            x.append(listKind[value])
            z+=1
            x.append(func(listKind,z,0,1))
            print(x)
    return(x)
print(func([1,2,3,4],0,1,0))
