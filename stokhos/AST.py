"""Arbol de Sintaxis Abstracta de utilidad para el parsing de Stókhos.

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

from .utils.custom_exceptions import NotEnoughInfoError, SemanticError
from .utils.constants import *

class AST:
    def __repr__(self) -> str:
        return self.__str__()
    
    def type_check(self, symbol_table: dict):
        raise SemanticError('Chequeo de tipos no implementado')

# -------- OPERACIONES BINARIAS --------
class BinOp(AST):
    def __init__(self, op: str, lhs_term: object, rhs_term: object):
        self.op = op
        self.lhs_term = lhs_term
        self.rhs_term = rhs_term

    def __str__(self) -> str:
        return f'({self.lhs_term} {self.op} {self.rhs_term})'

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.op == other.op
                and self.lhs_term == other.lhs_term 
                and self.rhs_term == other.rhs_term)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def type_check(self, symbol_table: dict):
        expected_type = self.expected_type()
        lhs_type = self.lhs_term.type_check(symbol_table)
        rhs_type = self.rhs_term.type_check(symbol_table)
        
        try:
            if lhs_type == expected_type and rhs_type == expected_type:
                return self.return_type()
        except TypeError:
            pass
        else:
            raise SemanticError(f'"{self.op}" no se puede aplicar a operandos '
                f'de tipo {lhs_type.type} y {rhs_type.type}')

    def expected_type(self):
        if self.op in ['&&', '||']:
            return BOOL
        else:
            return NUM

    def return_type(self):
        return self.expected_type()

    def evaluate(self, symbol_table: dict):
        if self.op == '+':
            return self.lhs_term.evaluate(symbol_table) + self.rhs_term.evaluate(symbol_table)
        elif self.op == '-':
            return self.lhs_term.evaluate(symbol_table) - self.rhs_term.evaluate(symbol_table)
        elif self.op == '*':
            return self.lhs_term.evaluate(symbol_table) * self.rhs_term.evaluate(symbol_table)
        elif self.op == '/':
            return self.lhs_term.evaluate(symbol_table) / self.rhs_term.evaluate(symbol_table)
        elif self.op == '%':
            return self.lhs_term.evaluate(symbol_table) % self.rhs_term.evaluate(symbol_table)
        elif self.op == '^':
            return self.lhs_term.evaluate(symbol_table) ** self.rhs_term.evaluate(symbol_table)
        elif self.op == '&&':
            return self.lhs_term.evaluate(symbol_table) and self.rhs_term.evaluate(symbol_table)
        else:
            return self.lhs_term.evaluate(symbol_table) or self.rhs_term.evaluate(symbol_table)

class Comparison(BinOp):
    def expected_type(self):
        return NUM

    def return_type(self):
        return BOOL

    def type_check(self, symbol_table: dict):
        lhs_type = self.lhs_term.type_check(symbol_table)
        rhs_type = self.rhs_term.type_check(symbol_table)
        
        if self.op in ['<>', '=']:
            try:
                if isinstance(rhs_type.type, PrimitiveType) and rhs_type == lhs_type:
                    return self.return_type()
            except TypeError:
                pass
            else:
                raise SemanticError(f'"{self.op}" no se puede aplicar a operandos '
                    f'de tipo {lhs_type.type} y {rhs_type.type}')
        else:
            expected_type = self.expected_type()
            lhs_type = self.lhs_term.type_check(symbol_table)
            rhs_type = self.rhs_term.type_check(symbol_table)
            
            try:
                if lhs_type == expected_type and rhs_type == expected_type:
                    return self.return_type()
            except TypeError:
                pass
            else:
                raise SemanticError(f'"{self.op}" no se puede aplicar a operandos '
                    f'de tipo {lhs_type.type} y {rhs_type.type}')

# -------- OPERACIONES UNARIAS --------
class UnOp(AST):
    def __init__(self, op: str, term: object):
        self.op = op
        self.term = term

    def __str__(self) -> str:
        return f'({self.op}{self.term})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.op == other.op 
                and self.term == other.term)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')
    
    def type_check(self, symbol_table: dict):
        expected_type = self.expected_type()
        term_type = self.term.type_check(symbol_table)

        try:
            if term_type == expected_type:
                return self.return_type()
        except TypeError:
            pass
        else:
            raise SemanticError(f'"{self.op}" no se puede aplicar a operando '
                f' de tipo {term_type.type}')

    def expected_type(self):
        if self.op == '!':
            return BOOL
        else:
            return NUM

    def return_type(self):
        return self.expected_type()

# -------- TERMINALES --------
class Terminal(AST):
    def __init__(self, value: object):
        self.value = value

    def __str__(self) -> str:
        return f'{type(self).__name__}({self.value})'

    def __eq__(self, other) -> str:
        if isinstance(other, type(self)):
            return self.value == other.value
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

class Number(Terminal):
    # Sobrecarga de operadores para números de Stókhos
    def __add__(self, other):
        return Number(self.value + other.value)

    def __sub__(self, other):
        return Number(self.value - other.value)
    
    def __mul__(self, other):
        return Number(self.value * other.value)
    
    def __truediv__(self, other):
        return Number(self.value / other.value)
    
    def __mod__(self, other):
        return Number(self.value % other.value)
    
    def __pow__(self, other):
        return Number(self.value ** other.value)

    def __neg__(self):
        return Number(-self.value)
    
    def __pos__(self):
        return self
    
    def __lt__(self, other):
        return Boolean(self.value < other.value)

    def __le__(self, other):
        return Boolean(self.value <= other.value)
    
    def __gt__(self, other):
        return Boolean(self.value > other.value)
    
    def __ge__(self, other):
        return Boolean(self.value >= other.value)

    def __floor__(self):
        return Number(floor(self.value))

    # Caso base del type checking
    def type_check(self, symbol_table: dict):
        return NUM

    def evaluate(self, symbol_table: dict):
        return Number(self.value)

class Id(Terminal):
    # Caso base del type checking
    def type_check(self, symbol_table: dict):
        if self.value in symbol_table:
            return symbol_table[self.value].type
        else:
            raise SemanticError(f'Variable "{self.value}" no definida')

    def evaluate(self, symbol_table: dict):
        if self.value in symbol_table:
            return symbol_table[self.value].value
        else:
            # Verificar si en algún caso hace falta esto
            raise SemanticError(f'Variable "{self.value}" no definida')

class Boolean(Terminal):
    # Sobrecarga de operadores para Boolean de Stókhos
    def __bool__(self):
        return self.value

    # Caso base del type checking
    def type_check(self, symbol_table: dict):
        return BOOL
    
    def evaluate(self, symbol_table: dict):
        return Boolean(self.value)

# -------- TIPOS --------
class Type(AST):
    def __init__(self, _type: object):
        self.type = _type

    def __str__(self) -> str:
        return f'Type({self.type.__str__()})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.type == other.type
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

class TypeArray(AST):
    def __init__(self, type: object):
        self.type = type        

    def __str__(self) -> str:
        return f'Array({self.type})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.type == other.type
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def __repr__(self) -> str:
        return f'TypeArray({self.type})'

class PrimitiveType(AST):
    def __init__(self, type: object):
        self.type = type        

    def __str__(self) -> str:
        return f'{self.type}'

    def __repr__(self) -> str:
        return f'PrimitiveType({self.type})'    

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.type == other.type
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

# -------- DEFINICIONES --------
class SymDef(AST):
    def __init__(self, _type: Type, _id: object, rhs: object):
        self.type = _type
        self.id = _id
        self.rhs = rhs
        
    def __str__(self) -> str:
        return f'SymDef({self.type}, {self.id}, {self.rhs})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.type == other.type
                and self.id == other.id
                and self.rhs == other.rhs)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def type_check(self, symbol_table: dict):
        if self.id.value in symbol_table:
            raise SemanticError(f'Variable "{self.id.value}" ya definida anteriormente')

        expected_type = self.type
        try:
            rhs_type = self.rhs.type_check(symbol_table)
        except NotEnoughInfoError:
            rhs_type = expected_type

        try:
            if expected_type == rhs_type:
                return VOID
        except TypeError:
            pass
        else:
            raise SemanticError(f'El tipo inferido es {rhs_type.type}, pero se '
                f'esperaba {expected_type.type}')

    def execute(self, symbol_table: dict) -> str:
        val = self.rhs.evaluate(symbol_table)
        if type(val) == Number:
            _type = NUM
        elif type(val) == Boolean:
            _type = BOOL

        symbol_table[self.id.value] = Symbol(_type, val)
        return f'{self.type.type} {self.id.value} := {val.value}'

# -------- ASIGNACIONES --------
class Assign(AST):
    def __init__(self, _id: object, rhs: object):
        self.id = _id
        self.rhs = rhs

    def __str__(self) -> str:
        return f'Assign({self.id}, {self.rhs})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id
                and self.rhs == other.rhs)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def type_check(self, symbol_table: dict):
        if self.id.value not in symbol_table:
            raise SemanticError(f'Variable "{self.id.value}" no definida '
                'anteriormente')
        
        var_type = self.id.type_check(symbol_table)
        try:
            rhs_type = self.rhs.type_check(symbol_table)
        except NotEnoughInfoError:
            rhs_type = var_type

        try:
            if var_type == rhs_type:
                return VOID
        except TypeError:
            pass
        else:
            raise SemanticError(f'El tipo inferido es {rhs_type}, pero se '
                f'esperaba {var_type}')

    def execute(self, symbol_table: dict) -> str:
        val = self.rhs.evaluate(symbol_table)
        symbol_table[self.id.value].value = val
        return f'{self.id.value} := {val.value}'

class AssignArrayElement(AST):
    def __init__(self, arrayAccess: object, rhs: object):
        self.array_access = arrayAccess.expr
        self.rhs = rhs

    def __str__(self) -> str:
        return f'AssignArrayElement({self.array_access}, {self.index} , {self.rhs})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.array_access == other.array_access
                and self.rhs == other.rhs)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def type_check(self, symbol_table: dict):
        array_type = self.array_access.type_check(symbol_table)
        rhs_type = self.rhs.type_check(symbol_table)

        try:
            if rhs_type.type == array_type.type.type:
                return VOID
        except TypeError:
            pass    
        else:
            raise SemanticError(f'El tipo inferido es {rhs_type.type}, pero se '
                f'esperaba {array_type.type.type}')

# -------- AGRUPACIONES --------
class Parentheses(AST):
    def __init__(self, expr: object):
        self.expr = expr

    def __str__(self) -> str:
        return f'{self.expr}'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.expr == other.expr
               
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def type_check(self, symbol_table: dict):
        return self.expr.type_check(symbol_table)


class Quoted(AST):
    def __init__(self, expr: object):
        self.expr = expr

    def __str__(self) -> str:
        return f"'{self.expr}'"
        
    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.expr == other.expr
               
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def type_check(self, symbol_table: dict):
        return self.expr.type_check(symbol_table)

    def evaluate(self, symbol_table: dict) -> str:
        return self.expr

# -------- ARREGLOS --------
class Array(AST):
    def __init__(self, list: object) -> None:
        self.list = list

    def __str__(self) -> str:
        return f'Array({self.list})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.list == other.list
            
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    # Soporte de indexing y cálculo de longitud
    def __len__(self) -> Number:
        return len(self.list)

    def __getitem__(self, index: int) -> object:
        return self.list[index]
    
    def type_check(self, symbol_table: dict):
        if not self:
            raise NotEnoughInfoError('No hay suficiente información para inferir '
                'el tipo del arreglo')

        array_type = self[0].type_check(symbol_table)

        for el in self:
            # Chequea que no haya arreglos anidados
            if isinstance(el, Array):
                raise SemanticError('Arreglos anidados no están permitidos')
            
            # Chequea que todos los elementos sean del mismo tipo
            if el.type_check(symbol_table) != array_type:
                raise SemanticError(f'El tipo de todos los elementos del '
                    f'arreglo debe ser {array_type.type}')
        return Type(TypeArray(array_type.type))
            
        
class ArrayAccess(AST):
    def __init__(self, expr: object, _index:object) -> None:
        self.expr = expr
        self.index = _index

    def __str__(self) -> str:
        return f'ArrayAccess({self.expr}, {self.index})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.expr == other.expr
                and self.index == other.index)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def type_check(self, symbol_table: dict):
        array_type = self.expr.type_check(symbol_table)
        index_type = self.index.type_check(symbol_table)

        # Verifica que se intente acceder a un arreglo
        if not isinstance(array_type.type, TypeArray):
            raise SemanticError('No se permite el acceso a arreglo para '
                f'expresión de tipo {array_type.type}')

        try:
            # Verifica que se el índice de acceso sea un número
            if index_type == NUM:
                return Type(array_type.type.type)
        except TypeError:
            pass
        else:
            raise SemanticError(f'El tipo inferido del índice es '
                f'{index_type.type}, pero se esperaba num')

class Function(AST):
    def __init__(self, _id:object, _args:object) -> None:
        self.id = _id
        self.args = _args

    def __str__(self) -> str:
        return f'Function({self.id}, {self.args})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id
                and self.args == other.args)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def type_check(self, symbol_table: dict):
        # Verifica que la función exista
        if self.id.value not in symbol_table:
            raise SemanticError(f'Variable "{self.value}" no definida')

        # Verifica que cada argumento sea del tipo correspondiente según la 
        # firma de la función
        expected_args = symbol_table[self.id.value].value.args
        
        if expected_args:
            for k, arg_list in enumerate(expected_args):
                # Si no coincide el número de argumentos
                if len(self.args) != len(arg_list):
                    # Si hay sobrecarga se pasa a la siguiente
                    if k != len(expected_args) - 1:
                        continue
                    
                    # Si ya no quedan sobrecargan se lanza el error
                    raise SemanticError(f'La función "{self.id.value}" esperaba '
                        f'{len(arg_list)} argumentos, pero se recibieron '
                        f'{len(self.args)}')
                try:
                    # Se verifica argumento a argumento
                    for i, expected_arg_type in enumerate(arg_list):
                        cur_arg_type = self.args[i].type_check(symbol_table)
                        if cur_arg_type != expected_arg_type:
                            raise TypeError

                    # Si se llega hasta acá, todos los argumentos han sido 
                    # validados correctamente
                    return symbol_table[self.id.value].type
                except TypeError:
                    # Si hay sobrecarga se pasa a la siguiente
                    if k != len(expected_args) - 1:
                        continue

                    # Si ya no quedan sobrecargas se lanza el error
                    raise SemanticError(f'El tipo del argumento #{i + 1} es '
                        f'{cur_arg_type.type}, pero se esperaba '
                        f' {expected_arg_type.type}')
        else:
            if len(self.args) != 0:
                raise SemanticError(f'La función "{self.id.value}" esperaba '
                    f'0 argumentos, pero se recibieron {len(self.args)}')

        return symbol_table[self.id.value].type

class ElemList(AST):
    def __init__(self, el: object):
        self.elements = [] if el is None else [el]

    def append(self, el:object):
        return self.elements.insert(0, el)

    def __str__(self) -> str:
        return f'ElemList({", ".join([str(el) for el in self.elements])})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.elements == other.elements
             
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    # Soporte de indexing y cálculo de longitud
    def __len__(self) -> int:
        return len(self.elements)
    
    def __getitem__(self, index):
        return self.elements[index]

    # Metodo usado para debug
    def __debug_Init__(self, elements:object):
        self.elements = elements
        return self

    # El chequeo de tipos de esta clase se hace por medio de las clases funciones
    # de funciones o arreglos

# --- ENTRADAS DE LA TABLA DE SIMBOLOS ---
class Symbol(AST):
    def __init__(self, _type: object, value: object):
        # Si es una función, tiene el tipo de retorno de la misma
        self.type = _type
        self.value = value

class FunctionSignature(AST):
    def __init__(self, callable: object, _args: list[Type] = None):
        # Función llamable de Python con la implementación de la misma
        self.callable = callable

        # Lista de listas donde cada elemento tiene la siguiente forma:
        # El i-ésimo elemento es el tipo del i-ésimo argumento
        # que acepta la función. None si no tiene argumentos
        self.args = _args

# --- CLASE DE ERROR ---

class Error(AST):
    def __init__(self, cause: str):
        self.cause = cause
    
    def __str__(self) -> str:
        return f'''Error('{self.cause}')'''

# Alias para los tipos de datos
NUM = Type(PrimitiveType('num'))
BOOL = Type(PrimitiveType('bool'))
VOID = Type(PrimitiveType('void'))
NUM_ARRAY = Type(TypeArray(PrimitiveType('num')))
BOOL_ARRAY = Type(TypeArray(PrimitiveType('bool')))