import ply.lex as lex
import lex_analysis
import sys
lexer = lex.lex(module=lex_analysis)

data = '''
if n%2 == 0 {
	println!(even)
} else {
	println!(odd)
}
'''

lexer.input(data)

for tok in lexer:
	print(tok)