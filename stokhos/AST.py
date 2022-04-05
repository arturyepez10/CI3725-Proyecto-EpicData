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
import operator
from math import floor


from .utils.custom_exceptions import *
from .utils.constants import *

class AST:
    def __repr__(self) -> str:
        return self.__str__()

    def ast2str(self) -> str:
        return self.__str__()
    
    def type_check(self, symbol_table: dict):
        raise SemanticError(f'Chequeo de tipos no implementado para {type(self)}')

    def evaluate(self, symbol_table: dict):
        raise SemanticError(f'Evaluacion no implementada para {type(self)}')

# -------- TERMINALES --------
class Terminal(AST):
    def __init__(self, value: object):
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'

    def __eq__(self, other) -> str:
        if isinstance(other, type(self)):
            return self.value == other.value
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def evaluate(self, symbol_table: dict):
        return self

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
    def __str__(self) -> str:
        return f'{self.value.__str__().lower()}'

    # Sobrecarga de operadores para Boolean de Stókhos
    def __bool__(self):
        return self.value

    # Caso base del type checking
    def type_check(self, symbol_table: dict):
        return BOOL

# -------- OPERACIONES BINARIAS --------
class BinOp(AST):
    def __init__(self, op: str, lhs_term: object, rhs_term: object):
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
            raise SemanticError(f'"{self.op}" no se puede aplicar a operandos '
                f'de tipo {lhs_type.type} y {rhs_type.type}')
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
        return BINARY_OP[self.op](
            self.lhs_term.evaluate(symbol_table), 
            self.rhs_term.evaluate(symbol_table)
        )

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
                raise SemanticError(f'"{self.op}" no se puede aplicar a operandos '
                    f'de tipo {lhs_type.type} y {rhs_type.type}')
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
                SemanticError(f'"{self.op}" no se puede aplicar a operandos '
                    f'de tipo {lhs_type.type} y {rhs_type.type}')
            else:
                raise SemanticError(f'"{self.op}" no se puede aplicar a operandos '
                    f'de tipo {lhs_type.type} y {rhs_type.type}')

    def evaluate(self, symbol_table: dict):
        return BINARY_OP[self.op](
            self.lhs_term.evaluate(symbol_table),
            self.rhs_term.evaluate(symbol_table)
        )

# -------- OPERACIONES UNARIAS --------
class UnOp(AST):
    def __init__(self, op: str, term: object):
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
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')
    
    def type_check(self, symbol_table: dict):
        expected_type = self.expected_type()
        term_type = self.term.type_check(symbol_table)

        try:
            if term_type == expected_type:
                return self.return_type()
        except TypeError:
            raise SemanticError(f'"{self.op}" no se puede aplicar a operando '
                f'de tipo {term_type.type}')
        else:
            raise SemanticError(f'"{self.op}" no se puede aplicar a operando '
                f'de tipo {term_type.type}')

    def expected_type(self):
        if self.op == '!':
            return BOOL
        else:
            return NUM

    def return_type(self):
        return self.expected_type()

    def evaluate(self, symbol_table: dict):
        return UNARY_OP[self.op](
            self.term.evaluate(symbol_table)
        )

# -------- TIPOS --------
class Type(AST):
    def __init__(self, _type: object):
        self.type = _type

    def __str__(self) -> str:
        return f'{self.type.__str__()}'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.type == other.type
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

class TypeArray(AST):
    def __init__(self, type: object):
        self.type = type        

    def __str__(self) -> str:
        return f'[{self.type}]'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.type == other.type
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

class PrimitiveType(AST):
    def __init__(self, type: object):
        self.type = type        

    def __str__(self) -> str:
        return f'{self.type}'

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
        
    def ast2str(self) -> str:
        return f'SymDef({self.type}, {self.id}, {self.rhs.ast2str()})'

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
            raise SemanticError(f'El tipo inferido es {rhs_type.type}, pero se '
                f'esperaba {expected_type.type}')
        else:
            raise SemanticError(f'El tipo inferido es {rhs_type.type}, pero se '
                f'esperaba {expected_type.type}')

    def execute(self, symbol_table: dict) -> str:
        val = self.rhs.evaluate(symbol_table)   
        
        # Se agrega el símbolo a la tabla de símbolos
        # No se verifica el tipo de val porque solo es posible
        # execute luego de una evaluación
        symbol_table[self.id.value] = Symbol(self.type, val)

        if issubclass(type(val), Terminal):
            return f'{self.type.type} {self.id.value} := {val.value}'
        else:
            return f'{self.type.type} {self.id.value} := {val}'

# -------- ASIGNACIONES --------
class Assign(AST):
    def __init__(self, _id: object, rhs: object):
        self.id = _id
        self.rhs = rhs

    def ast2str(self) -> str:
        return f'Assign({self.id}, {self.rhs.ast2str()})'

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

        if self.id.value in PRELOADED_FUNCTIONS:
            raise SemanticError(f'Variable "{self.id.value}" es una función '
                'precargada, no se puede asignar')
        
        var_type = self.id.type_check(symbol_table)
        try:
            rhs_type = self.rhs.type_check(symbol_table)
        except NotEnoughInfoError:
            rhs_type = var_type
        
        try:
            if var_type == rhs_type:
                return VOID
        except TypeError:
            raise SemanticError(f'El tipo inferido es {rhs_type}, pero se '
                f'esperaba {var_type}')
        else:
            raise SemanticError(f'El tipo inferido es {rhs_type}, pero se '
                f'esperaba {var_type}')

    def execute(self, symbol_table: dict) -> str:
        val = self.rhs.evaluate(symbol_table)
        symbol_table[self.id.value].value = val

        if issubclass(type(val), Terminal):
            return f'{self.id.value} := {val.value}'
        else:
            return f'{self.id.value} := {val}'

class AssignArrayElement(AST):
    def __init__(self, arrayAccess: object, rhs: object):
        self.id = arrayAccess.id
        self.index = arrayAccess.index
        self.rhs = rhs

    def ast2str(self) -> str:
        return f'Assign({self.id}[{self.index.ast2str()}], {self.rhs.ast2str()})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id and self.index == other.index
                and self.rhs == other.rhs)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def type_check(self, symbol_table: dict):

        array_type = self.id.type_check(symbol_table)
        rhs_type = self.rhs.type_check(symbol_table)

        try:
            if rhs_type.type == array_type.type.type:
                return VOID
        except TypeError:
            raise SemanticError(f'El tipo inferido es {rhs_type.type}, pero se '
                f'esperaba {array_type.type.type}')
        else:
            raise SemanticError(f'El tipo inferido es {rhs_type.type}, pero se '
                f'esperaba {array_type.type.type}')

    def execute(self, symbol_table: dict) -> str:        
        
        # Evaluar el indice y lado derecho
        index = self.index.evaluate(symbol_table)        
        val = self.rhs.evaluate(symbol_table)

        try:
            symbol_table[self.id.value].value[index.value].value = val.value
        except IndexError:
            raise RuntimeError(f'El indice {index.value} no está dentro del rango '
                f'de la variable {self.id.value}')
        except TypeError:
            raise RuntimeError(f'Se esperaba un índice entero, pero se '
                f'obtuvo {index.value}')

        return f'{self.id.value}[{index.value}] := {val.value}'


# -------- AGRUPACIONES --------
class Parentheses(AST):
    def __init__(self, expr: object):
        self.expr = expr

    def __str__(self) -> str:
        return f'({self.expr})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.expr == other.expr
               
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def type_check(self, symbol_table: dict):
        return self.expr.type_check(symbol_table)

    def evaluate(self, symbol_table: dict):
        return self.expr.evaluate(symbol_table)

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
        return f'[{self.list}]'

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

    def evaluate(self, symbol_table: dict):
        # Se evaluan todas las expresiones dentro del arreglo
        evaluated_list = []
        for expr in self:
            evaluated_list.append(expr.evaluate(symbol_table))
        # Se retorna un arreglo cuya lista es la lista de expresiones
        # evaluadas
        
        # Se retorna un arreglo con su lista de elementos evaluada        
        return Array(ElemList(None).__debug_Init__(evaluated_list))
        
class ArrayAccess(AST):
    def __init__(self, id: object, _index:object) -> None:
        self.id = id
        self.index = _index

    def __str__(self) -> str:
        return f'{self.id}[{self.index}]'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (self.id == other.id
                and self.index == other.index)
        else:
            raise TypeError(f'{type(self).__name__} is not {type(other).__name__}')

    def type_check(self, symbol_table: dict):
        array_type = self.id.type_check(symbol_table)
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
            SemanticError(f'El tipo inferido del índice es '
                f'{index_type.type}, pero se esperaba num')
        else:
            raise SemanticError(f'El tipo inferido del índice es '
                f'{index_type.type}, pero se esperaba num')

    def evaluate(self, symbol_table: dict):
        # Evaluar el indice
        index = self.index.evaluate(symbol_table)        

        try:
            return symbol_table[self.id.value].value[index.value].value
        except IndexError:
            raise StkRuntimeError(f'El indice {index.value} no está dentro del rango '
                f'de la variable {self.id.value}')
        except TypeError:
            raise StkRuntimeError(f'Se esperaba un índice entero, pero se '
                f'obtuvo {index.value}')

class Function(AST):
    def __init__(self, _id:object, _args:object) -> None:
        self.id = _id
        self.args = _args

    def __str__(self) -> str:
        return f'{self.id}({self.args})'

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
                except NotEnoughInfoError:
                    # Inferencia de tipos sobre arreglo vacío
                    if isinstance(expected_arg_type, TypeArray):
                        pass
        else:
            if len(self.args) != 0:
                raise SemanticError(f'La función "{self.id.value}" esperaba '
                    f'0 argumentos, pero se recibieron {len(self.args)}')

        return symbol_table[self.id.value].type

    def evaluate(self, symbol_table: dict):
        args = [arg.evaluate(symbol_table) for arg in self.args]
        f = symbol_table[self.id.value].value.callable
        
        return f(*args)

class ElemList(AST):
    def __init__(self, el: object):
        self.elements = [] if el is None else [el]

    def append(self, el:object):
        return self.elements.insert(0, el)

    def __str__(self) -> str:
        return f'{", ".join([str(el) for el in self])}'

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

# Diccionarios de operadores

stk_and = lambda p, q: p and q
stk_or = lambda p, q: p or q
stk_not = lambda p: Boolean(not p)
stk_eq = lambda p, q: Boolean(p == q)
stk_neq = lambda p, q: Boolean(p != q)
BINARY_OP = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '^': operator.pow,
    '%': operator.mod,
    '/': operator.truediv,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
    '=': stk_eq,
    '<>': stk_neq,
    '&&': stk_and,
    '||': stk_or
}
UNARY_OP = {
    '+': operator.pos,
    '-': operator.neg,
    '!': stk_not
}
PRELOADED_FUNCTIONS = set(['uniform', 'floor', 'length', 'sum', 'avg', 'pi', 'now'])