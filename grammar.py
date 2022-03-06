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

from ctypes import Array
import ply.yacc as yacc
from tokenrules import tokens
from VM import StokhosVM as SVM
import AST

# -------- REGLAS DE PRECEDENCIA --------
precedence = (
    ('nonassoc', 'TkAssign'),
    ('left', 'TkOr'),
    ('left', 'TkAnd'),
    ('nonassoc', 'TkEq', 'TkNE'),
    ('nonassoc', 'TkLT', 'TkGT', 'TkLE', 'TkGE'),
    ('left', 'TkPlus', 'TkMinus'),
    ('left', 'TkMult', 'TkDiv', 'TkMod'),
    ('nonassoc', 'UNARY'),
    ('right', 'TkPower'),
    ('nonassoc', 'TkOpenPar', 'TkClosePar', 'TkQuote', 'TkOpenBracket', 'TkCloseBracket'),
)

# -------- INSTRUCCIONES --------
# <instruccion> -> <definicion>;
#     | <asignacion>;
#     | <expresion>
def p_instruccion(p):
    '''instruccion : definicion TkSemicolon
        | asignacion TkSemicolon
        | expresion'''
    p[0] = p[1]

# -------- DEFINICIONES --------
# <definicion> -> <tipo> <identificador> := <expresion>
def p_definicion_var(p):
    'definicion : tipo TkId TkAssign expresion'
    p[0] = AST.SymDef(p[1], p[2], p[4])

# <definicion> -> [<tipo>] <identificador> := [<listaElems>]
def p_definicion_arr(p):
    'definicion : tipoArreglo TkId TkAssign TkOpenBracket listaElems TkCloseBracket' 
    p[0] = AST.SymDef(p[1], p[2], p[5])

# -------- ASIGNACIONES --------
# <asignacion>  -> <identificador> := <expresion>
def p_asignacion_var(p):
    'asignacion : TkId TkAssign expresion'
    p[0] = AST.Assign(p[1], p[3])

# <identificador>[<expresion>] := <expresion>
def p_asignacion_elemento_arr(p):
    'asignacion : acceso_arreglo TkAssign expresion'
    p[0] = AST.AssignArrayElement(p[1], p[3])

# <identificador> := [<listaElems>]
def p_asignacion_arr(p):
    'asignacion : TkId TkAssign TkOpenBracket listaElems TkCloseBracket'
    p[0] = AST.AssignArray(p[1], p[4])

# -------- LISTAS --------
# <acceso_arreglo> -> <identificador>[<expresión>]
def p_acceso_arreglo(p):
    'acceso_arreglo : TkId TkOpenBracket expresion TkCloseBracket'
    p[0] = AST.ArrayAccess(p[1], p[3])
    

# <listaElems> -> (lambda)
#     | <expresion>
#     | <listaElems> , <expresion>
def p_lista(p):
    '''listaElems : lambda
        | expresion
        | expresion TkComma listaElems'''
    # Caso base
    if len(p) == 2:
        p[0] = AST.ElemList(p[1])
    # Caso recursivo
    else:
        p[3].append(p[1])
        p[0] = p[3]


# -------- EXPRESIONES --------
# <expresion> -> (<expresion>)
#     | '<expresion>'
def p_expresion(p):
    '''expresion : TkOpenPar expresion TkClosePar
        | TkQuote expresion TkQuote'''
    if p[1] == '(':
        p[0] = AST.Parentheses(p[2])
    else:
        p[0] = AST.Quoted(p[2])

# -------- EXPRESIONES TERMINALES --------
# <expresion> -> <numero>
#     | <booleano>
#     | <identificador>
def p_expresion_terminales(p):
    '''expresion : TkNumber
        | booleano
        | TkId'''
    if type(p[1]) in [int, float]:
        p[0] = AST.Number(p[1])
    elif type(p[1]) == AST.Boolean:
        p[0] = p[1]
    else:
        p[0] = AST.Id(p[1])

# -------- EXPRESIONES CON OPERACIONES UNARIAS --------
# <expresion> -> -<expresion>
#     | +<expresion>
#     | !<expresion>
def p_expresion_unarias(p):
    '''expresion : TkMinus expresion %prec UNARY
        | TkPlus expresion %prec UNARY
        | TkNot expresion %prec UNARY'''
    p[0] = AST.UnOp(p[1], p[2])

# -------- EXPRESIONES CON OPERACIONES BINARIAS --------
# <expresion> -> <expresion> + <expresion>
#     | <expresion> - <expresion>
#     | <expresion> * <expresion>
#     | <expresion> / <expresion>
#     | <expresion> % <expresion>
#     | <expresion> ^ <expresion>
#     | <expresion> && <expresion>
#     | <expresion> || <expresion>
def p_expresion_binarias(p):
    '''expresion : expresion TkPlus expresion
        | expresion TkMinus expresion
        | expresion TkMult expresion
        | expresion TkDiv expresion
        | expresion TkMod expresion
        | expresion TkPower expresion
        | expresion TkAnd expresion
        | expresion TkOr expresion'''
    p[0] = AST.BinOp(p[2], p[1], p[3])

# -------- OTRAS EXPRESIONES --------
# <expresion> -> <comparacion>
def p_expresion_comparacion(p):
    'expresion : comparacion'
    p[0] = p[1]

# <expresion> -> <funcion>
def p_expresion_funcion(p):
    'expresion : funcion'
    p[0] = p[1]

# <expresion> -> <acceso_arreglo>
def p_expresion_acceso_arreglo(p):
    'expresion : acceso_arreglo'
    p[0] = p[1]

# -------- COMPARACIONES --------
# <comparacion> -> <expresion> < <expresion>
#     | <expresion> <= <expresion>
#     | <expresion> > <expresion>
#     | <expresion> >= <expresion>
#     | <expresion> = <expresion>
#     | <expresion> <> <expresion>
def p_comparacion_menor_que(p):
    '''comparacion : expresion TkLT expresion
        | expresion TkLE expresion
        | expresion TkGT expresion
        | expresion TkGE expresion
        | expresion TkEq expresion
        | expresion TkNE expresion'''
    p[0] = AST.Comparison(p[2], p[1], p[3])

# -------- FUNCIONES --------
def p_funcion(p):
    'funcion : TkId TkOpenPar listaElems TkClosePar'
    p[0] = AST.Function(p[1], p[3])

# -------- TERMINALES --------
# <booleano> -> true
#     | false
def p_booleano(p):
    '''booleano : TkTrue
        | TkFalse'''
    p[0] = AST.Boolean(p[1])

# <tipoArreglo> -> [<tipo>]
def p_tipo_arreglo(p):
    'tipoArreglo : TkOpenBracket tipo TkCloseBracket'
    p[0] = AST.Type(AST.Array(p[2]))

# <tipo> -> num
#     | bool
def p_tipo(p):
    '''tipo : TkNum
        | TkBool'''
    p[0] = AST.Type(p[1])

# -------- PALABRA VACÍA --------
def p_lambda(p):
    'lambda :'
    pass

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