colordict = {
        1: int("FF1010", 16),
        0.9: int("FF2727", 16),
        0.8: int("FF3F3F", 16),
        0.7: int("FF5757",16),
        0.6: int("FF6F6F",16),
        0.5: int("FF8787",16),
        0.4: int("FF9F9F",16),
        0.3: int("FFB7B7",16),
        0.2: int("FFCFCF",16),
        0.1: int("FFE7E7",16),
        0: int("FFFFFF",16),
        -0.1: int("E8E8F5",16),
        -0.2: int("D1D1EC",16),
        -0.3: int("BABAE3",16),
        -0.4: int("A3A3DA",16),
        -0.5: int("8C8CD1",16),
        -0.6: int("7575C8",16),
        -0.7: int("5E5EBF",16),
        -0.8: int("4747B6",16),
        -0.9: int("3030AD",16),
        -1: int("1919A4",16),
}

def colordetermine(maxCurrent, testCurrent):
    currentRatio = testCurrent / maxCurrent 
    return (colordict[round(currentRatio,1)])

def listDeterminer(currentList):
    hexList = []
    maxCurrent = max(currentList)
    for i in currentList:
        hexList.append(format(colordetermine(maxCurrent,i),'x'))
    return hexList
'''
print("max: 1.0, test: 1.0, round: " + str(round(1.0,1)))
print(colordetermine(1.0,1.0))
print("max: 1.0, test: .25, round: " + str(round(.25,1)))
print(colordetermine(1.0,.25))
print("max: 1.0, test: -0.75, round: " + str(round(-0.75,1)))
print(colordetermine(1.0,-.75))

'''
