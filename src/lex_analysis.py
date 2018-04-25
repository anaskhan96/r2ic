import ply.lex as lex

reserved_words = ['if', 'else', 'while', 'for', 'loop', 'break','in', 'continue', 'let', 'fn', 'false', 'true', 'match', 'return', 'self', 'main']
reserved = {word: word.upper() for word in reserved_words}

tokens = ['PRINTLNMAC',  'PRINTMAC', 'NOT', 'ID', 'MOD', 'STRINGZ', 'DECIMAL', 'NUMBER', 'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'NOTEQUALS', 'EQUALSEQUALS', 'GTHAN', 'LTHAN', 'GTHANEQU', 'LTHANEQU','LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACK', 'RBRACK', 'COMMENT', 'SPACE', 'TAB', 'SEMICOLON', 'COMMA', 'ELLIPSIS'] + list(reserved.values())

t_PRINTLNMAC = r'println\!'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'\%'
t_NOT = r'!'
t_NOTEQUALS = r'!='
t_EQUALSEQUALS = r'=='
t_GTHANEQU = r'>='
t_LTHANEQU = r'<='
t_GTHAN = r'>'
t_LTHAN = r'<'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_ELLIPSIS = r'\.\.'

# Ignoring spaces and tabs
t_TAB = r'\t'

def t_DECIMAL(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t
	
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_STRINGZ(t):
	r'["].*?["]'
	return t

def t_PRINTMAC(t):
	r'print\!|println\!'
	return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_SPACE(t):
	r'[\s]+'
	pass

# Ignoring the comments and self generating docs; capturing anyway for future purposes
def t_COMMENT(t):
	r'(\/\/\/.*)|(\/\/\!.*)|(\/\/.*)|(\/\*[.\n]*.*\*\/)'
	pass

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
