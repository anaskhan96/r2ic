import re

class table_stack:
	def __init__(self):
		self.items = []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		return self.items.pop()

	def peek(self):
		return self.items[len(self.items)-1]

	def get_length(self):
		return len(self.items)

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
	
	def get_symbols(self):
		return self.symbols

	def get_name(self):
		return self.name

	def get_parent(self):
		return self.parent

	def put_child(self, name, child): # eg. name = 'if_scope_1', child = the symbol_table object of the scope
		self.children[name] = child

	def get_child(self, name):
		return self.children[name]

	def get_children(self):
		return self.children.keys()

	def print_table(self):
		print ("Table :  ", self.name)		
		for i in self.symbols:
			print(i , self.symbols[i])
		print()	
		for i in self.children:
			self.children[i].print_table()	


def find_most_recent_scope(scope_name, symtab):
	pattern = re.compile("{}\d+".format(scope_name))
	key_digits = []
	for key in symtab.children:
		if pattern.match(key):
			key_digits.append(int(key[-1]))
	if len(key_digits) == 0:
		return 0
	else:
		return max(key_digits)

	
		