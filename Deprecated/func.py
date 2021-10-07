demarcators = ['s','p']
def func(listKind,seriesFlag,parallelFlag):
        x = []
        z = 0
        if(seriesFlag):
            if(len(listKind)==2):
                x.append(demarcators[0])
                x.append(listKind[0])
                x.append(listKind[1])
                return x
            else:
                z+=1
                x.append(func(listKind[z:],1,0))
        elif(parallelFlag):
            if(len(listKind)==2):
                x.append(demarcators[1])
                x.append(listKind[0])
                x.append(listKind[1])
                return x
            else:
                z+=1
                x.append(func(listKind[z:],0,1)
func([1,2],1,0)
