colordict = {
        1: int("931621", 16),
        0.9: int("A02E3C", 16),
        0.8: int("AD4756", 16),
        0.7: int("BA6070",16),
        0.6: int("C67989",16),
        0.5: int("D292A2",16),
        0.4: int("DEACBA",16),
        0.3: int("E9C7D1",16),
        0.2: int("F4E1E8",16),
        0.1: int("FEFDFD",16),
        0: int("FCFCFD",16),
        -0.1: int("E3E3FC",16),
        -0.2: int("E0E0FC",16),
        -0.3: int("C5C5FB",16),
        -0.4: int("A9A9FB",16),
        -0.5: int("8E8EFA",16),
        -0.6: int("7272F9",16),
        -0.7: int("5757F9",16),
        -0.8: int("3B3BF8",16),
        -0.9: int("2020F7",16),
        -1: int("0505F7",16),
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
