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

from .utils.constants import *
from .utils.custom_exceptions import *


class AST:
    def __repr__(self) -> str:
        return self.__str__()

    def ast2str(self) -> str:
        return self.__str__()

# -------- TERMINALES --------
class Terminal(AST):
    def __str__(self) -> str:
        return f'{self.value}'

    def __eq__(self, other) -> str:
        if isinstance(other, type(self)):
            return self.value == other.value
        return False

class Number(Terminal):
    def __init__(self, value: object):
        self.type = NUM
        self.value = value
        
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

class Boolean(Terminal):
    def __init__(self, value: object):
        self.type = NUM
        self.value = value

    def __str__(self) -> str:
        return f'{self.value.__str__().lower()}'

    # Sobrecarga de operadores para Boolean de Stókhos
    def __bool__(self):
        return self.value
        
class Id(Terminal):
    def __init__(self, value: object):
        self.type = None
        self.value = value
    pass

# -------- OPERACIONES BINARIAS --------
class BinOp(AST):
    def __init__(self, op: str, lhs_term: object, rhs_term: object):
        self.type = None
        self.op = op
        self.lhs_term = lhs_term
        self.rhs_term = rhs_term

    def __str__(self) -> str:
        return f'{self.lhs_term} {self.op} {self.rhs_term}'

    def ast2str(self) -> str:
        return f'({self.lhs_term.ast2str()} {self.op} {self.rhs_term.ast2str()})'

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.op == other.op
                and self.lhs_term == other.lhs_term 
                and self.rhs_term == other.rhs_term)
        return False

class Comparison(BinOp):
    pass

# -------- OPERACIONES UNARIAS --------
class UnOp(AST):
    def __init__(self, op: str, term: object):
        self.type = None
        self.op = op
        self.term = term

    def __str__(self) -> str:
        return f'{self.op}{self.term}'

    def ast2str(self) -> str:
        return f'({self.op}{self.term.ast2str()})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.op == other.op 
                and self.term == other.term)
        return False

# -------- TIPOS --------
class Type(AST):
    def __init__(self, _type: object):
        self.type = _type

    def __str__(self) -> str:
        return f'{self.type.__str__()}'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.type == other.type
        return False

class TypeArray(AST):
    def __init__(self, _type: object):
        self.type = _type        

    def __str__(self) -> str:
        return f'[{self.type}]'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            # Hace que un arreglo vacío pase por bool o num según sea necesario
            if self.type.type == 'void' or other.type.type == 'void':
                return True
            return self.type == other.type
        return False

class PrimitiveType(AST):
    def __init__(self, type: object):
        self.type = type        

    def __str__(self) -> str:
        return f'{self.type}'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.type == other.type
        return False

# -------- DEFINICIONES --------
class SymDef(AST):
    def __init__(self, _type: Type, _id: object, rhs_expr: object):
        self.type = _type
        self.id = _id
        self.rhs_expr = rhs_expr
        
    def ast2str(self) -> str:
        return f'SymDef({self.type}, {self.id}, {self.rhs_expr.ast2str()})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.type == other.type
                and self.id == other.id
                and self.rhs_expr == other.rhs_expr)
        return False

# -------- ASIGNACIONES --------
class Assign(AST):
    def __init__(self, _id: object, rhs_expr: object):
        self.id = _id
        self.rhs_expr = rhs_expr

    def ast2str(self) -> str:
        return f'Assign({self.id}, {self.rhs_expr.ast2str()})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id
                and self.rhs_expr == other.rhs_expr)
        return False

class AssignArrayElement(AST):
    def __init__(self, array_access: object, rhs_expr: object):
        self.array_access = array_access
        self.rhs_expr = rhs_expr

    def ast2str(self) -> str:
        return f'Assign({self.array_access}[{self.index.ast2str()}], {self.rhs_expr.ast2str()})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.array_access == other.array_access
                and self.rhs_expr == other.rhs_expr)
        return False

    def execute(self, symbol_table: dict) -> str:        
        
        # Evaluar el indice y lado derecho
        index = self.index.evaluate(symbol_table)        
        val = self.rhs_expr.evaluate(symbol_table)

        try:
            symbol_table[self.id.value].value[index.value].value = val.value
        except IndexError:
            raise RuntimeError(f'El indice {index.value} no está dentro del rango '
                f'de la variable {self.id.value}')
        except TypeError:
            raise RuntimeError(f'Se esperaba un índice entero, pero se '
                f'obtuvo {index.value}')

        return f'{self.id.value}[{index.value}] := {val.value}'

# -------- OTRAS EXPRESIONES --------
class Quoted(AST):
    def __init__(self, expr: object):
        self.type = None
        self.expr = expr

    def __str__(self) -> str:
        return f"'{self.expr}'"
        
    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.expr == other.expr
        return False

class Array(AST):
    def __init__(self, elements: list[object]):
        self.type = None
        self.elements = elements

    def __str__(self) -> str:
        return f'{self.elements}'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.elements == other.elements
        return False

    # Soporte de indexing y cálculo de longitud
    def __len__(self) -> int:
        return len(self.elements)

    def __getitem__(self, index: int) -> object:
        return self.elements[index]

class ArrayAccess(AST):
    def __init__(self, id: object, _index:object):
        self.type = None
        self.id = id
        self.index = _index

    def __str__(self) -> str:
        return f'{self.id}[{self.index}]'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id
                and self.index == other.index)
        return False

class Function(AST):
    def __init__(self, _id: object, _args: list[object]):
        self.type = None
        self.id = _id
        self.args = _args

    def __str__(self) -> str:
        args_str = f'{self.args}'
        return f'{self.id}({args_str[1:-1]})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id
                and self.args == other.args)
        return False

# --- AST DE ERROR ---
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
# De utilidad para 'inferencia de tipos'
VOID_ARRAY = Type(TypeArray(PrimitiveType('void')))
