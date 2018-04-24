tab_val = 0

class AbstractSyntaxTree:
	def __init__(self, value, left, right):
		self.value = value
		self.left = left
		self.right = right			

	def addNode(self, value, left, right):
		return AbstractSyntaxTree(value, left, right)

	def addLeaf(self, value):
		return AbstractSyntaxTree(value, None, None)

	def printAST(self):
		global tab_val
		print('\t'*tab_val+self.value)
		if self.left != None:
			tab_val += 1
			self.left.printAST()
			tab_val -= 1
		if self.right != None:
			tab_val += 1
			self.right.printAST()
			tab_val -= 1