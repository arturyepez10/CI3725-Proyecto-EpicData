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
    def __repr__(self) -> str:
        return self.__str__()
    
    def type_check(self, symbol_table):
        raise Exception('Type check not implemented')

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

    def type_check(self, symbol_table):
        expected_type = self.expected_type()
        lhs_type = self.lhs_term.type_check(symbol_table)
        rhs_type = self.rhs_term.type_check(symbol_table)
        
        if lhs_type == rhs_type and rhs_type == expected_type:
            return self.return_type()
        else:
            raise Exception(f'"{self.term}" is not "{expected_type.type}" type')

    def expected_type(self):
        if self.op in ['&&', '||']:
            return Type(PrimitiveType('bool'))
        else:
            return Type(PrimitiveType('num'))

    def return_type(self):
        return self.expected_type()


class Comparison(BinOp):
    def expected_type(self):
        return Type(PrimitiveType('num'))

    def return_type(self):
        return Type(PrimitiveType('bool'))

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
    
    def type_check(self, symbol_table):
        expected_type = self.expected_type()
        if self.term.type_check(symbol_table) == expected_type:
            return self.return_type()
        else:
            raise Exception(f'"{self.term}" is not "{expected_type.type}" type')

    def expected_type(self):
        if self.op in ['+', '-']:
            return Type(PrimitiveType('num'))
        else:
            return Type(PrimitiveType('bool'))

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
    def type_check(self, symbol_table):
        return Type(PrimitiveType('num'))        

class Id(Terminal):
    def type_check(self, symbol_table):

        if symbol_table.get(self.value):
            return symbol_table.get(self.value)

        else:
            raise Exception(f'No existe "{self.value}" en la tabla de simbolos')

class Boolean(Terminal):
    def type_check(self, symbol_table):
        return Type(PrimitiveType('bool'))  

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


class AssignArrayElement(AST):
    def __init__(self, arrayAccess: object, value: object):
        self.id = arrayAccess.id
        self.index = arrayAccess.index
        self.value = value

    def __str__(self) -> str:
        return f'AssignArrayElement({self.id}, {self.index} , {self.value})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id
                and self.index == other.index
                and self.value == other.value)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

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

    def type_check(self, symbol_table):
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

    def type_check(self, symbol_table):
        return self.expr.type_check(symbol_table)

# -------- ARREGLOS --------
class Array(AST):
    def __init__(self, elements: object) -> None:
        self.elements = elements

    def __str__(self) -> str:
        return f'Array({self.elements})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.elements == other.elements
            
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')


class ArrayAccess(AST):
    def __init__(self, _id:object, _index:object) -> None:
        self.id = _id
        self.index = _index

    def __str__(self) -> str:
        return f'ArrayAcces({self.id}, {self.index})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id
                and self.index == other.index)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')


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


class ElemList(AST):
    def __init__(self, el: object):
        self.elements = [el] if el else []

    def append(self, el:object):
        return self.elements.insert(0, el)

    def __str__(self) -> str:
        return f'ElemList({", ".join([str(el) for el in self.elements])})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.elements == other.elements
             
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')


    # Metodo usado para debug
    def __debug_Init__(self, elements:object):
        self.elements = elements
        return self


class Error(AST):
    def __init__(self, cause: str):
        self.cause = cause
    
    def __str__(self) -> str:
        return f'''Error('{self.cause}')'''


