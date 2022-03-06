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

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.op == other.op 
                and self.lhs_term == other.lhs_term 
                and self.rhs_term == other.rhs_term)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def __repr__(self) -> str:
        return self.__str__()


class Comparison(BinOp):
    pass

class NumberBinOp(BinOp):
    pass

class BooleanBinOp(BinOp):
    pass

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

class BooleanUnOp(UnOp):
    pass

class NumberUnOp(UnOp):
    pass


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

    def __repr__(self) -> str:
        return self.__str__()

class Number(Terminal):
    pass        

class Id(Terminal):
    pass

class Boolean(Terminal):
    pass

# -------- TIPOS --------
class Type(AST):
    def __init__(self, _id: object):
        self.id = _id

    def __str__(self) -> str:
        return f'Type({self.id.__str__()})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.id == other.id
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')
    
    def __repr__(self) -> str:
        return self.__str__()
        

# -------- DEFINICIONES --------
class SymDef(AST):
    def __init__(self, _type: Type, _id: object, value: object):
        self.type = _type
        self.id = _id
        self.value = value
        
    def __str__(self) -> str:
        return f'SymDef({self.type}, {self.id}, {self.value})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.type == other.type
                and self.id == other.id
                and self.value == other.value)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')
    
    def __repr__(self) -> str:
        return self.__str__()

# -------- ASIGNACIONES --------
class Assign(AST):
    def __init__(self, _id: object, value: object):
        self.id = _id
        self.value = value

    def __str__(self) -> str:
        return f'Assign({self.id}, {self.value})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id
                and self.value == other.value)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def __repr__(self) -> str:
        return self.__str__()

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
class TypeArray:
    def __init__(self, type: object):
        self.type = type        

    def __str__(self) -> str:
        return f'[{self.type}]'

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
    