"""Modulo de pruebas para la precedencia de los operadores de las reglas definidas en grammar.py"""


import os, sys, pytest


sys.path.insert(1, os.path.abspath('.'))

import ply.yacc as yacc
from tokenrules import tokens
from VM import StokhosVM as SVM
import grammar
from AST import *
# Build the parser
parser = yacc.yacc(debug=True, module=grammar)
vm = SVM()

NUM_BIN_OPS = ['^', '+', '-', '*', '%', '/']
BOOL_BIN_OPS = ['&&', '||']
COMPARISONS = ['<', '<=', '>', '>=', '=', '<>']
BOOL_UN_OPS = ['!']
NUM_UN_OPS = ['+', '-']
VAR_TYPE = ['bool', 'num']
BIN_OPS = NUM_BIN_OPS + BOOL_BIN_OPS

# ---------------- Casos de prueba: Operaciones Binarias Numericas y Comparaciones -------------
test_cases, test_sol = [], []

# Asignaciones con expresiones
test_cases.extend(list((f"x := {plus_or_minus_unary}2{plus_or_minus}3 {comparison} 2{prod_div_pow}{plus_or_minus_unary} 5;" for plus_or_minus_unary in NUM_UN_OPS for plus_or_minus in NUM_UN_OPS for comparison in COMPARISONS for prod_div_pow in ["^", "*", "/"])))
test_sol.extend(list((Assign(Id("x"), Comparison(comparison, BinOp(plus_or_minus, UnOp(plus_or_minus_unary, Number(2)), Number(3)), BinOp(prod_div_pow, Number(2), UnOp(plus_or_minus_unary, Number(5))) )) for plus_or_minus_unary in NUM_UN_OPS for plus_or_minus in NUM_UN_OPS for comparison in COMPARISONS for prod_div_pow in ["^", "*", "/"])))

# Definiciones con expresiones
test_cases.extend(list((f"{varType} x := {plus_or_minus_unary}2{plus_or_minus}3 {comparison} 2{prod_div_pow}{plus_or_minus_unary} 5;" for plus_or_minus_unary in NUM_UN_OPS for plus_or_minus in NUM_UN_OPS for comparison in COMPARISONS for prod_div_pow in ["^", "*", "/"] for varType in VAR_TYPE)))
test_sol.extend(list((SymDef(Type(varType), Id("x"), Comparison(comparison, BinOp(plus_or_minus, UnOp(plus_or_minus_unary, Number(2)), Number(3)), BinOp(prod_div_pow, Number(2), UnOp(plus_or_minus_unary, Number(5))) )) for plus_or_minus_unary in NUM_UN_OPS for plus_or_minus in NUM_UN_OPS for comparison in COMPARISONS for prod_div_pow in ["^", "*", "/"] for varType in VAR_TYPE)))

# Asignaciones de arreglos
test_cases.extend(list(( f'array := [2 {binNumOp} {unOp}3, z {comparison} false {bool_bin_op} x, h[2 {binNumOp} {unOp}3]];' for binNumOp in NUM_BIN_OPS for unOp in NUM_UN_OPS for comparison in COMPARISONS for bool_bin_op in BOOL_BIN_OPS )))
test_sol.extend(list((AssignArray(Id('array'), ElemList(None).__debug_Init__([BinOp(binNumOp, Number(2), UnOp(unOp, Number(3))), BinOp (bool_bin_op, Comparison(comparison, Id('z'), Boolean('false')), Id('x') ), ArrayAccess(Id('h'),BinOp(binNumOp, Number(2), UnOp(unOp, Number(3))) )])) for binNumOp in NUM_BIN_OPS for unOp in NUM_UN_OPS for comparison in COMPARISONS for bool_bin_op in BOOL_BIN_OPS)))

# Definiciones de arreglos
# Asignaciones de arreglos
test_cases.extend(list((f'[{arr_type}] array := [2 {binNumOp} {unOp}3, z {comparison} false {bool_bin_op} x, h[2 {binNumOp} {unOp}3]];' for binNumOp in NUM_BIN_OPS for unOp in NUM_UN_OPS for comparison in COMPARISONS for bool_bin_op in BOOL_BIN_OPS for arr_type in VAR_TYPE )))
test_sol.extend(list((SymDef(Type(TypeArray(Type(arr_type))), Id('array'), ElemList(None).__debug_Init__([BinOp(binNumOp, Number(2), UnOp(unOp, Number(3))), BinOp (bool_bin_op, Comparison(comparison, Id('z'), Boolean('false')), Id('x') ), ArrayAccess(Id('h'),BinOp(binNumOp, Number(2), UnOp(unOp, Number(3))) )])) for binNumOp in NUM_BIN_OPS for unOp in NUM_UN_OPS for comparison in COMPARISONS for bool_bin_op in BOOL_BIN_OPS for arr_type in VAR_TYPE)))



# ------------ Ejecucion de pruebas ---------------
cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_individual_rules(test_case:str, test_sol:object):
    assert parser.parse(test_case) == test_sol