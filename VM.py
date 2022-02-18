""" Maquina Virtual para la interpretacion de Stókhos
Autores: Arturo Yepez
         Jesus Bandez
"""
from distutils.log import error
from ply.lex import lex, LexToken

# Palabras reservadas del lenguaje
reserved = {
    'bool' : 'TkBool',
    'true' : 'TkTrue',
    'false' : 'TkFalse',
    'num' : 'TkNum'    
    }

# Definicion de los tokens.
tokens = [ 'TkOpenPar', 'TkClosePar','TkOpenBracket','TkCloseBracket', 'TkOpenBrace', 'TkCloseBrace', 
           'TkNot', 'TkPower', 'TkMult', 'TkDiv', 'TkMod', 'TkPlus', 'TkMinus','TkLT', 'TkLE', 'TkGE', 'TkGT',
           'TkEq', 'TkNE', 'TkAnd', 'TkOr', 'TkQuote', 'TkComma', 'TkAssign', 'TkSemicolon', 'TkColon',           
           'TkId', 'TkNumber'] + list(reserved.values())

# Se debe ignorar todo tipo de espacio en blanco
t_ignore = ' \t'

# Asignar la expresiones regulares para obtener cada token.
# Operadores y simbolos de agrupacion
t_TkOpenPar = r'\('
t_TkClosePar = r'\)'
t_TkOpenBracket = r'\['
t_TkCloseBracket = r'\]'
t_TkOpenBrace = r'\{'
t_TkCloseBrace = r'\}'
t_TkNot = r'!'
t_TkPower = r'\^'
t_TkMult = r'\*'
t_TkDiv = r'/'
t_TkMod = r'%'
t_TkPlus = r'\+'
t_TkMinus = r'-'
t_TkLT = r'<'
t_TkLE = r'<='
t_TkGE = r'>='
t_TkGT = r'>'
t_TkEq = r'='
t_TkNE = r'<>'
t_TkAnd = r'&&'
t_TkOr = r'\|\|'
t_TkQuote = r'\''
t_TkComma = r','
t_TkAssign = r':='
t_TkSemicolon = r';'
t_TkColon = r':'



t_TkNumber = r'\d+' # Deben arreglarse los numeros para que soporte los decimales



# Regex para los nombres de las variables y palabras reservadas
def t_TkId(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'

    # En caso de que se haya conseguido una palabra reservada del lenguaje,
    # se le asigna su respectivo tipo al token. En cualquier otro caso, el
    # el tipo del token es 'TkId'
    t.type = reserved.get(t.value,'TkId')    # Check for reserved words
    return t

# Lista para los tokens que contienen caracteres ilegales
errorTokens = []
# En caso de conseguirse un caracter ilegal
def t_error(t):
    # Se crea una nueva instancia de la clase token y se llenan sus atributos con la 
    # informacion del caracter ilegal.
    tok = LexToken()
    tok.type = 'IllegalCharacter'
    tok.value = t.value[0]
    tok.lineno = t.lineno
    tok.lexpos = t.lexpos

    # Se agrega el token creado a la lista de errores
    errorTokens.append(tok)
    # Se salta el caracter ilegal
    t.lexer.skip(1)



def process(comando:str):
    """Procesa una comando para reconocerlo (fase 2), transformarlo en un arbol abstracto (fase 3) para evaluar
    expresiones y ejecuta acciones en el conetexto de las variables existentes en memoria"""

    # Por ahora solo debe imprimir un error xd
    print('ERROR: interpretacion no implementada')

def lextest(comando:str):
    """Funcion que llama a la funcion interna para reconocer tokens y construye una secuencia de tokens.
    Ver enunciado para el formato pedido (fase 1, pag 5)"""

    # Se vacia lista de los tokens de error
    errorTokens.clear()

    # Inicializar el objeto lexer y analizar el comando
    lexer = lex()
    lexer.input(comando)
    # Se crea una lista vacia que recolecta todos los tokens conseguidos en el comando    
    out = []
    for tok in lexer:
        out.append(tok)
    
    # Los tokens conseguidos en el comando se concatenan con la lista de los tokens de error
    errorTokens.extend(out)

    # La lista "errorTokens" no necesariamente sera siempre vacia. Esta se llena
    # de tokens de error en caso de haberlos al momento de ejecutar el metodo:
    # "lexer.input(comando)". Luego, se le agregan los otros tokens conseguidos. 
    # Por tanto, se retorna una lista que contiene todos los tokens conseguidos con
    # los tokens de caracteres ilegales estando de primero

    return errorTokens

    





