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

    def visit_Id(self, ast: Id) -> AST:
        return self.sym_table.get_value(ast.value)

    # ---- NODOS RECURSIVOS ----

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
    def visit_Quoted(self, ast: Quoted) -> AST:
        return self.visit(ast.expr)

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
            return self.sym_table.get_value(ast.id.value)[index.value]
        except IndexError:
            raise StkRuntimeError(f'El indice {index.value} no está dentro del rango '
                f'de la variable {self.id.value}')
        except TypeError:
            raise StkRuntimeError(f'Se esperaba un índice entero, pero se '
                f'obtuvo {index.value}')

    def visit_Function(self, ast: Function):
        args = [self.visit(arg) for arg in ast.args]
        f = self.sym_table.get_value(ast.id.value)
        # print(f'\n\n\n\n\n\n\n\n\n\nFUNCION F: {f.__name__}\n\n\n\n\n\n\n\n\n\n')
        return f(*args)
                        
    def generic_visit(self, ast: AST):
        raise Exception(f'Evaluador de {type(ast).__name__} no implementado')

    def evaluate(self, ast: AST) -> AST:
        return self.visit(ast)