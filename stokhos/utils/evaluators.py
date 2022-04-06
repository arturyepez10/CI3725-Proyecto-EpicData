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
from typing import Union

from ..AST import *
from ..symtable import SymTable
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
    '=': lambda p, q: Boolean(p == q),
    '<>': lambda p, q: Boolean(p != q),
    '&&': lambda p, q: p and q,
    '||': lambda p, q: p or q
}
UNARY_OP = {
    '+': operator.pos,
    '-': operator.neg,
    '!': lambda p: Boolean(not p)
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
        lookup = self.sym_table.get_value(ast.value)
        
        # Tiene que hacerse así por la existencia de expresiones acotadas
        return self.visit(lookup)

    # ---- OPERADORES ----
    def visit_BinOp(self, ast: BinOp) -> AST:
        return BINARY_OP[ast.op](
            self.visit(ast.lhs_term),
            self.visit(ast.rhs_term)
        )

    def visit_Comparison(self, ast: Comparison) -> AST:
        return BINARY_OP[ast.op](
            self.visit(ast.lhs_term),
            self.visit(ast.rhs_term)
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

        try:
            return self.visit(ast.id)[index.value]
        except (IndexError, AttributeError):
            raise StkRuntimeError(f'El indice {index.value} no está dentro del rango '
                f'de la expresión {ast.id}')
        except TypeError:
            raise StkRuntimeError(f'Se esperaba un índice entero, pero se '
                f'obtuvo {index.value}')

    def visit_Function(self, ast: Function):
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

# Funciones especiales
# Son funciones que reciben el evaluador y pasan los argumentos
# de la forma requerida, dándoles un tratamiento especial
def stk_reset(evaluator: ASTEvaluator):
    '''Resetea la tabla de símbolos.
    
    Args:
        vm: Instancia de la tabla de símbolos a resetear.
    '''
    evaluator.sym_table.clear()
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
            return Type(PrimitiveType('function'))
        else:
            _type = evaluator.sym_table.get_type(expr.value)
    else:
        _type = expr.type

    if _type is VOID_ARRAY:
        raise SemanticError('No hay suficiente información para inferir el '
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
        raise SemanticError(f"La expresión '{expr}' no tiene LVALUE")
    elif isinstance(expr, Id):
        # En Stókhos no se puede asignar a una función
        # Debería ?
        if evaluator.sym_table.is_function(expr.value):
            raise SemanticError(f"La expresión '{expr}' no tiene LVALUE")

    return expr.type

# Diccionario de handlers de funciones especiales
SPECIAL_FUNCTION_HANDLERS = {
    'type': stk_type,
    'ltype': stk_ltype,
    'reset': stk_reset,
    'if': stk_if,
}
