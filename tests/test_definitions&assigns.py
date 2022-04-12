"""Modulo de pruebas para el chequeo de tipos"""
import os
import sys
import pytest

sys.path.insert(1, os.path.abspath('.'))


from stokhos.AST import *
from stokhos.VM import StokhosVM as SVM

NUM_UN_OPS = ['+', '-']
BOOL_UN_OPS = ['!']
NUM_BIN_OPS = ['^', '+', '-', '*', '%', '/']
BOOL_BIN_OPS = ['&&', '||']
COMPARISONS = ['<', '<=', '>', '>=', '=', '<>']
ALL_BIN_OPS = NUM_BIN_OPS + BOOL_BIN_OPS + COMPARISONS

# -------------- Pruebas de asignaciones ----------
test_cases, test_sol = [], []
VM = SVM()

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