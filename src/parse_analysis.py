import ply.yacc as yacc
from lex_analysis import tokens

def p_program(p):
	'''program : FN MAIN LPAREN RPAREN compoundStmt'''
	p[0] = p[5]

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
	'''print_text : PRINTMAC LPAREN text RPAREN'''
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

def p_expression_minus(p):
	'''expression : expression MINUS term'''
	p[0] = p[1] - p[3]

def p_term_times(p):
	'''expression : expression TIMES term'''
	p[0] = p[1] * p[3]

def p_term_div(p):
	'''expression : expression DIVIDE term'''
	p[0] = p[1] / p[3]

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
	'''factor : LPAREN expression RPAREN'''
	p[0] = p[2]


# Error rule for syntax errors
def p_error(p):
	print("Syntax error in input!")

def p_empty(p):
	'empty : '
	pass