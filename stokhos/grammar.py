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

from . import AST
from .tokenrules import tokens
from .utils.custom_exceptions import ParseError
from .utils.err_strings import *

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
    raise ParseError(error_missing_semicolon(col))

# -------- DEFINICIONES --------
# <definicion> -> <tipo> <identificador> := <expresion>
def p_definicion_var(p):
    'definicion : tipo identificador TkAssign expresion'
    p[0] = AST.SymDef(p[1], p[2], p[4])

# -------- ASIGNACIONES --------
# <asignacion>  -> <identificador> := <expresion>
def p_asignacion_var(p):
    'asignacion : identificador TkAssign expresion'
    p[0] = AST.Assign(p[1], p[3])

# <acceso_arreglo> := <expresion>
def p_asignacion_elemento_arr(p):
    'asignacion : acceso_arreglo TkAssign expresion'
    p[0] = AST.AssignArrayElement(p[1], p[3])

# ---- errores en asignaciones y definiciones ----
#def p_assign_def_err1(p):
#    '''definicion : tipo TkAssign expresion
#        | tipoArreglo TkAssign TkOpenBracket listaElems TkCloseBracket
#    asignacion : TkAssign expresion
#        | TkAssign TkOpenBracket listaElems TkCloseBracket'''
#    col = p.lexpos(2)
#    if isinstance(p[1], str) and p[1] == ':=':
#        col = p.lexpos(1) + 1
#
#    raise ParseError(error_id_expected(col))
#
#def p_assign_def_err2(p):
#    '''definicion : tipo identificador TkAssign
#    asignacion : identificador TkAssign'''
#    col = p.lexspan(2)[1] + 3
#    if len(p) == 4:
#        col = p.lexspan(3)[1] + 3
#    raise ParseError(error_expression_expected(col))
#
#def p_assign_def_err3(p):
#    'definicion : tipoArreglo identificador TkAssign listaElems'
#    col = p.lexpos(3) + 3
#    raise ParseError(error_array_constructor_expected(col))
#
#def p_arr_desbalanceado_err1(p):
#    '''definicion : tipoArreglo identificador TkAssign TkOpenBracket listaElems
#    asignacion : identificador TkAssign TkOpenBracket listaElems'''
#    col = p.lexspan(4)[1] + 2
#    if len(p) == 6:
#        col = p.lexspan(5)[1] + 2
#
#    raise ParseError(error_unclosed_array_constructor(col))
#
#def p_arr_desbalanceado_err2(p):
#    '''definicion : tipoArreglo identificador TkAssign listaElems TkCloseBracket
#    asignacion : identificador TkAssign listaElems TkCloseBracket'''
#    col = p.lexpos(2) + 3
#    if len(p) == 6:
#        col = p.lexpos(3) + 3
#
#    raise ParseError(error_unopened_array_constructor(col))
#
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
    raise ParseError(error_invalid_expression_access(p.lexpos(2)+1))

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
    raise ParseError(error_unbalance_parentheses())
    
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
#     | <funcion>
#     | <arreglo>
#     | <acceso_arreglo>
def p_expresion_comparacion(p):
    '''expresion : comparacion
        | funcion
        | arreglo
        | acceso_arreglo'''
    p[0] = p[1]

# <identificador> -> TkId
def p_identificador_tkId(p):
    'identificador : TkId'
    p[0] = AST.Id(p[1])

# <arreglo> -> [<listaElems>]
def p_arreglo(p):
    'arreglo : TkOpenBracket listaElems  TkCloseBracket'
    p[0] = AST.Array(p[2])

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

# <tipo> -> <tipo_primitivo> | <tipo_arreglo>
def p_tipo(p):
    '''tipo : tipo_primitivo
        | tipo_arreglo'''
    p[0] = AST.Type(p[1])

# <tipo_arreglo> -> [<tipo>]
def p_tipo_arreglo(p):
    'tipo_arreglo : TkOpenBracket tipo_primitivo TkCloseBracket'
    p[0] = AST.TypeArray(AST.PrimitiveType(p[2]))

# <tipo_primitivo> -> num
#     | bool
def p_tipo_primitivo(p):
    '''tipo_primitivo : TkNum
        | TkBool'''
    p[0] = AST.PrimitiveType(p[1])

# def p_easter_egg(p):
#     'tokensfaltantes : TkOpenBrace TkSemicolon TkColon TkCloseBrace'
#     # Imposible llegar a esta producción, está para esconder los warnings

# -------- PALABRA VACÍA --------
def p_lambda(p):
    'lambda :'
    pass

# -------- ERROR --------

def p_error(p):
    if p:
        if p.type == 'IllegalCharacter':
            raise ParseError(error_invalid_char(p.value, p.lexpos + 2))

        elif p.type == 'IllegalID':
            raise ParseError(error_invalid_id(p.value, p.lexpos + 1))


        raise ParseError(error_invalid_syntax_generic(p.value, p.lexpos + 1))

    else:
        raise ParseError(error_invalid_syntax_generic())