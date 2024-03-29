"""Evaluadores para subclases del AST de Stókhos.
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
from typing import Union

from ..AST import *
from ..symtable import SymFunction, SymTable
from .helpers import ASTNodeVisitor

# Diccionarios de operadores
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
    '=': lambda p, q: Boolean(p.value == q.value),
    '<>': lambda p, q: Boolean(p.value!= q.value),
    '&&': lambda p, q: Boolean(p.value and q.value),
    '||': lambda p, q: Boolean(p.value or q.value),
}
UNARY_OP = {
    '+': operator.pos,
    '-': operator.neg,
    '!': lambda p: Boolean(not p.value)
}

class ASTEvaluator(ASTNodeVisitor):
    def __init__(self, sym_table: SymTable):
        self.sym_table = sym_table

    # ---- CASOS BASE (TERMINALES) ----
    def visit_Number(self, ast: Number) -> Number:
        return ast
    
    def visit_Boolean(self, ast: Boolean) -> Boolean:
        return ast

    def visit_Quoted(self, ast: Quoted) -> AST:
        return ast.expr

    # ---- NODOS RECURSIVOS ----
    def visit_Id(self, ast: Id) -> AST:
        lookup = self.sym_table.lookup(ast.value)

        if isinstance(lookup, SymFunction):
            raise StkRuntimeError('No se puede evaluar una función como una '
                'expresión')

        # Implementación de memoización para Ids
        if self.sym_table.cycle != lookup.last_cycle:
            val = self.visit(lookup.value)

            lookup.cache = val
            lookup.last_cycle = self.sym_table.cycle
            return val

        if isinstance(lookup.cache, list):
            for i in range(0, len(lookup.cache)):
                if lookup.cache[i] is None:
                    lookup.cache[i] = self.visit(lookup.value[i])
        return lookup.cache

    # ---- OPERADORES ----
    def visit_BinOp(self, ast: BinOp) -> AST:
        try:
            res = BINARY_OP[ast.op](
                self.visit(ast.lhs),
                self.visit(ast.rhs)
            )

            if isinstance(res.value, complex):
                raise StkRuntimeError(f'No se puede realizar aritmética con '
                    f'números complejos')
            return res
        except ZeroDivisionError:
            raise StkRuntimeError(f'División por cero en la expresión {ast}')

    def visit_Comparison(self, ast: Comparison) -> AST:
        return BINARY_OP[ast.op](
            self.visit(ast.lhs),
            self.visit(ast.rhs)
        )

    def visit_UnOp(self, ast: UnOp) -> AST:
        return UNARY_OP[ast.op](self.visit(ast.term))

    # ---- OTRAS EXPRESIONES ----
    def visit_Array(self, ast: Array) -> AST:
        # Se evaluan todas las expresiones dentro del arreglo
        evaluated_list = []
        for expr in ast:
            evaluated_list.append(self.visit(expr))

        # Se retorna un arreglo con su lista de elementos evaluada        
        return Array(evaluated_list)

    def visit_ArrayAccess(self, ast: ArrayAccess) -> AST:
        # Evaluar el indice
        index = self.visit(ast.index)
        if index.value < 0:
            raise StkRuntimeError(f'Se esperaba un índice entero no negativo, pero se '
                f'obtuvo {index.value}')

        # Tratar de convertir a entero
        index_val = int(index.value) if index.value % 1 == 0 else index.value

        try:
            if not isinstance(ast.expr, Id):
                return self.visit(ast.expr)[index_val]

            # Si es una Id, se busca en la tabla de símbolos
            lookup = self.sym_table.lookup(ast.expr.value)

            # Implementación de memoización para Arrays
            # CASO DEGENERADO!!
            if not isinstance(lookup.value, Array):
                if self.sym_table.cycle != lookup.last_cycle:
                    lookup.cache = self.visit(lookup.value)
                    lookup.last_cycle = self.sym_table.cycle
                return lookup.cache[index_val]

            # Otros casos
            if (self.sym_table.cycle != lookup.last_cycle
                or lookup.cache is None 
                or lookup.cache[index_val] is None
            ):
                val = self.visit(lookup.value[index_val])

                lookup.cache[index_val] = val
                lookup.last_cycle = self.sym_table.cycle

            return lookup.cache[index_val]
        except (IndexError, AttributeError):
            raise StkRuntimeError(f'El indice {index.value} no está dentro del rango '
                f'de la expresión {ast.expr}')
        except TypeError:
            raise StkRuntimeError(f'Se esperaba un índice entero no negativo, pero se '
                f'obtuvo {index.value}')

    def visit_FunctionCall(self, ast: FunctionCall):
        # Tratamiento de funciones especiales
        if ast.id.value in SPECIAL_FUNCTION_HANDLERS:
            return SPECIAL_FUNCTION_HANDLERS[ast.id.value](self, *ast.args)

        args = [self.visit(arg) for arg in ast.args]
        f = self.sym_table.get_value(ast.id.value)

        return f(*args)
                        
    def generic_visit(self, ast: AST):
        raise Exception(f'Evaluador de {type(ast).__name__} no implementado')

    def evaluate(self, ast: AST) -> AST:
        return self.visit(ast)

# -------- FUNCIONES ESPECIALES --------

# Son funciones que reciben el evaluador y pasan los argumentos
# de la forma requerida, dándoles un tratamiento especial
def stk_reset(evaluator: ASTEvaluator):
    '''Resetea la tabla de símbolos e incrementa en uno el ciclo de computo.
    
    Args:
        vm: Instancia de la tabla de símbolos a resetear.
    '''
    evaluator.sym_table.clear()
    stk_tick(evaluator)
    return Boolean(True)

def stk_if(evaluator: ASTEvaluator,  condicion: AST, exprT: AST, exprF: AST) -> Union[Boolean, Number, Array]:
    '''Retorna el resultado de evaluar exprT si se satisface la condición,
    o exprF si no se satisface. Usa evaluación estricta
    
    Args:
        evaluator: Instancia de evaluador de Stokhos.
        condicion: La condición a evaluar.
        exprT: Expresión a evaluarse si la condición se satisface.
        exprF: Expresión a evaluarse si la condición no se satisface.
    '''
    if evaluator.evaluate(condicion):
        return evaluator.evaluate(exprT)
    else:
        return evaluator.evaluate(exprF)

def stk_type(evaluator: ASTEvaluator,  expr: AST) -> Type:
    '''Retorna el tipo del AST pasado como parámetro, no lo evalua. Usa las
    anotaciones del AST (el árbol ya se encuentra anotado tras la etapa de
    validación estática)
    
    Args:
        expr: Expresión a obtener el tipo.
    '''
    if isinstance(expr, Id):
        if evaluator.sym_table.is_function(expr.value):
            return Type('function')
        else:
            _type = evaluator.sym_table.get_type(expr.value)
    else:
        _type = expr.type

    if _type is ANY_ARRAY:
        raise StkRuntimeError('No hay suficiente información para inferir el '
            'tipo del arreglo')
    
    return _type

def stk_ltype(evaluator: ASTEvaluator,  expr: AST) -> Type:
    '''Retorna el tipo del AST pasado como parámetro, no lo evalua. Usa las
    anotaciones del AST (el árbol ya se encuentra anotado tras la etapa de
    validación estática)
    
    Args:
        expr: Expresión a obtener el ltype.
    '''
    if not isinstance(expr, (Id, ArrayAccess)):
        raise StkRuntimeError(f'La expresión "{expr}" no tiene LVALUE')
    elif isinstance(expr, Id):
        # En Stókhos no se puede asignar a una función
        if evaluator.sym_table.is_function(expr.value):
            raise StkRuntimeError(f'La expresión "{expr}" no tiene LVALUE')
    elif isinstance(expr, ArrayAccess) and not isinstance(expr.expr, Id):
        raise StkRuntimeError(f'La expresión "{expr}" no tiene LVALUE')

    return expr.type

def stk_tick(evaluator: ASTEvaluator) -> Number:
    '''Incrementa el ciclo de cómputo en 1 y retorna su nuevo valor.'''
    return evaluator.sym_table.increment_cycle()

def stk_formula(evaluator: ASTEvaluator,  expr: AST) -> AST:
    '''Retorna el CVALUE de la expresión pasada como argumento, si lo tiene.
    En caso de no tener LVALUE, lanza error.
    
    Args:
        expr: Expresión a obtener el cvalue.
    '''

    # Se chequea que la expresión tenga ltype, si no, ltype lanzará el Error
    stk_ltype(evaluator, expr)
    _id = expr.value if isinstance(expr, Id) else expr.expr.value

    lookup = evaluator.sym_table.lookup(_id).value
    if isinstance(expr, ArrayAccess):
        try:
            return lookup[expr.index.value]
        except:
            raise StkRuntimeError('Acceso a arreglo inválido')

    return lookup

def stk_array(evaluator: ASTEvaluator,  size: AST, expr: AST) -> Array:
    '''Retorna un arreglo de tamaño size dnode cada elemento está inicializado
    con el resultado de evaluar expr.
    
    Args:
        size: Tamaño del arreglo a retornar
        expr: Expresión a evaluar para obtener cada elemento del arreglo.
    '''
    n = evaluator.evaluate(size)

    if n.value < 0 or n.value % 1 != 0:
        raise StkRuntimeError(f'Se esperaba como tamaño un entero no negativo, pero se '
            f'obtuvo {n.value}')

    arr = []
    n_val = int(n.value)
    init = evaluator.evaluate(expr)

    for i in range(n_val):
        arr.append(evaluator.evaluate(init))
    return Array(arr)

def stk_histogram(evaluator: ASTEvaluator, x: AST,
    NS: AST, NB: AST, LB: AST, UB: AST) -> Array:
    lower_bound = evaluator.evaluate(LB).value
    upper_bound = evaluator.evaluate(UB).value
    n_samples = evaluator.evaluate(NS).value
    n_buckets = evaluator.evaluate(NB).value

    if upper_bound < lower_bound:
        raise StkRuntimeError('El límite superior de histogram es menor al '
            'límite inferior')

    if n_buckets < 0 or n_buckets % 1 != 0:
        raise StkRuntimeError(f'Se esperaba como numero de buckets un entero no'
        f' negativo, pero se obtuvo {n_buckets}')

    if n_samples < 0 or n_samples % 1 != 0:
        raise StkRuntimeError(f'Se esperaba como numero de samples un entero no'
        f' negativo, pero se obtuvo {n_samples}')
        
    n_buckets, n_samples = int(n_buckets), int(n_samples)
    
    histogram = [Number(0) for i in range(n_buckets + 2)]

    delta = (upper_bound - lower_bound) / n_buckets
    sample_eval = evaluator.evaluate(x)
    for i in range(n_samples):
        # Llama a tick por cada iteración
        stk_tick(evaluator)

        try:
            sample = evaluator.evaluate(sample_eval).value
        except:
            # Si hay un error en un sample se salta
            continue

        # Calcula el bucket correspondiente
        # (Fórmula derivada manualmente)
        # bucket = floor(((sample - lower_bound) / delta) + 1)
        if sample < lower_bound:
            histogram[0] += Number(1)
        elif sample >= upper_bound:
            histogram[-1] += Number(1)
        else:
            bucket = floor((sample - lower_bound) / delta + 1)
            histogram[bucket] += Number(1)

    return Array(histogram)


# Diccionario de handlers de funciones especiales
SPECIAL_FUNCTION_HANDLERS = {
    'type': stk_type,
    'ltype': stk_ltype,
    'reset': stk_reset,
    'if': stk_if,
    'tick': stk_tick,
    'formula': stk_formula,
    'array': stk_array,
    'histogram': stk_histogram,
}
