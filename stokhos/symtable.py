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
from .builtins.functions import *
from .utils.custom_exceptions import UndefinedSymbolError


# --- ENTRADAS DE LA TABLA DE SIMBOLOS ---
class Symbol:
    pass

class SymFunction(Symbol):
    '''Símbolo que representa una función en la tabla de símbolos.

    Atributos:
        callable: Función de Python con la implementación interna de la
            función correspondiente de Stókhos. Los tipos de los argumentos
            y del retorno son consistentes con los indicados en args y
            type.
        args: Lista donde cada elemento son los tipos de argumento que
            pide la función en orden.
        type: Tipo de retorno de la función.
    '''
    def __init__(self, _callable: callable,
    _args: list[Type], _type: Type):
        self.callable = _callable
        self.args = _args
        self.type = _type

    def __str__(self) -> str:
        return (f'{self.callable.__name__}({self.args}) '
            f'-> {self.type}')

    def __repr__(self) -> str:
        return self.__str__()

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
    
    def __str__(self):
        return f'({self.type} <--> {self.value})'

    def __repr__(self) -> str:
        return self.__str__()

# Funciones precargadas de Stókhos
PRELOADED_FUNCTIONS = {
    'type': SymFunction(None, [VOID], Type('type')),
    'ltype': SymFunction(None, [VOID], Type('type')),
    'if': SymFunction(None, [], None),
    'reset': SymFunction(None, [], BOOL),
    'uniform': SymFunction(stk_uniform, [], NUM,),
    'floor': SymFunction(stk_floor, [NUM], NUM),
    'length': SymFunction(stk_length, [ANY_ARRAY], NUM),
    'sum': SymFunction(stk_sum, [NUM_ARRAY], NUM),
    'avg': SymFunction(stk_avg, [NUM_ARRAY], NUM),
    'pi': SymFunction(stk_pi, [], NUM),
    'now': SymFunction(stk_now, [], NUM),
}

# --- IMPLEMENTACIÓN DE TABLA DE SÍMBOLOS ---
class SymTable:
    '''Clase que implementa la tabla de símbolos del intérprete de Stókhos.
    
    Incluye las funciones precargadas con su firma.
    
    Soporta las operaciones de búsqueda, existencia, inserción de variables
    y limpieza de variables definidas.

    Args:
        preloaded: Booleano que indica si se incluirán las funciones
            precargadas del intérprete. True por defecto.
    '''
    def __init__(self, preloaded: Boolean = True):
        self.preloaded = preloaded
        if self.preloaded:
            self.table = PRELOADED_FUNCTIONS.copy()
        else:
            self.table = {}

    def exists(self, _id: str) -> bool:
        '''Retorna un booleano indicando si existe en la tabla de símbolos un
        símbolo definido con la id especificada.
        '''
        return _id in self.table

    def insert(self, _id: str, _type: Type, value: AST) -> bool:
        '''Inserta una variable en la tabla de símbolos, dado el nombre, su
        tipo y su valor.
        
        Retorna un booleano indicando si la inserción resultó exitosa. De lo
        contrario, retorna False.
        '''
        if not self.exists(_id):
            self.table[_id] = SymVar(_type, value)
            return True

        return False

    def update(self, _id: str, value: AST) -> bool:
        '''Reemplaza el valor de una variable en la tabla de símbolos por el
        indicado, dado su identificador.
        
        Retorna un booleano indicando si la actualización resultó exitosa. De
        lo contrario, retorna False.
        '''
        if self.exists(_id):
            self.table[_id].value = value
            return True

        return False
    
    def lookup(self, _id: str) -> Symbol:
        '''Retorna el contenido del símbolo con la id especificada en la tabla
        símbolos.

        En caso de no existir, lanza una excepción UndefinedSymbolError.
        '''
        if self.exists(_id):
            return self.table[_id]

        raise UndefinedSymbolError(_id)

    def get_type(self, _id: str) -> Type:
        '''Obtiene el tipo del símbolo con la id especificada.
        
        Retorna:
            - El tipo de la variable, si el símbolo era una variable.
            - El tipo de retorno de la función, si el símbolo era una función.
        '''
        s = self.lookup(_id)
        return s.type
    
    def get_value(self, _id: str) -> Type:
        '''Obtiene el valor del símbolo con la id especificada.
        
        Retorna:
            - El valor de la variable, si el símbolo era una variable.
            - El callable de la implementación interna de la función, si el
                símbolo era una función.
        '''
        s = self.lookup(_id)
        if isinstance(s, SymVar):
            return s.value
        else:
            return s.callable

    def get_args(self, _id: str) -> Union[list[list[Type]], list[Type]]:
        '''Retorna la lista con los tipos de argumentos que recibe la función
        con la id especificada.

        En caso de no ser una función, lanza una excepción NotAFunctionError
        '''
        s = self.lookup(_id)
        if isinstance(s, SymFunction):
            return s.args
        raise NotAFunctionError(_id)

    def is_function(self, _id: str) -> bool:
        '''Retorna un booleano indicando si el símbolo con la id especificada
        es una función precargada de la tabla de símbolos.
        '''
        s = self.lookup(_id)
        return isinstance(s, SymFunction) 

    def clear(self):
        '''Limpia la tabla de símbolos. Vuelve a precargar las funciones si
        self.preloaded se estableció como True.
        '''
        if self.preloaded:
            self.table = PRELOADED_FUNCTIONS.copy()
        else:
            self.table = {}
