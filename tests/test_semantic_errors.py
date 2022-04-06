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
# -------------- Pruebas de errores semanticos ----------
test_cases, test_sol = [], []
VM = SVM()

# Operaciones binarias y unarias con errores en semantica
test_cases.extend([f'2 {binOp} true' for binOp in ALL_BIN_OPS])
test_cases.extend([f'false {binOp} 3.6' for binOp in ALL_BIN_OPS])
test_cases.extend([f'{NumUnOp} false ' for NumUnOp in NUM_UN_OPS])
test_cases.extend([f'{boolUnOp} 2 ' for boolUnOp in BOOL_UN_OPS])

# Lo mismo que antes con parentesis
test_cases.extend([f'(2) {binOp} (true)' for binOp in ALL_BIN_OPS])
test_cases.extend([f'false {binOp} (((3.6)))' for binOp in ALL_BIN_OPS])
test_cases.extend([f'{NumUnOp} (false) ' for NumUnOp in NUM_UN_OPS])
test_cases.extend([f'{boolUnOp} ((2)) ' for boolUnOp in BOOL_UN_OPS])


# Prueba sobre definiciones
test_cases.append(f'num x := false;')
test_cases.append(f'num x := [1,2,3];')
test_cases.append(f'num x := [true, false, true];')

test_cases.append(f'bool x := 2;')
test_cases.append(f'bool x := [1,2,3];')
test_cases.append(f'bool x := [true, false, true];')

test_cases.append(f'[num] x := 2;')
test_cases.append(f'[num] x := true;')
test_cases.append(f'[num] x := [true, false, true];')

test_cases.append(f'[bool] x := 2;')
test_cases.append(f'[bool] x := true;')
test_cases.append(f'[bool] x := [3, -1, 4];')

# Faltan las asignaciones

# llamadas a funciones en operaciones con problemas de tipo (y que no explotan
# la a VM
test_cases.append(f'uniform() - true')
test_cases.append(f'pi(uniform())')
test_cases.append(f'length([1,2,3])^[2,3]') 
test_cases.append(f'sum([1,2,3])+true')
test_cases.append(f'avg([1,2,3]) * 3 + [2]')
# Cuando se ejecutan estas pruebas de forma individual, funcionan. Pero al hacerlo,
# global (con solo "pytest") fallan. El programa no falla con estos casos

cases = list(zip(test_cases, test_cases))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_type_check_semantic_errors(test_case:str, test_sol:object):
    
    try:
        out = VM.validate(VM.parse(test_case))
    except SemanticError: 
        assert True        
    else:
        if not isinstance(out, Error):
            assert False 