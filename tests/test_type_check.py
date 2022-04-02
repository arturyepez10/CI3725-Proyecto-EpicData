
import os
import sys
from ast import Num

import pytest


sys.path.insert(1, os.path.abspath('.'))

import ply.yacc as yacc
import stokhos.grammar as grammar
from stokhos.AST import *
from stokhos.tokenrules import tokens

NUM_BIN_OPS = ['^', '+', '-', '*', '%', '/']
BOOL_BIN_OPS = ['&&', '||']
COMPARISONS = ['<', '<=', '>', '>=', '=', '<>']

parser = yacc.yacc(debug=True, module=grammar)
test_cases, test_sol = [], []

test_cases.append('1')
test_sol.append(Type(PrimitiveType('num')))

test_cases.append('true')
test_sol.append(Type(PrimitiveType('bool')))

# 'unNumero' esta en la tabla de simbolos como num
test_cases.append('unNumero')
test_sol.append(Type(PrimitiveType('num')))

# 'unBooleano' esta en la tabla de simbolos como bool
test_cases.append('unBooleano')
test_sol.append(Type(PrimitiveType('bool')))

# ----- Operaciones Unarias -------
test_cases.append('+1')
test_sol.append(Type(PrimitiveType('num')))

test_cases.append('-1')
test_sol.append(Type(PrimitiveType('num')))

test_cases.append('!true')
test_sol.append(Type(PrimitiveType('bool')))

test_cases.append('!false')
test_sol.append(Type(PrimitiveType('bool')))

# 'unNumero' esta en la tabla de simbolos como num
test_cases.append('-unNumero')
test_sol.append(Type(PrimitiveType('num')))

# 'unBooleano' esta en la tabla de simbolos como bool
test_cases.append('!unBooleano')
test_sol.append(Type(PrimitiveType('bool')))

# ------------- Operaciones binarias --------
test_cases.extend([f'3 {numOp} 5' for numOp in NUM_BIN_OPS])
test_sol.extend([Type(PrimitiveType('num')) for i in range(len(NUM_BIN_OPS))])

test_cases.extend([f'true {boolOp} false' for boolOp in BOOL_BIN_OPS])
test_sol.extend([Type(PrimitiveType('bool')) for i in range(len(BOOL_BIN_OPS))])

# -------------- Comparaciones ------------
test_cases.extend([f'3 {comparison} unNumero' for comparison in COMPARISONS])
test_sol.extend([Type(PrimitiveType('bool')) for i in range(len(COMPARISONS))])


# ------------ Ejecucion de pruebas ---------------
cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_type_check(test_case:str, test_sol:object):
    symbols = {
        'unNumero': Type(PrimitiveType('num')),
        'unBooleano': Type(PrimitiveType('bool')),
    }    
    assert parser.parse(test_case).type_check(symbols) == test_sol
