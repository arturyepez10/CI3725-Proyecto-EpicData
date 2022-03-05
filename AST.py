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
    def __init__(self, _id: str):
        self.id = _id

    def __str__(self) -> str:
        return f'Type({self.value})'

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
        self. value = value

    def __str__(self) -> str:
        return f'Assign({self.id}, {self.value})'

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
        
    def __str__()