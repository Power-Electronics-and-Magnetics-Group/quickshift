class Stackup:
	'''Stackup class specifies a set of two windings (each are node objects) and a 
	number of turns. Used for transformer specification.'''
	def __init__(self, primary, secondary, N):
		self.primary = primary
		self.secondary = secondary
		self.N = N

	def __eq__(self, other):
		if (isinstance(other, Stackup)):
			nEq = self.N == other.N
			pEq = (self.primary == other.primary) or (self.primary == other.secondary)
			sEq = (self.secondary == other.secondary) or (self.secondary == other.primary)
			return (nEq and pEq and sEq)
		return False

	def __repr__(self):
		return f'Stack: Primary - {self.primary.__repr__()}; Secondary - {self.secondary.__repr__()}'

	def turnsRatio(self):
		'''Returns turns ratio of the stackup.'''
		n1 = self.primary.turns
		n2 = self.secondary.turns

		if (n1 > n2):
			return n1/n2
		else: return n2/n1

	def validStackup(self):
		'''Validates that the stackup has all necessary layers, and they are all in range of N'''
		primLayers = self.primary.allLayers()
		secondaryLayers = self.secondary.allLayers()
		primLayers.extend(secondaryLayers)
		layers = sorted(primLayers)
		correct = list(range(1, self.N + 1))
		return (layers == correct)

	def turnCount(self):
		'''Returns turns on each layer in the stackup.'''
		Turns = self.primary.turnCount()
		secTurns = self.secondary.turnCount()
		Turns.extend(secTurns)
		TurnsSort = sorted(Turns, key=lambda x: x[0])
		turnCounts = [0] * self.N
		for i in range(0,self.N):
			turnCounts[i] = TurnsSort[i][1]
		return turnCounts

class Node(object):
	'''Node class specifies a binary tree used to represent transformer connections.'''

	def __init__(self, left, right):
		self.left = left
		self.right = right

	def __eq__(self,other):
		if (isinstance(other,Node)):
			return (str(self) == str(other))
		return False

	def __hash__(self):
		return hash(str(self))

	def hasLayer(self):
		'''Returns a layer that is contained by this node.'''
		return self.left.hasLayer()

	def allLayers(self):
		'''Returns all layers contained by this node.'''
		a = self.left.allLayers()
		a.extend(self.right.allLayers())
		return a

	def turnCount(self):
		'''Returns array of layers and their respective turn counts.'''
		a = self.left.turnCount()
		b = self.right.turnCount()
		a.extend(b)
		return a

	def swap(self):
		'''Swaps position of left and right children on this node.'''
		temp = self.right
		self.right = self.left
		self.left = temp
		return 0

	# def sortChildren(self):
	# 	if (isinstance(self.left,Layer) and isinstance(self.right,Layer)):
	# 		if (self.left.number > self.right.number): self.swap()
	# 		return
	# 	if (isinstance(self.left,Layer) and isinstance(self.right,Node)):
	# 		self.swap()
	# 		return
	# 	if (isinstance(self.left,SeriesNode) and isinstance(self.right,ParallelNode)):
	# 		self.swap()
	# 		return
	# 	if ((isinstance(self.left,ParallelNode) and isinstance(self.right,ParallelNode)) or (isinstance(self.left,SeriesNode) and isinstance(self.right,SeriesNode))):
	# 		a = min(self.left.allLayers())
	# 		b = min(self.right.allLayers())
	# 		if (b < a): self.swap()
	# 		return

	def sortTree(self):
		'''Re-orders tree such that smaller layer #s are the left children.'''
		if (isinstance(self.left,Layer) and isinstance(self.right,Layer)):
			if (self.left.number > self.right.number): self.swap()
			return
		if (isinstance(self.left,Node)): self.left.sortTree()
		if (isinstance(self.right,Node)): self.right.sortTree()
		return

	def standardForm(self):
		'''Returns a sorted but equivalent tree.'''
		self.sortTree()
		edgeNodes = self.findNodeEdge()
		nodePlusMinLayer = []
		for node in edgeNodes:
			minLayer = min(node.allLayers())
			nodePlusMinLayer.append([node, minLayer])
		edgeNodesAlmostSorted = sorted(nodePlusMinLayer, key=lambda x: x[1])
		edgeNodesSorted  = []
		for nodePlusLayer in edgeNodesAlmostSorted:
			edgeNodesSorted.append(nodePlusLayer[0])
		for node in edgeNodesSorted:
			node = node.standardForm()
		if (self.kind == 'P'):
			return parallelConnectNodes(edgeNodesSorted)
		if (self.kind == 'S'):
			return seriesConnectNodes(edgeNodesSorted)
		else: 
			return edgeNodesSorted[0]

	def findNodeEdge(self):
		'''Returns list of nodes that are attached to the edge of the cumulative node 
		(i.e. if self.kind=='P' and it is connected to several other parallel nodes,
		findNodeEdge will return the nodes connected to those parallel nodes.'''
		if (self.kind == self.left.kind): nodes = self.left.findNodeEdge()
		else: nodes = [self.left]
		if (self.kind == self.right.kind): b = self.right.findNodeEdge()
		else: b = [self.right]

		nodes.extend(b)
		return nodes

class ParallelNode(Node):
	'''Node subclass that specifies parallel connected children.'''
	kind = 'P'
	
	def __init__(self, left, right):
		super().__init__(left, right)
		self.turns = (.5*(self.left.turns + self.right.turns)) # NOT CORRECT. TO DO

	def __repr__(self):
		return f'(P,{self.left.__repr__()},{self.right.__repr__()})'

	def I_node(self):
		'''Returns current flowing through this node'''
		a = self.left.I_node()
		a.extend(self.right.I_node())
		return a

	def nodeCount(self):
		'''Counts total attached nodes, separated by kind [#S,#P].'''
		lN = self.left.nodeCount()
		rN = self.right.nodeCount()
		return [lN[0] + rN[0], 1 + lN[1] + rN[1]]

class SeriesNode(Node):
	'''Node subclass that specifies series connected children.'''
	kind = 'S'
	
	def __init__(self, left, right):
		super().__init__(left, right)
		self.turns = (self.left.turns + self.right.turns)

	def __repr__(self):
		return f'(S,{self.left.__repr__()},{self.right.__repr__()})'

	def I_node(self):
		'''Returns current flowing through this node'''
		return self.left.I_node()

	def nodeCount(self):
		'''Counts total attached nodes, separated by kind [#S,#P].'''
		lN = self.left.nodeCount()
		rN = self.right.nodeCount()
		return [1 + lN[0] + rN[0], lN[1] + rN[1]]

class Layer:
	'''Layer class specifies single layer in a transformer. Composed of turn count and layer number.'''
	kind = 'L'

	def __init__(self, number, turns):
		#if (not isinstance(number, int)): print(type(number))
		self.number = number
		self.turns = turns

	def __eq__(self, other):
		if (isinstance(other, Layer)):
			return (self.number == other.number) and (self.turns == other.turns)
		return False

	def __hash__(self):
		return hash(str(self.number)+','+str(self.turns))

	def __repr__(self):
		return f'[L{self.number},{self.turns}T]'

	def I_node(self):
		'''Returns own layer.'''
		return [self.number]

	def hasLayer(self):
		'''Returns own layer.'''
		return self.number

	def allLayers(self):
		'''Returns own layer.'''
		return [self.number]

	def turnCount(self):
		'''Returns layer number and turn count.'''
		return [[self.number, self.turns]]

	def nodeCount(self):
		'''Returns number of attached nodes.'''
		return [0, 0]

	def standardForm(self):
		'''Returns self to aid in construction of standardized stack representations.'''
		return self

def parallelConnectNodes(NodeList):
	'''Connect all nodes in NodeList in parallel.'''
	length = len(NodeList)
	if (length == 2):
		return ParallelNode(NodeList[0],NodeList[1])
	else:
		return ParallelNode(parallelConnectNodes(NodeList[0:length-1]),NodeList[length-1])

def seriesConnectNodes(NodeList):
	'''Connect all nodes in NodeList in series.'''
	length = len(NodeList)
	if (length == 2):
		return SeriesNode(NodeList[0],NodeList[1])
	else:
		return SeriesNode(seriesConnectNodes(NodeList[0:length-1]),NodeList[length-1])