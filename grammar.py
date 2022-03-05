"""Definiciones de reglas para el parser de Stókhos.

Copyright (C) 2022 Arturo Yepez - Jesus Bandez - Christopher Gómez
CI3725 - Traductores e Interpretadores

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import ply.yacc as yacc
from tokenrules import tokens
from VM import StokhosVM as SVM

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

# <instruccion> -> <definicion> 
#     | <asignacion>
def p_instruccion(p):
    '''instruccion : definicion TkSemicolon
        | asignacion TkSemicolon
        | indefinido TkSemicolon
        | expresion'''
    print('instruccion')
    p[0] = p[1]

# -------- DEFINICIONES --------

# <definicion> -> <tipo> <identificador> := <expresion>;
def p_definicion_var(p):
    'definicion : tipo TkId TkAssign expresion'
    p[0] = ('def', p[1], p[2], p[4])

# <definicion> -> [<tipo>] <identificador> := [<listaElems>];
def p_definicion_arr(p):
    'definicion : TkOpenBracket tipo TkCloseBracket TkId TkAssign TkOpenBracket listaElems TkCloseBracket'
    p[0] = ('def', p[2], p[4], p[7])

# -------- ASIGNACIONES --------

# <asignacion>  -> <identificador> := <expresion>;
def p_asignacion_var(p):
    'asignacion : TkId TkAssign expresion'
    p[0] = ('asignacion', p[1], p[3])
    print(p[0])

# <identificador>[<expresion>] := <expresion>;
def p_asignacion_elemento_arr(p):
    'asignacion : TkId TkOpenBracket expresion TkCloseBracket TkAssign expresion'
    p

# <identificador> := [<listaElems>]
def p_asignacion_arr(p):
    'asignacion : TkId TkAssign TkOpenBracket listaElems TkCloseBracket'
    p

# -------- LISTAS --------

# <listaElems> -> (lambda) 
#     | <expresion>
#     | <listaElems> , <expresion>
def p_lista(p):
    '''listaElems : lambda
        | expresion
        | listaElems TkComma expresion'''
    p

# -------- EXPRESIONES --------

# <expresion> -> (<expresion>)
#     | '<expresion>'
def p_expresion(p):
    '''expresion : TkOpenPar expresion TkClosePar
        | TkQuote expresion TkQuote'''
    p[0] = p[2]

# -------- EXPRESIONES NUMÉRICAS --------

# <expresion> -> <numero>
#     | <booleano>
#     | <identificador>
def p_expresion_terminales(p):
    '''expresion : TkNumber
        | booleano
        | TkId'''
    p[0] = p[1]

# <expresion> -> -<expresion>
#     | +<expresion>
def p_expresion_parentesis(p):
    '''expresion : TkMinus expresion %prec UNARY
        | TkPlus expresion %prec UNARY'''
    p

# <expresion> -> <expresion> + <expresion>
#     | <expresion> - <expresion>
def p_expresion_suma_resta(p):
    '''expresion : expresion TkPlus expresion
        | expresion TkMinus expresion'''
    if p[1] == '+':
        p
    else:
        p

# <expresion> -> <expresion> * <expresion>
#     | <expresion> / <expresion>
def p_expresion_mult_div(p):
    '''expresion : expresion TkMult expresion
        | expresion TkDiv expresion'''
    if p[1] == '*':
        p
    else:
        p

# <expresion> -> <expresion> * <expresion>
#     | <expresion> / <expresion>
def p_expresion_mod_exp(p):
    '''expresion : expresion TkMod expresion
        | expresion TkPower expresion'''
    if p[1] == '%':
        p
    else:
        p

# -------- EXPRESIONES BOOLEANAS --------


# <expresion> -> !<expresion>
def p_expresion_negacion(p):
    'expresion : TkNot expresion %prec UNARY'
    p

# <expresion> -> <expresion> && <expresion>
#     | <expresion> || <expresion>
def p_expresion_conj_disy(p):
    '''expresion : expresion TkAnd expresion
        | expresion TkOr expresion'''
    if p[2] == '&&':
        p
    else:
        p

# <expresion> -> <comparacion>
def p_expresion_comparacion(p):
    'expresion : comparacion'
    p

# <expresion> -> <funcion>
def p_expresion_funcion(p):
    'expresion : funcion'
    p

# -------- COMPARACIONES (BOOLEANAS) --------

# <comparacion> -> <expresion> < <expresion>
#     | <expresion> <= <expresion>
def p_comparacion_menor_que(p):
    '''comparacion : expresion TkLT expresion
        | expresion TkLE expresion'''
    if p[2] == '<':
        p
    else:
        p
    
# <comparacion> -> <expresion> > <expresion>
#     | <expresion> >= <expresion>
def p_comparacion_mayor_que(p):
    '''comparacion : expresion TkGT expresion
        | expresion TkGE expresion'''
    if p[2] == '>':
        p
    else:
        p

# <comparacion> -> <expresion> = <expresion>
#     | <expresion> <> <expresion>
def p_comparacion_igual_distinto(p):
    '''comparacion : expresion TkEq expresion
        | expresion TkNE expresion'''
    if p[2] == '==':
        p
    else:
        p

# -------- FUNCIONES --------

def p_funcion(p):
    'funcion : TkId TkOpenPar listaElems TkClosePar'
    p

# -------- TERMINALES --------

# <funcion> -> <identificador> (<listaElems>)
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
    result = parser.parse(s, lexer=vm.lex)
    print(result)