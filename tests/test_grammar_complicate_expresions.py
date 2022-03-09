"""Modulo de pruebas para la precedencia de los operadores de las reglas definidas en grammar.py"""

from ast import Num
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

BIN_OPS = NUM_BIN_OPS + BOOL_BIN_OPS

# ---------------- Casos de prueba: Operaciones Binarias Numericas y Comparaciones -------------
test_cases, test_sol = [], []
# Definiciones y asignaciones con expresiones

test_cases.extend(list((f"x := {plus_or_minus_unary}2{plus_or_minus}3 {comparison} 2{prod_div_pow}{plus_or_minus_unary} 5;" for plus_or_minus_unary in NUM_UN_OPS for plus_or_minus in NUM_UN_OPS for comparison in COMPARISONS for prod_div_pow in ["^", "*", "/"])))
test_sol.extend(list((Assign(Id("x"), Comparison(comparison, NumberBinOp(plus_or_minus, NumberUnOp(plus_or_minus_unary, Number(2)), Number(3)), NumberBinOp(prod_div_pow, Number(2), NumberUnOp(plus_or_minus_unary, Number(5))) )) for plus_or_minus_unary in NUM_UN_OPS for plus_or_minus in NUM_UN_OPS for comparison in COMPARISONS for prod_div_pow in ["^", "*", "/"]         )))

# ------------ Ejecucion de pruebas ---------------
cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_individual_rules(test_case:str, test_sol:object):
    assert parser.parse(test_case) == test_sol