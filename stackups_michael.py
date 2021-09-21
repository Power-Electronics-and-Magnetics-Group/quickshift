import numpy as np
from itertools import combinations
from itertools import product
import pprint
from scipy.special import comb

def stackups(N, turnsRatio):
	if (N <=2 or type(N) != int): 
		raise valueError('Invalid N')
	if (turnsRatio <= 0): 
		raise valueError('Invalid turns ratio')

	if (turnsRatio < 1): turnsRatio = 1/turnsRatio

	layers = [0] * N
	for i in range(1, N+1):
		layers[i-1] = i

	#Generate valid turn pairs. 
	pairs = turnPairs(N, turnsRatio)
	#rint(pairs)
	stackupList =[]
	for pair in pairs:
		#print(pair)
		primaryLayers = layerAssignments(N,pair)
		#print(primaryLayers)
		for pL in primaryLayers:
			sL = tuple(set(layers).difference(pL))
			primaryConnection = layerConnections(pL, pair[0])
			secondaryConnection = layerConnections(sL, pair[1])
			if (secondaryConnection[0] != 's' and secondaryConnection[0] != 'p'):
				for connect in secondaryConnection:
					stackupList.append((primaryConnection,connect))
			else: 
				stackupList.append((primaryConnection,secondaryConnection))

	return stackupList

def turnPairs(N, turnsRatio):
	if (N <=2 or type(N) != int): raise valueError('Invalid N')
	if (turnsRatio <= 0): raise valueError('Invalid turns ratio')

	nFlag = 1
	turnPairs = []
	p=1

	while nFlag:
		s = p * turnsRatio
		if ((s + p) > N): nFlag = 0
		else: 
			if (isinstance(s,int) or s.is_integer()): turnPairs.append([p,s])
		p = p+1

	return turnPairs

def layerAssignments(N, turnPairs):
	if (N <=2 or type(N) != int): raise valueError('Invalid N')
	if (len(turnPairs) != 2): raise valueError('Invalid Turn Pairs')

	layers = [0] * N
	for i in range(1, N+1):
		layers[i-1] = i

	validPrimaryCounts = range(turnPairs[0],N - turnPairs[1] + 1)
	primaryLayerAssignments = []
	for j in validPrimaryCounts:
		primaryLayerAssignments.extend(list(combinations(layers,j)))

	return primaryLayerAssignments

def layerConnections(layers, turns):
	if (type(layers) == int): return layers
	if (len(layers) == 1): return layers[0]
	if (len(layers) < turns): return valueError('Invalid turn number for specified layers.')

	num = len(layers)
	p_count = num-turns
	s_count = turns-1
	if (p_count==0): return seriesConnect(layers)
	if (s_count==0): return parallelConnect(layers)
	else:
		connections = []
		for i in range(1, num - turns + 1):
			set1 = list(combinations(layers,i))
			for s in set1:
				s2 = tuple(set(layers).difference(s))
				a = layerConnections(s,1)
				b = layerConnections(s2,turns-1)
				if (type(b[0]) == str):
					connections.append(['s',a,b])
				else:
					for connection in b:
						connections.append(['s',a,connection])
		return connections

def seriesConnect(layers):
	if (len(layers) == 2):
		return ['s',layers[0],layers[1]]
	else:
		return ['s',layers[0],seriesConnect(layers[1:])]

def parallelConnect(layers):
	if (len(layers) == 2):
		return ['p',layers[0],layers[1]]
	else:
		return ['p',layers[0],parallelConnect(layers[1:])]

#print(returnSeriesParallelPair(stackups(8,3),0))
#print(turnPairs(12,1.5))
#print(layerAssignments(5,[2,3]))
#print(layerConnections([2,3,4],3))
#print(layerConnections([1,2,3,4,5],4))
