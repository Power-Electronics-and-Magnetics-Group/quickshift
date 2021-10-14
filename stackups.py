import numpy as np
from itertools import combinations
from itertools import product
import pprint
import math
from scipy.special import comb
from stackupClasses import Layer, SeriesNode, ParallelNode, Node, Stackup

def stackups(N, turnsRatio, maxTurns):
	'''
	Generates list of valid stackups for N layer transformer with supplied turns ratio. Maximum 1 turn per layer.

	Parameters:
	-----------
	N : int
		Number of turns.
	turnsRatio : int or float
		Desired turns ratio. 
	maxTurns : int
		Maximum amount of turns to put on a single layer.

	Returns:
	--------
	stackupList
		List of valid stackups.
	'''
	#Input Validation
	if (N <=2 or type(N) != int): 
		raise valueError('Invalid N')
	if (turnsRatio <= 0): 
		raise valueError('Invalid turns ratio')

	#TurnsRatio should be >= 1
	if (turnsRatio < 1): 
		turnsRatio = 1/turnsRatio
		if (not turnsRatio.is_integer()):
			raise valueError('Invalid turns ratio')
		else: turnsRatio = int(turnsRatio)

	#Generate [1,...,N]
	layers = [0] * N
	for i in range(1, N+1):
		layers[i-1] = i

	#Generate valid turn pairs. 
	pairs = turnPairs(N, turnsRatio, maxTurns)
	#print(pairs)
	stackupList = []

	#Iterate over all the turn pairs
	for pair in pairs:
		primaryLayers = layerAssignments(N,pair,maxTurns)							#Generate primary layer combinations
		#print(primaryLayers)
		for pL in primaryLayers:													#Iterate over them
			sL = tuple(set(layers).difference(pL))									#Secondary list is the remaining layers
			primaryConnection = layerConnections(pL, pair[0], maxTurns)				#Generate primary connections
			secondaryConnection = layerConnections(sL, pair[1], maxTurns)			#Generate secondary connections

			for pConnect in primaryConnection:
				for sConnect in secondaryConnection:
					stackupList.append(Stackup(pConnect, sConnect, N))

	return stackupList

def turnPairs(N, turnsRatio, maxTurns):
	'''
	Returns valid pairs of turn counts for a N layer transformer, assuming maximum 1 turn per layer.

	Parameters:
	-----------
	N : int
		Number of turns.
	turnsRatio : int or float
		Desired turns ratio. turnsRatio >= 1
	maxTurns : int
		Maximum amount of turns to put on a single layer.

	Returns:
	--------
	turnPairs
		list of lists, each inner list represents a valid turn pair, with turnPairs[0] turns on the primary
		and turnPairs[1] turns on the secondary.
	'''
	#Input validation
	if (N <=2 or type(N) != int): raise valueError('Invalid N')
	if (turnsRatio <= 0): raise valueError('Invalid turns ratio')

	if (turnsRatio < 1): turnsRatio = 1/turnsRatio

	maxTotalTurns = N * maxTurns;

	nFlag = 1						#True while haven't exceeded N
	turnPairs = []					#Empty list to put turn pairs in
	p=1								#start with 1 turn in primary

	while nFlag:
		s = p * turnsRatio														#Set S based on turns ratio
		if ((s + p) > maxTotalTurns): nFlag = 0									#Not valid if s+p>maxTotalTurns. Break out of loop
		else: 
			if (isinstance(s,int) or s.is_integer()): turnPairs.append([p,int(s)])	#append to list if valid
		p = p+1																	#Increment p counter

	return turnPairs

def layerAssignments(N, turnPair, maxTurns):
	'''
	Selects different combinations of layers for a given set of turns and a layer count.

	Parameters:
	-----------
	N : int
		Number of turns.
	turnPair: int list of length 2
		Pair of turn counts. turnPair[0] turns on the primary, turnPair[1] turns on the secondary.
	maxTurns : int
		Maximum amount of turns to put on a single layer.

	Returns:
	--------
	primaryLayerAssignments
		List of lists. Each inner list is a unique set of layers that can function as the primary for
		the specified N and turnPair, with a max of 1 turn per layer.
	'''
	#Input Validation
	if (N <=2 or type(N) != int): raise valueError('Invalid N')
	if (len(turnPair) != 2): raise valueError('Invalid Turn Pairs')

	#Generate list [1,..,N]
	layers = [0] * N
	for i in range(1, N+1):
		layers[i-1] = i

	#Possible number of layers on the primary
	minPrimaryLayers = int(math.ceil(float(turnPair[0])/maxTurns))
	minSecondaryLayers = int(math.ceil(float(turnPair[1])/maxTurns))
	if ((minPrimaryLayers + minSecondaryLayers) > N): return []
	if (turnPair[1]==turnPair[0]): validPrimaryCounts=range(minPrimaryLayers,N//2)
	else: validPrimaryCounts = range(minPrimaryLayers, N - minSecondaryLayers + 1)	
	primaryLayerAssignments = []
	for j in validPrimaryCounts:
		options = list(combinations(layers,j))
		for option in options:
			mirror = [(N-x)+1 for x in option]
			mirror = tuple(reversed(mirror))
			if ((mirror in options) and (mirror != tuple(option))): 
				options.remove(mirror)
		primaryLayerAssignments.extend(options)	#Generate all combinations

	return primaryLayerAssignments

def layerConnections(layers, N, maxTurns):
	'''
	Returns combinations that place N turns on the specified layers.

	Parameters:
	-----------
	layers : int list
		Layers that will be connected together with specified amount of turns.
	N : int
		Number of turns.
	maxTurns : int
		Maximum amount of turns to put on a single layer.

	Returns:
	--------
	connections
		List of layer connections that put N turns on the provided layers. 
	'''
	#If called on single layer, just return the layer with specified turns.
	if (type(layers) == int): 
		if (N <= maxTurns): return set([Layer(layers,N)])
		else: return None
	if (len(layers) == 1): 
		if (N <= maxTurns): return set([Layer(layers[0],N)])
		else: return None

	#If only need one turn, can only put layers in parallel. 
	if (N == 1): return([parallelConnect(layers,1)])

	num = len(layers)

	seriesConnections = set()
	#Make all possible connections with a series node at the top of the tree
	for i in range(1,1+int(num/2)):										#Limit set size b/c problem is symmetric
		seriesSetsLeft = list(combinations(layers,i))
		if ((num/2)==i): seriesSetsLeft = seriesSetsLeft[:len(seriesSetsLeft)//2]			#Another symmetry, can eliminate entries
		seriesSetsLeft = set(seriesSetsLeft)
		for seriesSetLeft in seriesSetsLeft:
			seriesSetRight = tuple(set(layers).difference(seriesSetLeft))
			for j in range(1,N):
				seriesLeftConnections = layerConnections(seriesSetLeft,j,maxTurns)
				seriesRightConnections = layerConnections(seriesSetRight,N-j,maxTurns)
				if ((seriesLeftConnections != None) and (seriesRightConnections != None)):
					for seriesLeftConnection in seriesLeftConnections:
						for seriesRightConnection in seriesRightConnections:
							a = SeriesNode(seriesLeftConnection,seriesRightConnection)
							a = a.standardForm()
							if (a not in seriesConnections): seriesConnections.add(a)

	connections = set()
	#Make all possible connections with a parallel node at the top of the tree:
	for i in range(1,1+int(num/2)):										#Limit set size b/c problem is symmetric
		parallelSetsLeft = list(combinations(layers,i))
		if ((num/2)==i): parallelSetsLeft = parallelSetsLeft[:len(parallelSetsLeft)//2]		#Another symmetry, can eliminate entries
		parallelSetsLeft = set(parallelSetsLeft)
		for parallelSetLeft in parallelSetsLeft:
			parallelSetRight = tuple(set(layers).difference(parallelSetLeft))
			parallelLeftConnections = layerConnections(parallelSetLeft,N,maxTurns)
			parallelRightConnections = layerConnections(parallelSetRight,N,maxTurns)
			if ((parallelLeftConnections != None) and (parallelRightConnections != None)):
				for parallelLeftConnection in parallelLeftConnections:
					for parallelRightConnection in parallelRightConnections:
						b = ParallelNode(parallelLeftConnection,parallelRightConnection)
						b = b.standardForm()
						if (b not in connections): connections.add(b)

	connections.update(seriesConnections)
	return connections

def seriesConnect(layers, turns = 1):
	'''
	Connects specified layers in series.

	Parameters:
	-----------
	layers : int list
		layers to be connected in series
	turns : int list
		Optional parameter. If not passed, all turns assumed to be 1. If passed, len(turns)==len(layers)
		and each layer will be assigned its corresponding turn.

	Returns:
	--------
		Series connection of all input layers.
	'''
	if (turns == 1): turns = [1] * len(layers)
	elif (len(turns) != len(layers)): raise valueError

	if (len(layers) == 2): #Base Case
		return SeriesNode(Layer(layers[0],turns[0]),Layer(layers[1],turns[1]))
	else: #Put first layer in series with the remaining layers
		return SeriesNode(Layer(layers[0],turns[0]),seriesConnect(layers[1:],turns[1:]))

def parallelConnect(layers, turns = 1):
	'''
	Connects specified layers in parallel.

	Parameters:
	-----------
	layers : int list
		layers to be connected in parallel
	turns : int
		Optional parameter. If not passed, all turns assumed to be 1. If passed, all the parallel turns will
		be created with specified turns on them.

	Returns:
	--------
		Parallel connection of all input layers.
	'''
	if (not isinstance(turns, int)): raise valueError

	if (len(layers) == 2): #Base Case
		return ParallelNode(Layer(layers[0],turns),Layer(layers[1],turns))
	else: #Put first layer in series with the remaining layers
		return ParallelNode(Layer(layers[0],turns),parallelConnect(layers[1:],turns))

# a = layerConnections([2,3,4,5],2,1)
# for c in a:
# 	print(c)
stacks = stackups(4,2,8)
print(len(stacks))
for stack in stacks:
	print(stack)