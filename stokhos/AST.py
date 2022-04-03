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

from stokhos.utils.custom_exceptions import SemanticError

class AST:
    def __repr__(self) -> str:
        return self.__str__()
    
    def type_check(self, symbol_table):
        raise SemanticError('Type check not implemented')

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
        
        try:
            if lhs_type == expected_type and rhs_type == expected_type:
                return self.return_type()
            else:
                raise SemanticError(f'"{self.op}" no se puede aplicar a '
                    f'operandos de tipo {lhs_type.type} y {rhs_type.type}')
        except TypeError:
            raise SemanticError(f'"{self.op}" no se puede aplicar a operandos '
                f'de tipo {lhs_type.type} y {rhs_type.type}')

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
        term_type = self.term.type_check(symbol_table)

        try:
            if term_type == expected_type:
                return self.return_type()
            else:
                raise SemanticError(f'"{self.op}" no se puede aplicar a '
                    f'operando de tipo {term_type.type}')
        except TypeError as e:
            raise SemanticError(f'"{self.op}" no se puede aplicar a operando '
                f' de tipo {term_type.type}')

    def expected_type(self):
        if self.op == '!':
            return Type(PrimitiveType('bool'))
        else:
            return Type(PrimitiveType('num'))

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
    def type_check(self, symbol_table):
        return Type(PrimitiveType('num'))

class Id(Terminal):
    # Caso base del type checking
    def type_check(self, symbol_table):
        if self.value in symbol_table:
            return symbol_table[self.value].type
        else:
            raise SemanticError(f'Variable "{self.value}" no definida')

class Boolean(Terminal):
    # Sobrecarga de operadores para Boolean de Stókhos
    def __bool__(self):
        return self.value

    # Caso base del type checking
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

    def type_check(self, symbol_table):

        if symbol_table.get(self.id.value):
            raise SemanticError(f'"{self.id.value}" is already defined in the symbol table')

        expected_type = self.type
        rhs_type = self.rhs.type_check(symbol_table)

        if isinstance(rhs_type.type, type(expected_type.type)) and rhs_type == expected_type:
            return Type(PrimitiveType('void'))
        else:
            raise SemanticError(f'"{self.rhs}" is not "{expected_type.type}" type')

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

    def type_check(self, symbol_table):
        # Añadir qeu la variable exista en la tabla de simbolos
        var_type = self.id.type_check(symbol_table)
        rhs_type = self.rhs.type_check(symbol_table)

        if isinstance(rhs_type.type, type(var_type.type)) and rhs_type == var_type:
            return Type(PrimitiveType('void'))
        else:
            raise SemanticError(f'"{self.rhs}" is not "{var_type.type}" type,'
            f' at assigning value to variable "{self.id}"')

class AssignArrayElement(AST):
    def __init__(self, arrayAccess: object, rhs: object):
        self.id = arrayAccess.id
        self.index = arrayAccess.index
        self.rhs = rhs

    def __str__(self) -> str:
        return f'AssignArrayElement({self.id}, {self.index} , {self.rhs})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id
                and self.index == other.index
                and self.rhs == other.rhs)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def type_check(self, symbol_table):
        array_type = self.id.type_check(symbol_table)
        index_type = self.index.type_check(symbol_table)
        rhs_type = self.rhs.type_check(symbol_table)

        # Tratar de acceder a algo que no es de tipo arreglo
        if not isinstance(array_type.type, TypeArray):
            raise SemanticError(f'{self.id} is not an array')

        # Tratar de usar un indice que no es un numero
        if not isinstance(index_type.type, PrimitiveType) or index_type != Type(PrimitiveType('num')):
            raise SemanticError(f'{self.index} is not num type, bad array access')

        # Comprobar que el tipo del arreglo es el mismo tipo que el rhs
        if isinstance(rhs_type.type, type(array_type.type.type)) and rhs_type.type == array_type.type.type:
            return Type(PrimitiveType('void'))
        else:
            raise SemanticError(f'"{self.rhs}" is not "{array_type.type}" type')

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
    
    def type_check(self, symbol_table):
        if len(self.list.elements) == 0:
            raise SemanticError('Not enough information to infer type')

        array_type = self.list.elements[0].type_check(symbol_table)

        try: 
            # Hacer mejor diseño
            # Quiero tratar de reportar cuál es el primer elemento que falla la aserción
            assert all([x.type_check(symbol_table) == array_type for x in self.list.elements])
        except (TypeError, AssertionError):
            raise SemanticError('non-homogeneous array')
        
        return Type(TypeArray(array_type.type)) 


class ArrayAccess(AST):
    def __init__(self, _id:object, _index:object) -> None:
        self.id = _id
        self.index = _index

    def __str__(self) -> str:
        return f'ArrayAccess({self.id}, {self.index})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id
                and self.index == other.index)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def type_check(self, symbol_table): 
        array_type = self.id.type_check(symbol_table)
        index_type = self.index.type_check(symbol_table)

        # Tratar de acceder a algo que no es de tipo arreglo
        if not isinstance(array_type.type, TypeArray):
            raise SemanticError(f'{self.id} is not an array')

        # Tratar de usar un indice que no es un numero
        if not isinstance(index_type.type, PrimitiveType) or index_type != Type(PrimitiveType('num')):
            raise SemanticError(f'{self.index} is not num type, bad array access')

        return Type(array_type.type.type)


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
        self.type = _type
        self.value = value

# --- CLASE DE ERROR ---

class Error(AST):
    def __init__(self, cause: str):
        self.cause = cause
    
    def __str__(self) -> str:
        return f'''Error('{self.cause}')'''


