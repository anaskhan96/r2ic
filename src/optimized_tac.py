from symbol_table import table_stack
tac_stack = table_stack()
mult_flag = 0
loop_values = []

loop_unroll = False
ad_hoc_constant_prop = {}

class ThreeAddressCode:
	def __init__(self):
		self.symbolTable = None
		self.allCode = []
		self.tempVarCount = 1
		self.label_counter = 1
		self.temp_symbol_table = {}
		self.loop_statement_count = 0
		self.loop_staus = ''
	
	def loop_begin(self):
		print('toogle beig')
		self.loop_staus = 'begin'
		
	def loop_end(self):
		print('toogle end')
		
		self.loop_staus = 'end'

	def generateCode(self, operation, arg1, arg2, result):
		code = Quadruple(operation, arg1, arg2, result)
		#code.print_quadruple()
		self.allCode.append(code)

	def print_code(self):
		print("\tOperation\tArg1\t\tArg2\t\tResult")
		for i in self.allCode:
			print("\t", i.operation, "\t\t", i.arg1, "\t\t", i.arg2, "\t\t", i.result)

	def generate_icg(self, operation, arg1, arg2, result):
		global ad_hoc_constant_prop
		global mult_flag
		global loop_unroll
		
		if operation == '+' or operation == '-':
			if tac_stack.get_length() == 1:
				if mult_flag == 1:
					mult_flag -= 1
			
				tac_stack.push('t'+str(self.tempVarCount))
				self.temp_symbol_table[self.tempVarCount] = result
				self.tempVarCount += 1

			elif tac_stack.get_length() > 1:
				tac_stack.push('t'+str(self.tempVarCount))
				self.temp_symbol_table[self.tempVarCount] = result
				self.tempVarCount += 1
				mult_flag -= 1
			
			else:
				tac_stack.push('t'+str(self.tempVarCount))
				self.temp_symbol_table[self.tempVarCount] = result
				self.tempVarCount += 1
	
		elif operation == '*' or operation == '/':
		
			if tac_stack.get_length() == 1:
				if not mult_flag == 1:
					mult_flag -= 1

				tac_stack.push('t'+str(self.tempVarCount))
				self.temp_symbol_table[self.tempVarCount] = result
				self.tempVarCount += 1

			elif tac_stack.get_length() > 1:
				tac_stack.push('t'+str(self.tempVarCount))
				self.temp_symbol_table[self.tempVarCount] = result
				self.tempVarCount += 1
				mult_flag -= 1
			
			else:

				tac_stack.push('t'+str(self.tempVarCount))
				mult_flag += 1

				self.temp_symbol_table[self.tempVarCount] = result
				self.tempVarCount += 1
		
		elif operation == '=':
				if tac_stack.get_length() > 0:
					self.generateCode(operation, str(self.temp_symbol_table[len(self.temp_symbol_table)]), '', result)
					while tac_stack.get_length() > 0:
						tac_stack.pop()
					ad_hoc_constant_prop[result] = str(self.temp_symbol_table[len(self.temp_symbol_table)])

				else:
					if(str(arg1) in ad_hoc_constant_prop.keys()):
						self.generateCode(operation, ad_hoc_constant_prop[str(arg1)], '', result)
					else:
						self.generateCode(operation, str(arg1), '', result)
						ad_hoc_constant_prop[result] = str(arg1)

		elif operation == "goto":
			self.generateCode(operation, arg1, arg2, result)

		elif operation == "FOR":
			print ("in for ", arg1, arg2)
			if (int(arg2) - int(arg1) > 10 ):
				self.generateCode(operation, arg1, arg2, result)
			else:
				
				loop_unroll = True
				loop_values.append(int(arg1))
				loop_values.append(int(arg2))
				
				return
				
		elif operation.endswith('F'):
			self.generateCode(operation, str(arg1), str(arg2), result)
		
		elif operation == "print":
			self.generateCode("SWI", '', '', result)	
		
		if self.loop_staus == 'begin':
			self.loop_statement_count +=1

		elif self.loop_staus == 'end' and loop_unroll:
			op = []
			for i in range(self.loop_statement_count):
				op.append (self.allCode.pop())
			
			for i in range (loop_values[0], loop_values[1]):
				for j in op[1::-1]:
					self.allCode.append(j)
		
			loop_unroll = False
			self.loop_staus = ''
		else:
			print("Invalid operation")
		
	def putLabel(self, kind):
		label = len(self.allCode)
		if kind == 'result':
			for i in reversed(self.allCode):
				if i.result.endswith("S"):
					i.result += str(label)
					break
		elif kind == 'arg1':
			for i in reversed(self.allCode):
				if i.arg1.endswith("S"):
					i.arg1 += str(label)
					break
		else:
			allCodeReverse = self.allCode[::-1]
			for i in range(len(allCodeReverse)):
				if allCodeReverse[i].result.endswith("S"):
					self.generate_icg("goto", "S"+str(label-i-1), '', '')
					break
		

class Quadruple:
	def __init__(self, operation, arg1, arg2, result):
		self.operation = operation
		self.arg1 = arg1
		self.arg2 = arg2
		self.result = result

	def print_quadruple(self):
		print(self.operation, self.arg1, self.arg2, self.result)