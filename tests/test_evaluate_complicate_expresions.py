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

# Operaciones Numericas
test_cases.append('----+----+-----+-----+-----+---------1')
test_sol.append(Number(1))

test_cases.append('--------+-++--------+++++++----------------1')
test_sol.append(Number(-1))

test_cases.append('-2*6*(-2^3)')
test_sol.append(Number(96))

# Raiz cuadrada implicita!
test_cases.append('(100/10*5 + 14)^(1/2)') 
test_sol.append(Number(8))

test_cases.append('42%(4+1) * 7') 
test_sol.append(Number(14))

# Indeterminaciones numericas, esto no tiene sentido aqui pero lo dejo para recordar que esta explotando el programa
test_cases.append('1/0') 
test_sol.append('') 

test_cases.append('0^0') 
test_sol.append('') 

# Operaciones booleanas
test_cases.append('!!!!!!((!!!!true || !!false) && !false && !!!!!!!!!!!false)') 
test_sol.append(Boolean(True))

test_cases.append('false || false || false || false || false || false ||false || !false') 
test_sol.append(Boolean(True))

test_cases.append('false && true && true || false') 
test_sol.append(Boolean(False))

# Combinaciones
test_cases.append('2+1 >= 2 && -3-2^2 <= 3') 
test_sol.append(Boolean(True))

test_cases.append('2*10 > 2/10^5 && 3+-8^2 < 3') 
test_sol.append(Boolean(True))

test_cases.append('2*10/2+10^3-500 <> 2*10/2+10^3-500+1 || 2 < 1 || 5 *2 < 5+5') 
test_sol.append(Boolean(True))

test_cases.append('2*10/2+100^30-500 = 2*10/2+100^30-500+1000 || false || 1 <> 1') 
test_sol.append(Boolean(True))

test_cases.append('2*10/2+100^30-500 = 2*10/2+100^30-500 || false || 1 <> 1') 
test_sol.append(Boolean(True))

test_cases.append('4 = 4 = true') 
test_sol.append(Boolean(True))

test_cases.append('(4 = 4) = true') 
test_sol.append(Boolean(True))

test_cases.append('(4 <> 4) <> true') 
test_sol.append(Boolean(True))

test_cases.append('4 <> 4 <> true') 
test_sol.append(Boolean(True))

test_cases.append('4 <> 5 && true || false') 
test_sol.append(Boolean(True))


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