import ply.yacc as yacc
from lex_analysis import tokens

def p_program(p):
	'''program : FN SPACE MAIN LPAREN RPAREN compoundStmt'''
	p[0] = p[6]

def p_compoundStmt_Stmt(p):
	'''compoundStmt : LBRACE Stmt RBRACE'''
	if p[1] == ' ':
		p[0] = p[3]
	else:
		p[0] = p[2]

def p_Stmt(p):
	'Stmt : 	expression'
	p[0] = p[1]

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
				p[0] = p[2] + p[6]
			else:
				p[0] = p[2] + p[5]

		if p[3] == '+':
			if p[4] == ' ':
				p[0] = p[2] + p[5]
			else:
				p[0] = p[2] + p[4]

	else:
		if p[2] == ' ':
			if p[4] == ' ':
				p[0] = p[1] + p[5]
			else:
				p[0] = p[1] + p[4]

		if p[2] == '+':
			if p[3] == ' ':
				p[0] = p[1] + p[4]
			else:
				p[0] = p[1] + p[3]

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
				p[0] = p[2] - p[6]
			else:
				p[0] = p[2] - p[5]

		if p[3] == '-':
			if p[4] == ' ':
				p[0] = p[2] - p[5]
			else:
				p[0] = p[2] - p[4]

	else:
		if p[2] == ' ':
			if p[4] == ' ':
				p[0] = p[1] - p[5]
			else:
				p[0] = p[1] - p[4]

		if p[2] == '-':
			if p[3] == ' ':
				p[0] = p[1] - p[4]
			else:
				p[0] = p[1] - p[3]

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
				p[0] = p[2] * p[6]
			else:
				p[0] = p[2] * p[5]

		if p[3] == '*':
			if p[4] == ' ':
				p[0] = p[2] * p[5]
			else:
				p[0] = p[2] * p[4]

	else:
		if p[2] == ' ':
			if p[4] == ' ':
				p[0] = p[1] * p[5]
			else:
				p[0] = p[1] * p[4]

		if p[2] == '*':
			if p[3] == ' ':
				p[0] = p[1] * p[4]
			else:
				p[0] = p[1] * p[3]

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
				p[0] = p[2] / p[6]
			else:
				p[0] = p[2] / p[5]

		if p[3] == '/':
			if p[4] == ' ':
				p[0] = p[2] / p[5]
			else:
				p[0] = p[2] / p[4]

	else:
		if p[2] == ' ':
			if p[4] == ' ':
				p[0] = p[1] / p[5]
			else:
				p[0] = p[1] / p[4]

		if p[2] == '/':
			if p[3] == ' ':
				p[0] = p[1] / p[4]
			else:
				p[0] = p[1] / p[3]

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