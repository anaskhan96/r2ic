import ply.yacc as yacc
from lex_analysis import tokens
from optimized_tac import ThreeAddressCode
from ast import AbstractSyntaxTree

threeAddressCode = ThreeAddressCode()
abstractSyntaxTree = AbstractSyntaxTree('root', None, None)

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
	
	'''CAN ONLY BE DONE IF THE VARIABLES ARE ADDED TO SYMBOL TABLE:

					| ID EQUALS ID SEMICOLON
					| ID EQUALS ID PLUS expression SEMICOLON
					| ID EQUALS ID MINUS expression SEMICOLON'''
	#if p[4] = '+':
	#	p[0] = threeAddressCode.get_value(p[3]) + p[5]
	#elif p[4] = '-':
	#	p[0] = threeAddressCode.get_value(p[3]) + p[5]
	#elif p[4] = '+':
	#	p[0] = threeAddressCode.get_value(p[3]) + p[5]
	p[0] = p[3]
	threeAddressCode.generate_icg('=', p[3], '', p[1])

def p_Stmt(p):
	'''Stmt : print_text SEMICOLON
			| expression SEMICOLON
			| AssignExpr
			| if
			| if_else
			| loop'''
	p[0] = p[1]

def p_print(p):
	'''print_text : PRINTMAC LPAREN text RPAREN
					| PRINTLNMAC LPAREN text RPAREN'''
	p[0] = p[3][1:-1]

def p_text(p):
	'''text : STRINGZ '''
	p[0] = p[1]

def p_if_else(p):
	'''if_else : IF   condition   compoundStmt generateGoto  ELSE putLabelResult compoundStmt putLabelArg'''
	if p[2] == "True":
		p[0] = p[3]
	else:
		p[0] = p[6]

def p_if_cond(p):
	'''if : IF   condition   compoundStmt putLabelResult'''
	if p[2] == "True":
		p[0] = p[3]
	else:
		print("Condition failed!")
		pass

def p_loop(p):
	'''loop : WHILE condition compoundStmt putLabelResult
			| LOOP compoundStmt putLabelResult'''
	if p[1] == 'while':
		if p[2] == 'True':
			p[0] = p[3]
		else:
			pass
	else:
		p[0] = p[2]

def p_expression_plus(p):
	'''expression : expression PLUS term'''
	p[0] = p[1] + p[3]
	threeAddressCode.generate_icg('+', p[1], p[3], p[0])

def p_expression_minus(p):
	'''expression : expression MINUS term'''
	p[0] = p[1] - p[3]
	threeAddressCode.generate_icg('-', p[1], p[3], p[0])

def p_term_times(p):
	'''term : term TIMES factor'''
	p[0] = p[1] * p[3]
	threeAddressCode.generate_icg('*', p[1], p[3], p[0])

def p_term_div(p):
	'''term : term DIVIDE factor'''
	p[0] = p[1] / p[3]
	threeAddressCode.generate_icg('/', p[1], p[3], p[0])

def p_condition_equequ(p):
	'''condition : term EQUALSEQUALS term'''
	threeAddressCode.generate_icg("==F", p[1], p[3], "goto S")
	if p[1] == p[3]:
		p[0] = "True"
	else:
		p[0] = "False"

def p_condition_notequ(p):
	'''condition : term NOTEQUALS term'''
	threeAddressCode.generate_icg("!=F", p[1], p[3], "goto S")
	if not p[1] == p[3]:
		p[0] = "True"
	else:
		p[0] = "False"

def p_condition_gthanequ(p):
	'''condition : term GTHANEQU term'''
	threeAddressCode.generate_icg(">=F", p[1], p[3], "goto S")
	if p[1] >= p[3]:
		p[0] = "True"
	else:
		p[0] = "False"

def p_condition_lthanequ(p):
	'''condition : term LTHANEQU term'''
	threeAddressCode.generate_icg("<=F", p[1], p[3], "goto S")
	if p[1] <= p[3]:
		p[0] = "True"
	else:
		p[0] = "False"

def p_condition_lthan(p):
	'''condition : term GTHAN term'''
	threeAddressCode.generate_icg(">F", p[1], p[3], "goto S")
	if p[1] > p[3]:
		p[0] = "True"
	else:
		p[0] = "False"

def p_condition_gthan(p):
	'''condition : term LTHAN term'''
	threeAddressCode.generate_icg("<F", p[1], p[3], "goto S")
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

def p_putLabelResult(p):
	'''putLabelResult : empty'''
	threeAddressCode.putLabel('result')

def p_putLabelArg(p):
	'''putLabelArg : empty'''
	threeAddressCode.putLabel('arg1')

def p_generateGoto(p):
	'''generateGoto : empty'''
	threeAddressCode.generate_icg("goto", "S", '', '')

# Error rule for syntax errors
def p_error(p):
	print("Syntax error in input!")
	print(p)

def p_empty(p):
	'empty : '
	pass