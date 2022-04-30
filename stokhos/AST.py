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
from typing import Union

from .utils.constants import *
from .utils.custom_exceptions import *


class AST:
    def __repr__(self) -> str:
        return self.ast2str()

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
    def __init__(self, value: int):
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
    def __init__(self, value: bool):
        self.type = BOOL
        self.value = value

    def __str__(self) -> str:
        return super().__str__().lower()

    # Sobrecarga de operadores para Boolean de Stókhos
    def __bool__(self):
        return self.value

class Id(Terminal):
    def __init__(self, value: str):
        self.type = None
        self.value = value

# -------- TIPOS --------
class TypedArray(AST):
    def __init__(self, _type: str):
        self.type = _type

    def __str__(self) -> str:
        return f'[{self.type}]'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            # Hace que un arreglo vacío pase por bool o num según sea necesario
            if self.type == 'any' or other.type== 'any':
                return True
            return self.type == other.type
        return False

class Type(AST):
    def __init__(self, _type: Union[TypedArray, str]):
        self.type = _type

    def __str__(self) -> str:
        return f'{self.type.__str__()}'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.type == other.type
        return False

# -------- OPERACIONES BINARIAS --------
class BinOp(AST):
    def __init__(self, op: str, lhs: AST, rhs: AST):
        self.type = None
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        # Remueve lo paréntesis redundantes más externos
        return self.ast2str()[1:-1]

    def ast2str(self) -> str:
        return f'({self.lhs.ast2str()} {self.op} {self.rhs.ast2str()})'

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.op == other.op
                and self.lhs == other.lhs 
                and self.rhs == other.rhs)
        return False

class Comparison(BinOp):
    pass

# -------- OPERACIONES UNARIAS --------
class UnOp(AST):
    def __init__(self, op: str, term: AST):
        self.type = None
        self.op = op
        self.term = term

    def __str__(self) -> str:
        # Remueve lo paréntesis redundantes más externos
        return self.ast2str()[1:-1]

    def ast2str(self) -> str:
        return f'({self.op}{self.term.ast2str()})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.op == other.op 
                and self.term == other.term)
        return False

# -------- OTRAS EXPRESIONES --------
class Quoted(AST):
    def __init__(self, expr: AST):
        self.type = None
        self.expr = expr

    def __str__(self) -> str:
        return f"'{self.expr}'"

    def ast2str(self) -> str:
        return f"'{self.expr.ast2str()}'"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.expr == other.expr
        return False

class Array(AST):
    def __init__(self, elements: list[AST]):
        self.type = None
        self.elements = elements

    def __str__(self) -> str:
        return f'{self.elements}'

    def ast2str(self) -> str:
        els_str = ', '.join([el.ast2str() for el in self.elements])
        return f'[{els_str}]'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.elements == other.elements
        return False

    # Soporte de indexing y cálculo de longitud
    def __len__(self) -> int:
        return len(self.elements)

    def __getitem__(self, index: int) -> AST:
        return self.elements[index]

    def __setitem__(self, index: int, value: AST):
        self.elements[index] = value

class FunctionCall(AST):
    def __init__(self, _id: Id, _args: list[AST]):
        self.type = None
        self.id = _id
        self.args = _args

    def __str__(self) -> str:
        args_str = f'{self.args}'
        return f'{self.id}({args_str[1:-1]})'

    def ast2str(self) -> str:
        args_str = ', '.join([arg.ast2str() for arg in self.args])
        return f'{self.id}({args_str})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id
                and self.args == other.args)
        return False

class ArrayAccess(AST):
    def __init__(self, expr: Union[Id, FunctionCall, Array], _index: AST):
        self.type = None
        self.expr = expr # Puede ser una id, un arreglo o una función
        self.index = _index

    def __str__(self) -> str:
        return f'{self.expr}[{self.index}]'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.expr == other.expr
                and self.index == other.index)
        return False

# -------- DEFINICIONES --------
class SymDef(AST):
    def __init__(self, _type: Type, _id: Id, rhs: AST):
        self.type = _type
        self.id = _id
        self.rhs = rhs

    def ast2str(self) -> str:
        return f'SymDef({self.type}, {self.id}, {self.rhs.ast2str()})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.type == other.type
                and self.id == other.id
                and self.rhs == other.rhs)
        return False

# -------- ASIGNACIONES --------
class Assign(AST):
    def __init__(self, _id: Id, rhs: AST):
        self.id = _id
        self.rhs = rhs

    def ast2str(self) -> str:
        return f'Assign({self.id}, {self.rhs.ast2str()})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id
                and self.rhs == other.rhs)
        return False

class AssignArrayElement(AST):
    def __init__(self, array_access: ArrayAccess, rhs: object):
        self.array_access = array_access
        self.rhs = rhs

    def ast2str(self) -> str:
        return f'Assign({self.array_access}[{self.index.ast2str()}], {self.rhs.ast2str()})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.array_access == other.array_access
                and self.rhs == other.rhs)
        return False

# --- AST DE ERROR ---
class Error(AST):
    def __init__(self, cause: str):
        self.cause = cause

    def __str__(self) -> str:
        return f"Error('{self.cause}')"

# Alias para los tipos de datos
NUM = Type('num')
BOOL = Type('bool')
VOID = Type('void')
NUM_ARRAY = Type(TypedArray('num'))
BOOL_ARRAY = Type(TypedArray('bool'))
# De utilidad para 'inferencia de tipos'
ANY_ARRAY = Type(TypedArray('any'))
