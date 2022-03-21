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

import AST
from tokenrules import tokens
from utils.custom_exceptions import ParseError

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

# ---- errores en instrucciones ----
def p_instruccion_errores(p):
    '''instruccion : definicion 
        | asignacion'''
    col = p.lexspan(1)[1] + 2
    raise ParseError(f'Punto y coma faltante al final (columna {col})')

# -------- DEFINICIONES --------
# <definicion> -> <tipo> <identificador> := <expresion>
def p_definicion_var(p):
    'definicion : tipo identificador TkAssign expresion'
    p[0] = AST.SymDef(p[1], p[2], p[4])

# <definicion> -> [<tipo>] <identificador> := [<listaElems>]
def p_definicion_arr(p):
    'definicion : tipoArreglo identificador TkAssign TkOpenBracket listaElems TkCloseBracket' 
    p[0] = AST.SymDef(p[1], p[2], p[5])

# -------- ASIGNACIONES --------
# <asignacion>  -> <identificador> := <expresion>
def p_asignacion_var(p):
    'asignacion : identificador TkAssign expresion'
    p[0] = AST.Assign(p[1], p[3])

# <identificador>[<expresion>] := <expresion>
def p_asignacion_elemento_arr(p):
    'asignacion : acceso_arreglo TkAssign expresion'
    p[0] = AST.AssignArrayElement(p[1], p[3])

# <identificador> := [<listaElems>]
def p_asignacion_arr(p):
    'asignacion : identificador TkAssign TkOpenBracket listaElems TkCloseBracket'
    p[0] = AST.AssignArray(p[1], p[4])

# ---- errores en asignaciones y definiciones ----
def p_assign_def_err1(p):
    '''definicion : tipo TkAssign expresion
        | tipoArreglo TkAssign TkOpenBracket listaElems TkCloseBracket
    asignacion : TkAssign expresion
        | TkAssign TkOpenBracket listaElems TkCloseBracket'''
    col = p.lexpos(2)
    if isinstance(p[1], str) and p[1] == ':=':
        col = p.lexpos(1) + 1

    raise ParseError(f'Se esperaba un identificador (columna {col})')

def p_assign_def_err2(p):
    '''definicion : tipo identificador TkAssign
    asignacion : identificador TkAssign'''
    col = p.lexspan(2)[1] + 3
    if len(p) == 4:
        col = p.lexspan(3)[1] + 3
    raise ParseError(f'Se esperaba una expresión (columna {col})')

def p_assign_def_err3(p):
    'definicion : tipoArreglo identificador TkAssign listaElems'
    raise ParseError('Constructor de arreglo faltante del lado derecho de '
     f'la asignación (columna {p.lexpos(3) + 2})')

def p_arr_desbalanceado_err1(p):
    '''definicion : tipoArreglo identificador TkAssign TkOpenBracket listaElems
    asignacion : identificador TkAssign TkOpenBracket listaElems'''
    col = p.lexspan(4)[1] + 1
    if len(p) == 6:
        col = p.lexspan(5)[1] + 1

    raise ParseError('Constructor de arreglo sin cerrar (corchetes '
        f'desbalanceados) (columna {col})')

def p_arr_desbalanceado_err2(p):
    '''definicion : tipoArreglo identificador TkAssign listaElems TkCloseBracket
    asignacion : identificador TkAssign listaElems TkCloseBracket'''
    col = p.lexpos(2) + 2
    if len(p) == 6:
        col = p.lexpos(3) + 2

    raise ParseError('Constructor de arreglo sin abrir (corchetes '
        f'desbalanceados) (columna {col})')

# -------- LISTAS --------
# <acceso_arreglo> -> <identificador>[<expresión>]
def p_acceso_arreglo(p):
    '''acceso_arreglo : identificador TkOpenBracket expresion TkCloseBracket
        | funcion TkOpenBracket expresion TkCloseBracket'''
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

# ---- errores de arreglos ----
def p_acceso_arreglo_err(p):
    'acceso_arreglo : expresion TkOpenBracket expresion TkCloseBracket'
    raise ParseError(f'Acceso inválido a expresión (columna {p.lexpos(2)})')

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

# No se pueden reportar errores de aquí en adelante de la manera anterior

def p_expresion_err1(p):
    '''expresion : TkOpenPar error
        | TkQuote error '''
    raise ParseError('Paréntesis desbalanceados')
    
# -------- EXPRESIONES TERMINALES --------
# <expresion> -> <numero>
#     | <booleano>
#     | <identificador>
def p_expresion_terminales(p):
    '''expresion : TkNumber
        | booleano
        | identificador'''
    if type(p[1]) in [int, float]:
        p[0] = AST.Number(p[1])
    elif type(p[1]) == AST.Boolean:
        p[0] = p[1]
    else:
        p[0] = p[1]

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
        | expresion TkOr expresion
        '''    
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

# <identificador> -> TkId
def p_identificador_tkId(p):
    'identificador : TkId'
    p[0] = AST.Id(p[1])

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
    'funcion : identificador TkOpenPar listaElems TkClosePar'
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
    p[0] = AST.Type(AST.TypeArray(p[2]))

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
    if p:
        if p.type == 'IllegalCharacter':
            raise ParseError(f'Caracter inválido ("{p.value}") (columna {p.lexpos + 1})')
        elif p.type == 'IllegalID':
            raise ParseError(f'ID ilegal ("{p.value}") (columna {p.lexpos + 1})')

        raise ParseError(f'Sintaxis inválida en {p.value} (columna {p.lexpos + 1})')
    else:
        raise ParseError(f'Sintaxis inválida al final de la línea')