import ply.yacc as yacc
from lex_analysis import tokens
from tac import ThreeAddressCode
from symbol_table import table_stack

threeAddressCode = ThreeAddressCode()
tac_stack = table_stack()

temp_var_no = 1
label_counter = 1

def generate_icg(operation, arg1, arg2, result):
	global temp_var_no
	if operation == '+' or operation == '-':
		if tac_stack.get_length() == 1:
			threeAddressCode.generateCode(operation, str(arg1), str(tac_stack.pop()), 't'+str(temp_var_no))
			tac_stack.push('t'+str(temp_var_no))
			# add 't'+str(temp_var_no) to symbol_table
			temp_var_no += 1

		elif tac_stack.get_length() > 1:
			threeAddressCode.generateCode(operation, str(tac_stack.pop()), str(tac_stack.pop()), 't'+str(temp_var_no))
			tac_stack.push('t'+str(temp_var_no))
			# add 't'+str(temp_var_no) to symbol_table
			temp_var_no += 1
		else:
			threeAddressCode.generateCode(operation, str(arg1), str(arg2), 't'+str(temp_var_no))
			tac_stack.push('t'+str(temp_var_no))
			# add 't'+str(temp_var_no) to symbol_table
			temp_var_no += 1
	
	elif operation == '*' or operation == '/':
		#print("Peek: ", tac_stack.peek(), "Length: ", tac_stack.get_length())
		threeAddressCode.generateCode(operation, str(arg1), str(arg2), 't'+str(temp_var_no))
		tac_stack.push('t'+str(temp_var_no))
		# add 't'+str(temp_var_no) to symbol_table
		temp_var_no += 1
	
	elif operation == '=':
			threeAddressCode.generateCode(operation, str(tac_stack.pop()), '', result)
			#tac_stack.push('t'+str(temp_var_no))

	elif operation.startswith('if'):
		threeAddressCode.generateCode(operation, str(arg1), str(arg2), result)
		threeAddressCode.generateCode("goto", 'L'+str(label_counter+2), '', '')
	
	else:
		print("Invalid operation")

def p_program(p):
	'''program : FN MAIN LPAREN RPAREN compoundStmt'''
	p[0] = p[5]

def p_compoundStmt_Stmt(p):
	'''compoundStmt : LBRACE Stmt moreStmt RBRACE
					| LBRACE Decl moreStmt RBRACE'''
	if p[1] == '{':
		p[0] = p[2]
	elif p[1] == 'if':
		p[0] = p[1]

def p_moreStmt(p):
	'''moreStmt : Stmt moreStmt
				| Decl moreStmt
				| empty'''
	p[0] = p[1]

def p_decl_Stmt(p):
	'''Decl : LET VarList
			| LET AssignExpr'''
	p[0] = p[2]

def p_varlist(p):
	'''VarList : VarList COMMA ID
				| ID SEMICOLON'''
	if p[2] == ',':
		p[0] = p[3]
	else:
		p[0] = p[1]

def p_assignExpr(p):
	'''AssignExpr : ID EQUALS expression COMMA AssignExpr
					| ID EQUALS expression SEMICOLON'''
	p[0] = p[3]
	generate_icg('=', '', '', p[1])

def p_Stmt(p):
	'''Stmt : print_text SEMICOLON
			| expression SEMICOLON
			| AssignExpr
			| if
			| if_else '''
	p[0] = p[1]

def p_print(p):
	'''print_text : PRINTMAC LPAREN text RPAREN
					| PRINTLNMAC LPAREN text RPAREN'''
	p[0] = p[3][1:-1]

def p_text(p):
	'''text : STRINGZ '''
	p[0] = p[1]

def p_if_else(p):
	'''if_else : IF   condition   compoundStmt   ELSE   compoundStmt'''
	if p[2] == "True":
		p[0] = p[3]
	else:
		p[0] = p[5]

def p_if_cond(p):
	'''if : IF   condition   compoundStmt'''
	if p[2] == "True":
		p[0] = p[3]
	else:
		print("Condition failed!")
		pass

def p_expression_plus(p):
	'''expression : expression PLUS term'''
	p[0] = p[1] + p[3]
	generate_icg('+', p[1], p[3], p[0])

def p_expression_minus(p):
	'''expression : expression MINUS term'''
	p[0] = p[1] - p[3]
	generate_icg('-', p[1], p[3], p[0])

def p_term_times(p):
	'''term : term TIMES term'''
	p[0] = p[1] * p[3]
	generate_icg('*', p[1], p[3], p[0])

def p_term_div(p):
	'''term : term DIVIDE term'''
	p[0] = p[1] / p[3]
	generate_icg('/', p[1], p[3], p[0])

def p_condition_equequ(p):
	'''condition : term EQUALSEQUALS term'''
	generate_icg("if==", p[1], p[3], "goto L"+str(label_counter+1))
	if p[1] == p[3]:
		p[0] = "True"
	else:
		p[0] = "False"

def p_condition_notequ(p):
	'''condition : term NOTEQUALS term'''
	if not p[1] == p[3]:
		p[0] = "True"
	else:
		p[0] = "False"

def p_condition_gthanequ(p):
	'''condition : term GTHANEQU term'''
	if p[1] >= p[3]:
		p[0] = "True"
	else:
		p[0] = "False"

def p_condition_lthanequ(p):
	'''condition : term LTHANEQU term'''
	if p[1] <= p[3]:
		p[0] = "True"
	else:
		p[0] = "False"

def p_condition_lthan(p):
	'''condition : term GTHAN term'''
	if p[1] > p[3]:
		p[0] = "True"
	else:
		p[0] = "False"

def p_condition_gthan(p):
	'''condition : term LTHAN term'''
	if p[1] < p[3]:
		p[0] = "True"
	else:
		p[0] = "False"

def p_expression_term(p):
	'expression : term'
	p[0] = p[1]

def p_term_factor(p):
	'term : factor'
	p[0] = p[1]

def p_factor_num(p):
	'''factor : NUMBER
				| ID '''
	p[0] = p[1]

def p_factor_expr(p):
	'''factor : LPAREN expression RPAREN'''
	p[0] = p[2]


# Error rule for syntax errors
def p_error(p):
	print("Syntax error in input!")
	print(p)

def p_empty(p):
	'empty : '
	pass