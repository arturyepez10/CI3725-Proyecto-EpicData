"""Validadores semánticos de los AST de Stókhos.

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

from re import I
from ..builtins.functions import _type
from .. import AST
from .custom_exceptions import SemanticError

# VALIDACIONES PRINCIPALES (retornan un árbol)

def validate_ast(ast: AST.AST, sym_table: dict) -> AST.AST:
    '''Valida el AST de Stókhos.

    Args:
        Un AST de Stókhos, SymDef, Assign, AssignArrayElement o una expresión.

    Retorna:
        El árbol validado, o un nodo de error.
    '''
    # Se dividen 3 casos, dependiendo de si el árbol corresponde a una
    # definición, una asignación o una expresión

    try:
        if type(ast) == AST.SymDef:
            # Caso 1: Es una definición de variable
            validate_vardef(ast, sym_table)
        elif type(ast) == AST.Assign:
            # Caso 2.1: Es una asignación
            validate_assign(ast)
        elif type(ast) == AST.AssignArrayElement:
            # Caso 2.1: Es una asignación de un acceso a arreglo
            AST.Error('TODO')
        else:
            # Caso 3: Es una expresión
            validate_expr(ast)
    except SemanticError as e:
        return AST.Error(e.message)
    
    return ast

def validate_vardef(ast: AST.SymDef, sym_table: dict) -> None:
    # Se valida que la variable no haya sido previamente definida
    if ast.id in sym_table:
        raise SemanticError(f'Variable {ast.id} ya definida')

    # Se valida el tipo del lado derecho de la asignación
    type_check(ast.type, ast.value, sym_table)

def validate_assign(ast: AST.Assign, sym_table: dict) -> None:
    # Se valida que la variable a la que se le asigna sea previamente
    # definida
    if ast.name not in sym_table:
        raise Exception(f'Variable {ast.name} no definida')
    else:
        # Se valida que la variable a la que se le asigna sea del mismo
        # tipo que la variable a la que se le asigna
        if sym_table[ast.name] != ast.type:
            raise Exception(f'Variable {ast.name} no es del mismo tipo que la variable a la que se le asigna')
        else:
            return ast

def validate_expr(ast: AST.AST, sym_table: dict) -> None:
    # Se valida que la expresión sea de tipo booleano
    if ast.type != 'bool':
        raise Exception(f'Expresión no es de tipo booleano')
    else:
        return ast

def type_check(_type: AST.Type, ast: AST.AST, sym_table: dict) -> None:
    # Se valida que el ast sea del mismo tipo que type, independientemente de
    # si sus variables existen o el ast es semánticamente correcto
    if _type != _type(ast):
        raise SemanticError(f'Tipos no compatibles')

    # Casos base: ast es un terminal
    if issubclass(type(ast), AST.Terminal):
        return

    # Si ast es un operador binario
    if issubclass(type(ast), AST.BinOp):
        type_check(_type, ast.lhs_term, sym_table)
        type_check(_type, ast.rhs_term, sym_table)
        return