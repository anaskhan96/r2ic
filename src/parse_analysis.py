import ply.yacc as yacc
from lex_analysis import tokens

def p_program(p):
	'''program : FN SPACE MAIN LPAREN RPAREN SPACE compoundStmt'''
	p[0] = p[7]

def p_compoundStmt_Stmt(p):
	'''compoundStmt : LBRACE Stmt RBRACE'''
	if p[1] == '{':
		p[0] = p[2]
	elif p[1] == 'if':
		p[0] = p[1]

def p_Stmt(p):
	'''Stmt : print_text
			| expression
			| if
			| if_else '''
	p[0] = p[1]

def p_print(p):
	'''print_text : PRINTMAC LPAREN text RPAREN
					| SPACE PRINTMAC LPAREN text RPAREN SPACE'''
	if p[1] == ' ':
		p[0] = p[4][1:-1]
	else:
		p[0] = p[3][1:-1]

def p_text(p):
	'''text : STRINGZ '''
	p[0] = p[1]

def p_if_else(p):
	'''if_else : IF SPACE condition SPACE compoundStmt SPACE ELSE SPACE compoundStmt'''
	if p[3] == "True":
		p[0] = p[5]
	else:
		p[0] = p[9]

def p_if_cond(p):
	'''if : IF SPACE condition SPACE compoundStmt
			| IF SPACE condition SPACE Stmt'''
	if p[3] == "True":
		p[0] = p[5]
	else:
		print("Condition failed!")
		pass

def p_expression_plus(p):
	'''expression : expression PLUS term
					| expression PLUS SPACE term
					| expression SPACE PLUS term
					| expression SPACE PLUS SPACE term
					| SPACE expression PLUS term
					| SPACE expression PLUS SPACE term
					| SPACE expression SPACE PLUS term
					| SPACE expression SPACE PLUS SPACE term'''
	if p[1] == ' ':
		if p[3] == ' ':
			if p[5] == ' ':
				operand1 = p[2]
				operand2 = p[6]
			else:
				operand1 = p[2]
				operand2 = p[5]

		if p[3] == '+':
			if p[4] == ' ':
				operand1 = p[2]
				operand2 = p[5]
			else:
				operand1 = p[2]
				operand2 = p[4]

	else:
		if p[2] == ' ':
			if p[4] == ' ':
				operand1 = p[1]
				operand2 = p[5]
			else:
				operand1 = p[1]
				operand2 = p[4]

		if p[2] == '+':
			if p[3] == ' ':
				operand1 = p[1]
				operand2 = p[4]
			else:
				operand1 = p[1]
				operand2 = p[3]
	p[0] = operand1 + operand2

def p_expression_minus(p):
	'''expression : expression MINUS term
					| expression MINUS SPACE term
					| expression SPACE MINUS term
					| expression SPACE MINUS  SPACE term
					| SPACE expression MINUS  term
					| SPACE expression MINUS  SPACE term
					| SPACE expression SPACE MINUS  term
					| SPACE expression SPACE MINUS SPACE term'''
	if p[1] == ' ':
		if p[3] == ' ':
			if p[5] == ' ':
				operand1 = p[2]
				operand2 = p[6]
			else:
				operand1 = p[2]
				operand2 = p[5]

		if p[3] == '-':
			if p[4] == ' ':
				operand1 = p[2]
				operand2 = p[5]
			else:
				operand1 = p[2]
				operand2 = p[4]

	else:
		if p[2] == ' ':
			if p[4] == ' ':
				operand1 = p[1]
				operand2 = p[5]
			else:
				operand1 = p[1]
				operand2 = p[4]

		if p[2] == '-':
			if p[3] == ' ':
				operand1 = p[1]
				operand2 = p[4]
			else:
				operand1 = p[1]
				operand2 = p[3]
	p[0] = operand1 - operand2

def p_term_times(p):
	'''expression : expression TIMES term
					| expression TIMES SPACE term
					| expression SPACE TIMES term
					| expression SPACE TIMES  SPACE term
					| SPACE expression TIMES  term
					| SPACE expression TIMES  SPACE term
					| SPACE expression SPACE TIMES  term
					| SPACE expression SPACE TIMES SPACE term'''
	if p[1] == ' ':
		if p[3] == ' ':
			if p[5] == ' ':
				operand1 = p[2]
				operand2 = p[6]
			else:
				operand1 = p[2]
				operand2 = p[5]

		if p[3] == '*':
			if p[4] == ' ':
				operand1 = p[2]
				operand2 = p[5]
			else:
				operand1 = p[2]
				operand2 = p[4]

	else:
		if p[2] == ' ':
			if p[4] == ' ':
				operand1 = p[1]
				operand2 = p[5]
			else:
				operand1 = p[1]
				operand2 = p[4]

		if p[2] == '*':
			if p[3] == ' ':
				operand1 = p[1]
				operand2 = p[4]
			else:
				operand1 = p[1]
				operand2 = p[3]
	p[0] = operand1 * operand2

def p_term_div(p):
	'''expression : expression DIVIDE term
					| expression DIVIDE SPACE term
					| expression SPACE DIVIDE term
					| expression SPACE DIVIDE  SPACE term
					| SPACE expression DIVIDE  term
					| SPACE expression DIVIDE  SPACE term
					| SPACE expression SPACE DIVIDE  term
					| SPACE expression SPACE DIVIDE SPACE term'''
	if p[1] == ' ':
		if p[3] == ' ':
			if p[5] == ' ':
				operand1 = p[2]
				operand2 = p[6]
			else:
				operand1 = p[2]
				operand2 = p[5]

		if p[3] == '/':
			if p[4] == ' ':
				operand1 = p[2]
				operand2 = p[5]
			else:
				operand1 = p[2]
				operand2 = p[4]
	else:
		if p[2] == ' ':
			if p[4] == ' ':
				operand1 = p[1]
				operand2 = p[5]
			else:
				operand1 = p[1]
				operand2 = p[4]

		if p[2] == '/':
			if p[3] == ' ':
				operand1 = p[1]
				operand2 = p[4]
			else:
				operand1 = p[1]
				operand2 = p[3]
	p[0] = operand1 / operand2

def p_condition_equequ(p):
	'''condition : term EQUALSEQUALS term'''
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
	'''factor : NUMBER'''
	p[0] = p[1]

def p_factor_expr(p):
	'''factor : LPAREN expression RPAREN
				| LPAREN SPACE expression SPACE RPAREN 
				| LPAREN SPACE expression RPAREN
				| LPAREN expression SPACE RPAREN'''
	p[0] = p[2]


# Error rule for syntax errors
def p_error(p):
	print("Syntax error in input!")

def p_empty(p):
	'empty : '
	pass