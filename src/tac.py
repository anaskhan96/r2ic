class ThreeAddressCode:
	def __init__(self):
		self.symbolTable = None
		self.allCode = []
		self.tempVarCount = 0

	def generateCode(self, operation, arg1, arg2, result):
		code = Quadruple(operation, arg1, arg2, result)
		#code.print_quadruple()
		self.allCode.append(code)

	def print_code(self):
		print("\tOperation\tArg1\t\tArg2\t\tResult")
		for i in self.allCode:
			print("\t", i.operation, "\t\t", i.arg1, "\t\t", i.arg2, "\t\t", i.result)

class Quadruple:
	def __init__(self, operation, arg1, arg2, result):
		self.operation = operation
		self.arg1 = arg1
		self.arg2 = arg2
		self.result = result

	def print_quadruple(self):
		print(self.operation, self.arg1, self.arg2, self.result)