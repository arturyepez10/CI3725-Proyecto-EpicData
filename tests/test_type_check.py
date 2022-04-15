"""Modulo de pruebas para el chequeo de tipos"""
import os
import sys
import pytest

sys.path.insert(1, os.path.abspath('.'))
import ply.yacc as yacc
import stokhos.grammar as grammar
from stokhos.AST import *
from stokhos.utils.validators import ASTValidator
from stokhos.symtable import SymTable, SymVar

NUM_UN_OPS = ['+', '-']
BOOL_UN_OPS = ['!']
NUM_BIN_OPS = ['^', '+', '-', '*', '%', '/']
BOOL_BIN_OPS = ['&&', '||']
COMPARISONS = ['<', '<=', '>', '>=', '=', '<>']
ALL_BIN_OPS = NUM_BIN_OPS + BOOL_BIN_OPS + COMPARISONS

test_cases, test_sol = [], []

test_cases.append('1')
test_sol.append(NUM)

test_cases.append('true')
test_sol.append(BOOL)

# 'unNumero' esta en la tabla de simbolos como num
test_cases.append('unNumero')
test_sol.append(NUM)

# 'unBooleano' esta en la tabla de simbolos como bool
test_cases.append('unBooleano')
test_sol.append(BOOL)

# ----- Operaciones Unarias -------
test_cases.append('+1')
test_sol.append(NUM)

test_cases.append('-1')
test_sol.append(NUM)

test_cases.append('!true')
test_sol.append(BOOL)

test_cases.append('!false')
test_sol.append(BOOL)

# 'unNumero' esta en la tabla de simbolos como num
test_cases.append('-unNumero')
test_sol.append(NUM)

# 'unBooleano' esta en la tabla de simbolos como bool
test_cases.append('!unBooleano')
test_sol.append(BOOL)

# ------------- Operaciones binarias --------
test_cases.extend([f'3 {numOp} 5' for numOp in NUM_BIN_OPS])
test_sol.extend([NUM for i in range(len(NUM_BIN_OPS))])

test_cases.extend([f'true {boolOp} false' for boolOp in BOOL_BIN_OPS])
test_sol.extend([BOOL for i in range(len(BOOL_BIN_OPS))])

# -------------- Comparaciones ------------
test_cases.extend([f'3 {comparison} unNumero' for comparison in COMPARISONS])
test_sol.extend([BOOL for i in range(len(COMPARISONS))])

test_cases.extend([f'true {comparison} unBooleano' for comparison in ['<>', '=']])
test_sol.extend([BOOL for i in range(2)])

# ------------ Parentesis ---------
test_cases.extend([f'((3) {numOp} (5))' for numOp in NUM_BIN_OPS])
test_sol.extend([NUM for i in range(len(NUM_BIN_OPS))])

test_cases.extend([f'(true {boolOp} false)' for boolOp in BOOL_BIN_OPS])
test_sol.extend([BOOL for i in range(len(BOOL_BIN_OPS))])


test_cases.extend([f'3 {comparison} (unNumero)' for comparison in COMPARISONS])
test_sol.extend([BOOL for i in range(len(COMPARISONS))])

# ---------- Acotado ------------
test_cases.extend([f"''3' {numOp} '5''" for numOp in NUM_BIN_OPS])
test_sol.extend([NUM for i in range(len(NUM_BIN_OPS))])

test_cases.extend([f"'true {boolOp} false'" for boolOp in BOOL_BIN_OPS])
test_sol.extend([BOOL for i in range(len(BOOL_BIN_OPS))])


test_cases.extend([f"3 {comparison} 'unNumero'" for comparison in COMPARISONS])
test_sol.extend([BOOL for i in range(len(COMPARISONS))])

# -----------Acceso a arreglos ----------
# En tabla de simbolos:
test_cases.append('arregloDeNumeros[2]')
test_sol.append(NUM)

test_cases.append('arregloDeBooleanos[2]')
test_sol.append(BOOL)

# Arreglos
test_cases.append('[1, 2, 3]')
test_sol.append(NUM_ARRAY)

# Arreglos
test_cases.append('[1, 2, 3][2]')
test_sol.append(NUM)

test_cases.append('[1, unNumero]')
test_sol.append(NUM_ARRAY)

# ----------- Definiciones ---------------
test_cases.append('num h := 2;')
test_sol.append(VOID)

test_cases.append('bool j := true;')
test_sol.append(VOID)

test_cases.append('[num] k := [2,3,4];')
test_sol.append(VOID)

test_cases.append('[bool] m := [true, false, true];')
test_sol.append(VOID)

# ------------ Asignaciones ----------------
test_cases.append('unNumero := 3;')
test_sol.append(VOID)

test_cases.append('unBooleano := true;')
test_sol.append(VOID)

test_cases.append('arregloDeNumeros[4] := 3;')
test_sol.append(VOID)

test_cases.append('arregloDeBooleanos[1] := false;')
test_sol.append(VOID)

test_cases.append('arregloDeNumeros := [1, 2, 5 ,1];')
test_sol.append(VOID)

test_cases.append('arregloDeBooleanos := [false, true, false];')
test_sol.append(VOID)

# ------------ Ejecucion de pruebas ---------------
# Configuración del entorno de pruebas
symbols = [
    ('x', NUM, Number(42)),
    ('y', BOOL, Boolean(True)),
    ('unNumero', NUM, Number(616)),
    ('unBooleano', BOOL, Boolean(False)),
    ('arregloDeNumeros', NUM_ARRAY, Array([Number(42)])),
    ('arregloDeBooleanos', BOOL_ARRAY, Array([Boolean(False)]))
]

symbol_table = SymTable()
for _id, _type, val in symbols:
    symbol_table.insert(_id, _type, val)

parser = yacc.yacc(debug=True, module=grammar)
validator = ASTValidator(symbol_table)

cases = list(zip(test_cases, test_sol))

@pytest.mark.parametrize("test_case,test_sol", cases)
def test_type_check(test_case:str, test_sol:object):
    
    out = validator.validate(parser.parse(test_case))
    assert out == test_sol