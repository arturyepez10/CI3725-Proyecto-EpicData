import ply.yacc as yacc
from tokenrules import tokens
from StokhosVM import StokhosVM as SVM

# -------- REGLAS DE PRECEDENCIA --------
precedence = (
    ('nonassoc', 'TkAssign'),
    ('left', 'TkOr'),
    ('left', 'TkAnd'),
    ('nonassoc', 'TkEq', 'TkNE'),
    ('nonassoc', 'TkLT', 'TkGT', 'TkLE', 'TkGE'),
    ('left', 'TkPlus', 'TkMinus'),
    ('left', 'TkMult', 'TkDiv', 'TkMod'),
    ('left', 'UNARY'),
    ('right', 'TkPower'),
    ('nonassoc', 'TkOpenPar', 'TkClosePar', 'TkQuote', 'TkOpenBracket', 'TkCloseBracket'),
)

# -------- INSTRUCCIONES --------

# <instrucción> -> <definición> 
#     | <asignación>
def p_instruccion(p):
    '''instruccion : definicion TkSemicolon
        | asignacion TkSemicolon
        | indefinido TkSemicolon'''
    print('instrucción')
    p[0] = p[1]

# -------- DEFINICIONES --------

# <definición> -> <tipo> <identificador> := <expresión>;
def p_definicion_var(p):
    'definicion : tipo TkId TkAssign expresion'
    p[0] = ('def', p[1], p[2], p[4])

# <definición> -> [<tipo>] <identificador> := [<listaElems>];
def p_definicion_arr(p):
    'definicion : TkOpenBracket tipo TkCloseBracket TkId TkAssign TkOpenBracket listaElems TkCloseBracket'
    p[0] = ('def', p[2], p[4], p[7])

# -------- ASIGNACIONES --------

# <asignación>  -> <identificador> := <expresión>;
def p_asignacion_var(p):
    'asignacion : TkId TkAssign expresion'
    p  

# <identificador>[<numExpr>] := <expresión>;
def p_asignacion_arr(p):
    'asignacion : TkId TkOpenBracket numExpr TkCloseBracket TkAssign expresion'
    p

# -------- LISTAS --------

# <listaElems> -> (lambda) 
#     | <expresión>
#     | <listaElems> , <expresión>
def p_lista(p):
    '''listaElems : lambda
        | expresion
        | listaElems TkComma expresion'''
    p

# -------- EXPRESIONES --------

# <expresión> -> (<expresión>)
#     | '<expresión>'
#     | <numExpr>
#     | <boolExpr>
def p_expresion(p):
    '''expresion : TkOpenPar expresion TkClosePar
        | TkQuote expresion TkQuote
        | numExpr
        | boolExpr'''
    p

# -------- EXPRESIONES NUMÉRICAS --------

# <numExpr> -> <número>
#     | <identificador>
def p_numExpr_terminales(p):
    '''numExpr : TkNumber
        | TkId'''
    p

# <numExpr> -> -<numExpr>
#     | +<numExpr>
def p_numExpr_parentesis(p):
    '''numExpr : TkMinus numExpr %prec UNARY
        | TkPlus numExpr %prec UNARY'''
    p

# <numExpr> -> <numExpr> + <numExpr>
#     | <numExpr> - <numExpr>
def p_numExpr_suma_resta(p):
    '''numExpr : numExpr TkPlus numExpr
        | numExpr TkMinus numExpr'''
    if p[1] == '+':
        p
    else:
        p

# <numExpr> -> <numExpr> * <numExpr>
#     | <numExpr> / <numExpr>
def p_numExpr_mult_div(p):
    '''numExpr : numExpr TkMult numExpr
        | numExpr TkDiv numExpr'''
    if p[1] == '*':
        p
    else:
        p

# <numExpr> -> <numExpr> * <numExpr>
#     | <numExpr> / <numExpr>
def p_numExpr_mod_exp(p):
    '''numExpr : numExpr TkMod numExpr
        | numExpr TkPower numExpr'''
    if p[1] == '%':
        p
    else:
        p

# <numExpr> -> funcion
def p_numExpr_funcion(p):
    'numExpr : funcion'
    p

# -------- EXPRESIONES BOOLEANAS --------

# <boolExpr> -> <booleano>
#     | <identificador>
def p_boolExpr_terminales(p):
    '''boolExpr : booleano
        | TkId'''
    p

# <boolExpr> -> <comparación>
def p_boolExpr_comparacion(p):
    'boolExpr : comparacion'
    p

# <boolExpr> -> (<boolExpr>)
def p_boolExpr_parentesis(p):
    'boolExpr : TkOpenPar boolExpr TkClosePar'
    p

# <boolExpr> -> !<boolExpr>
def p_boolExpr_negacion(p):
    'boolExpr : TkNot boolExpr %prec UNARY'
    p

# <boolExpr> -> <boolExpr> && <boolExpr>
#     | <boolExpr> || <boolExpr>
def p_boolExpr_conj_disy(p):
    '''boolExpr : boolExpr TkAnd boolExpr
        | boolExpr TkOr boolExpr'''
    if p[2] == '&&':
        p
    else:
        p

# <boolExpr> -> <función>
def p_boolExpr_funcion(p):
    'boolExpr : funcion'
    p

# -------- COMPARACIONES (BOOLEANAS) --------

# <comparación> -> <numExpr> < <numExpr>
#     | <numExpr> <= <numExpr>
def p_comparacion_menor_que(p):
    '''comparacion : numExpr TkLT numExpr
        | numExpr TkLE numExpr'''
    if p[2] == '<':
        p
    else:
        p
    
# <comparación> -> <numExpr> > <numExpr>
#     | <numExpr> >= <numExpr>
def p_comparacion_mayor_que(p):
    '''comparacion : numExpr TkGT numExpr
        | numExpr TkGE numExpr'''
    if p[2] == '>':
        p
    else:
        p

# <comparación> -> <expresión> = <expresión>
#     | <expresión> <> <expresión>
def p_comparacion_igual_distinto(p):
    '''comparacion : numExpr TkEq numExpr
        | numExpr TkNE numExpr'''
    if p[2] == '==':
        p
    else:
        p

# -------- FUNCIONES --------

def p_funcion(p):
    'funcion : TkId TkOpenPar listaElems TkClosePar'
    p

# -------- TERMINALES --------

# <función> -> <identificador> (<listaElems>)
def p_booleano(p):
    '''booleano : TkTrue
        | TkFalse'''
    p

# <tipo> -> num
#     | bool
def p_tipo(p):
    '''tipo : TkNum
        | TkBool'''
    p[0] = p[1]

# -------- PALABRA VACÍA --------

def p_lambda(p):
    'lambda :'
    p

# -------- ???????? --------

def p_indefinido(p):
    '''indefinido : TkOpenBrace listaElems TkCloseBrace
        | TkNumber TkColon TkNumber'''
    p

# -------- ERROR --------

def p_error(p):
    print("Syntax error in input!")
    print(p)

vm = SVM()

# Build the parser
parser = yacc.yacc(debug=True)

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)