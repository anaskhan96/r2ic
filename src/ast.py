tab_val = 0

class AbstractSyntaxTree:
	def __init__(self):
		self.value = None
		self.left = None
		self.right = None			

	def addNode(self, value, left, right):
		self.value = value
		self.left = left
		self.right = right

	def addLeaf(self, value):
		self.value = value

	def printAST(self):
		print('\t'*tab_val+self.value)
		if self.left != None:
			tab_val += 1
			self.left.printAST()
			tab_val -= 1
		if self.right != None:
			tab_val += 1
			self.right.printAST()
			tab_val -= 1