import ply.lex as lex 	# Lexer
import ply.yacc as yacc	# Parser
import lex_analysis		# Lex File
import sys				# Python sys
import symbol_table		# Symbol Table File
import parse_analysis
from parse_analysis import threeAddressCode
from parse_analysis import abstractSyntaxTree
from optimized_tac import tac_stack

lexer = lex.lex(module=lex_analysis)

data = '''
// Single Comment
fn main(){
	let a = 3 + 4 * 9;
	while a < 2 {
		let a = 5 + 6;
	}
	let b = c + 4 * 5;
}
/* Multiline Comments */
/// Generate library docs for the following item.
//! Generate library docs for the enclosing item.
'''
lexer.input(data)
global_symtab = symbol_table.symbol_table("global", "global")
stack = symbol_table.table_stack()
stack.push(global_symtab)
linecount, items = 0, []

for tok in lexer:
	# print(tok)
	if(tok.lineno == linecount):
		items.append(tok.value)
	else:
		items = [tok.value]
		linecount+=1
	symtab = stack.peek()
	if(tok.value in lex_analysis.reserved):
		symtab.insert(tok.value, [tok.lineno, tok.type, "reserved", "-", "-"])

	elif(tok.type == 'ID'):
		symtab.insert(tok.value, [tok.lineno, tok.type, '~', "global", "-"])

	elif(tok.type == 'LBRACE'):
		scope_name = ''
		if 'if' in items:
			scope_name = 'if'
		elif 'else' in items:
			scope_name = 'else'
		elif 'for' in items:
			scope_name = 'for'
		elif 'while' in items:
			scope_name = 'while'
		elif 'loop' in items:
			scope_name = 'loop'
		digit = symbol_table.find_most_recent_scope(scope_name, symtab)
		scope_name = ''.join([scope_name, str(digit+1)])
		new_symtab = symbol_table.symbol_table(scope_name, symtab)
		stack.push(new_symtab)
		# print("Addded new symbol table", scope_name)

	elif(tok.type == 'RBRACE'):
		child_symtab = stack.pop()
		symtab = stack.peek()
		symtab.put_child(child_symtab.name, child_symtab)

final_sym = stack.peek()
parser = yacc.yacc(module=parse_analysis)
final_sym.print_table()
threeAddressCode.symbolTable = final_sym
parse_analysis.initSymbolTable(final_sym)
result = parser.parse(data)
print(result)
threeAddressCode.print_code()
abstractSyntaxTree.printAST()