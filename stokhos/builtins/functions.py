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

from math import floor
from random import uniform
from time import time

from ..AST import *
from ..utils.custom_exceptions import SemanticError
from ..VM import StokhosVM
from ..utils.constants import *


def stk_type(ast: AST, sym_table: dict) -> Type:
    '''Retorna el tipo de una expresión.
    
    Args:
        Un árbol de  una expresión de Stókhos.
    
    Retorna:
        El tipo de la expresión.
    '''
    # Si es una constante, se obtiene su tipo.
    if type(ast) in [Number, Boolean]:
        return type(ast)
    
    # Si es una variable, se obtiene su tipo de la tabla de símbolos.
    if type(ast) == Id:
        if ast.id.value in sym_table:
            return sym_table[ast.id.value].type
        else:
            raise SemanticError('Variable no definida')
    
    # Si es una función, se obtiene su tipo de retorno de la tabla de símbolos.
    # TODO

    # Si es una expresión binaria, se obtiene el tipo de la operación.
    if type(ast) == BinOp:
        if ast.op in ['&&', '||']:
            return Boolean
        else:
            return Number
    
    return ast.type

def stk_reset(vm: StokhosVM) -> Boolean:
    '''Resetea la tabla de símbolos de la vm dada.
    
    Args:
        vm: Instancia de VM de Stókhos.
    '''
    vm.symbols.clear()
    return Boolean(True)

def stk_uniform() -> Number:
    '''Retorna un número aleatorio entre 0 y 1.
    '''
    return Number(uniform(0, 1))

def stk_floor(x: Number) -> Number:
    '''Retorna el máximo entero menor o igual a x.
    
    Args:
        x: Número a redondear.
    '''
    return floor(x)

def stk_length(a: Array) -> Number:
    '''Retorna el tamaño de una lista.
    
    Args:
        l: Lista a evaluar.
    '''
    return len(a)

def stk_sum(a: Array) -> Number:
    '''Retorna la suma de los elementos de un arreglo de Number
    
    Args:
        l: Arreglo a evaluar.
    '''
    return sum(a, Number(0))

def stk_avg(a: Array) -> Number:
    '''Retorna la media de los elementos de un arreglo de Number, o 0 si el
    arreglo está vacío.
    
    Args:
        a: Arreglo a evaluar.
    '''
    return stk_sum(a) / stk_length(a) if a else 0

def stk_pi() -> Number:
    '''Retorna el valor de pi en formato de doble precisión (IEEE754).'''
    return Number(3.141592653589793)

def stk_now() -> Number:
    '''Retorna un Number correspondiente al los milisegundos transcurridos
    desde un punto de referencia en el tiempo.
    
    La implementación interna es la de currentmillis.com sugerida para Python.
    '''
    return Number(int(round(time() * 1000)))

PRELOADED_FUNCTIONS = {
    'reset': 
        Symbol(
            Type(PrimitiveType('void')),
            FunctionSignature([], stk_reset,)
        ),
    'uniform': Symbol(
            Type(PrimitiveType('num')),
            FunctionSignature([], stk_uniform)
        ),
    'floor': Symbol(
            Type(PrimitiveType('num')),
            FunctionSignature(
                [Type(PrimitiveType('num'))],
                stk_floor
            )
        ),
    'length': Symbol(
            Type(PrimitiveType('num')),
            FunctionSignature(
                [Type(TypeArray(PrimitiveType(('num'))))],
                stk_floor,
                [[Type(TypeArray(PrimitiveType(('num'))))]]
            )
        ),
    'sum': stk_sum,
    'avg': stk_avg,
    'pi': stk_pi,
    'now': stk_now,
}