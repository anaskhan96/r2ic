class table_stack:
	def __init__(self):
		self.items = []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		self.items.pop()

	def peek(self):
		return self.items[len(self.items)-1]

class symbol_table:
	def __init__(self, name, parent): # parent is another object of the symbol_table class
		self.symbols = {}
		self.name = name
		self.children = {} # to store all scopes inside an enclosing one
		self.parent = parent

	def insert(self, symbol, token): # eg. symbol = 'if', token = ['KEYWORD', 'if']
		if symbol not in self.symbols:
			self.symbols[symbol] = token	

	def lookup(self, symbol):
		return self.symbols[symbol]

	def get_parent(self):
		return self.parent

	def put_child(self, name, child): # eg. name = 'if_scope_1', child = the symbol_table object of the scope
		self.children[name] = child

	def get_child(self, name):
		return self.children[name]