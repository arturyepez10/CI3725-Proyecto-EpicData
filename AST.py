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

class AST:
    pass

# -------- OPERACIONES BINARIAS --------
class BinOp(AST):
    def __init__(self, op: str, lhs_term: object, rhs_term: object):
        self.op = op
        self.lhs_term = lhs_term
        self.rhs_term = rhs_term

    def __str__(self) -> str:
        return f'({self.lhs_term} {self.op} {self.rhs_term})'

class Comparison(BinOp):
    def __init__(self, op: str, lhs_term: object, rhs_term: object):
        super().__init__(op, lhs_term, rhs_term)

    def __str__(self) -> str:
        return super().__str__()

# -------- OPERACIONES UNARIAS --------
class UnOp(AST):
    def __init__(self, op: str, term: object):
        self.op = op
        self.term = term

    def __str__(self) -> str:
        return f'({self.op}{self.term})'

# -------- TERMINALES --------
class Number(AST):
    def __init__(self, value: object):
        self.value = value

    def __str__(self) -> str:
        return f'Number({self.value})'

class Id(Number):
    def __init__(self, value: object):
        super().__init__(value)
    
    def __str__(self) -> str:
        return f'Id({self.value})'

class Boolean(Number):
    def __init__(self, value: object):
        super().__init__(value)
    
    def __str__(self) -> str:
        return f'Boolean({self.value})'

# -------- TIPOS --------
class Type(AST):
    def __init__(self, _id: object):
        self.id = _id

    def __str__(self) -> str:
        return f'Type({self.id.__str__()})'

# -------- DEFINICIONES --------
class SymDef(AST):
    def __init__(self, _type: Type, _id: object, value: object):
        self.type = _type
        self.id = _id
        self.value = value
        
    def __str__(self) -> str:
        return f'SymDef({self.type}, {self.id}, {self.value})'

# -------- ASIGNACIONES --------
class Assign(AST):
    def __init__(self, _id: object, value: object):
        self.id = _id
        self.value = value

    def __str__(self) -> str:
        return f'Assign({self.id}, {self.value})'

class AssignArrayElement:
    def __init__(self, arrayAccess: object, value: object):
        self.id = arrayAccess.id
        self.index = arrayAccess.index
        self.value = value

    def __str__(self) -> str:
        return f'AssignArrayElement({self.id}, {self.index} , {self.value})'

class AssignArray:
    def __init__(self, _id: object, elements: object):
        self.id = _id
        self.elements = elements

    def __str__(self) -> str:
        return f'AssignArray({self.id}, {self.elements})'


# -------- AGRUPACIONES --------
class Parentheses(AST):
    def __init__(self, expr: object):
        self.expr = expr

    def __str__(self) -> str:
        return f'{self.expr}'

class Quoted(AST):
    def __init__(self, expr: object):
        self.expr = expr

    def __str__(self) -> str:
        return f"'{self.expr}'"

# -------- ARREGLOS --------
class Array:
    def __init__(self, el: object):
        self.elements = []
        if (el): self.elements.append(el)

    def __str__(self) -> str:
        return f'[{", ".join([str(el) for el in self.elements])}]'

class ArrayAccess:
    def __init__(self, _id:object, _index:object) -> None:
        self.id = _id
        self.index = _index

    def __str__(self) -> str:
        return f'ArrayAcces({self.id}, {self.index})'

class Function:
    def __init__(self, _id:object, _args:object) -> None:
        self.id = _id
        self.args = _args

    def __str__(self) -> str:
        return f'Function({self.id}, {self.args})'

class ElemList:
    def __init__(self, el: object):
        self.elements = [el] if el is not None else []

    def append(self, el:object):
        return self.elements.insert(0, el)    

    def __str__(self) -> str:
        return f'ElemList({", ".join([str(el) for el in self.elements])})'
    