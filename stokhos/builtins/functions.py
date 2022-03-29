"""Implementaciones de las funciones predefinidas de Stókhos.

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

from .. import AST


def _type(ast: AST.AST, sym_table: dict) -> AST.Type:
    '''Retorna el tipo de una expresión.
    
    Args:
        Un árbol de  una expresión de Stókhos.
    
    Retorna:
        El tipo de la expresión.
    '''
    # Si es una constante, se obtiene su tipo.
    if type(ast) in [AST.Number, AST.Boolean]:
        return type(ast)
    
    # Si es una variable, se obtiene su tipo de la tabla de símbolos.
    if type(ast) == AST.Id:
        return sym_table[ast.id.value]
    
    # Si es una función, se obtiene su tipo de retorno de la tabla de símbolos.
    # TODO

    # Si es una expresión binaria, se obtiene el tipo de la operación.
    if type(ast) == AST.BinOp:
        if ast.op in ['&&', '||']:
            return AST.Boolean
        else:
            return AST.Number
    
    return ast.type