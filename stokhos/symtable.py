"""Implementación de tabla de símbolos para el intérprete de Stókhos.

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

from typing import Union

from .AST import *
from .utils.custom_exceptions import UndefinedSymbolError
from .builtins.functions import *

# --- ENTRADAS DE LA TABLA DE SIMBOLOS ---
class Symbol:
    def __init__(self, _type: Type, value: Union[AST, callable]):
        pass

class SymFunctionSignature(Symbol):
    '''Símbolo que representa una función en la tabla de símbolos.

    Atributos:
        callable: Función de Python con la implementación interna de la
            función correspondiente de Stókhos. Los tipos de los argumentos
            y del retorno son consistentes con los indicados en args y
            return_type.
        args: Lista donde cada elemento cumple una de estas dos condiciones:
            1. Es una lista con los tipos de argumentos que pide cada
                sobrecarga de la función.
            2. Una lista donde cada elemento son los tipos de argumento que
                pide la función, si esta no admite sobrecargas.
        return_type: Tipo de retorno de la función.
    '''
    def __init__(self, _callable: callable,
    _args: Union[list[list[Type]], list[Type]], return_type: Type):
        self.callable = _callable
        self.args = _args
        self.return_type = return_type

class SymVar(Symbol):
    '''Símbolo que representa una variable en la tabla de símbolos.

    Atributos:
        type: Tipo de la variable.
        value: Valor de la variable. Normalmente una subclase de Terminal
            o un AST de expresión en caso de que se guarde una expresión
            acotada.
    '''
    def __init__(self, _type: Type, value: AST):
        self.type = _type

        # Un terminal o un AST en caso de que se guarde una expresión acotada
        self.value = value

# Funciones precargadas de Stókhos

PRELOADED_FUNCTIONS = {
    'uniform': SymFunctionSignature(stk_uniform, [], NUM,),
    'floor': SymFunctionSignature(stk_floor, [NUM], NUM),
    'length': SymFunctionSignature(stk_length, [[NUM_ARRAY], [BOOL_ARRAY]], NUM),
    'sum': SymFunctionSignature(stk_sum, [NUM_ARRAY], NUM),
    'avg': SymFunctionSignature(stk_avg, [NUM_ARRAY], NUM),
    'pi': SymFunctionSignature(stk_pi, [], NUM),
    'now': SymFunctionSignature(stk_now, [], NUM),
}

# --- IMPLEMENTACIÓN DE TABLA DE SÍMBOLOS ---
class SymTable:
    def __init__(self):
        self.table = PRELOADED_FUNCTIONS

    def insert(self, id: str, s: Symbol):
        if not id in self.table:
            self.table[id] = s
            return True

        return False

    def update(self, id: str, value: AST):
        if id in self.table:
            self.table[id].value = value
        
        raise UndefinedSymbolError(id)
    
    def lookup(self, id: str):
        if id in self.table:
            return self.table[id]

        raise UndefinedSymbolError(id)

    def clear(self):
        self.table = PRELOADED_FUNCTIONS