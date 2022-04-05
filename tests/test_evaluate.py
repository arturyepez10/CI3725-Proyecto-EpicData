"""Modulo de pruebas para el chequeo de tipos"""
import os
import sys
import pytest

sys.path.insert(1, os.path.abspath('.'))
import ply.yacc as yacc
import stokhos.grammar as grammar
from stokhos.AST import *
from stokhos.VM import StokhosVM as SVM
import copy
NUM_UN_OPS = ['+', '-']
BOOL_UN_OPS = ['!']
NUM_BIN_OPS = ['^', '+', '-', '*', '%', '/']
BOOL_BIN_OPS = ['&&', '||']
COMPARISONS = ['<', '<=', '>', '>=', '=', '<>']
ALL_BIN_OPS = NUM_BIN_OPS + BOOL_BIN_OPS + COMPARISONS

# -------------- Pruebas de errores evaluacion ----------
test_cases, test_sol = [], []
VM = SVM()

test_cases.append('2+2')
test_sol.append(Number(4))

test_cases.append('2-2')
test_sol.append(Number(0))

test_cases.append('5*2')
test_sol.append(Number(10))

test_cases.append('10/2')
test_sol.append(Number(5))

test_cases.append('5^2')
test_sol.append(Number(25))

test_cases.append('5%2')
test_sol.append(Number(1))

test_cases.append('-5')
test_sol.append(Number(-5))

test_cases.append('+5')
test_sol.append(Number(5))

test_cases.append('!false')
test_sol.append(Boolean(True))

test_cases.append('false && true')
test_sol.append(Boolean(False))

test_cases.append('false || true')
test_sol.append(Boolean(True))

test_cases.append('false = true')
test_sol.append(Boolean(False))

test_cases.append('false <> true')
test_sol.append(Boolean(True))

test_cases.append('-1 <> -1')
test_sol.append(Boolean(False))

test_cases.append('-1 = -1')
test_sol.append(Boolean(True))

test_cases.append('-1 > 1')
test_sol.append(Boolean(False))

test_cases.append('1 < 2')
test_sol.append(Boolean(True))

test_cases.append('1 <= 1')
test_sol.append(Boolean(True))

test_cases.append('1 >= 1')
test_sol.append(Boolean(True))

# Funciones:
test_cases.append('pi()')
test_sol.append(Number(3.141592653589793))

test_cases.append('length([1,2,-3])')
test_sol.append(Number(3))

test_cases.append('length([])')
test_sol.append(Number(0))

test_cases.append('floor(2.3)')
test_sol.append(Number(2))

test_cases.append('sum([1,2,3,-3])')
test_sol.append(Number(3))

test_cases.append('avg([1,2,3,-3])')
test_sol.append(Number(0.75))

cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_evaluate(test_case:str, test_sol:object):
    ast = VM.parse(test_case)
    if isinstance(ast, Error):
        # No se construye el AST
        assert False
    
    val = VM.validate(ast)
    if isinstance(val, Error):
        # AST invalido
        assert False

    res = VM.eval(ast)
    
    assert res == test_sol
