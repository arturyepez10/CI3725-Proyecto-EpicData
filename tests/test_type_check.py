"""Modulo de pruebas para el chequeo de tipos"""
import os
import sys
import pytest
sys.path.insert(1, os.path.abspath('.'))
import ply.yacc as yacc
import stokhos.grammar as grammar
from stokhos.AST import *

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

test_cases.extend([f'true {comparison} unBooleano' for comparison in ['<>', '=']])
test_sol.extend([Type(PrimitiveType('bool')) for i in range(2)])

# ------------ Parentesis ---------
test_cases.extend([f'((3) {numOp} (5))' for numOp in NUM_BIN_OPS])
test_sol.extend([Type(PrimitiveType('num')) for i in range(len(NUM_BIN_OPS))])

test_cases.extend([f'(true {boolOp} false)' for boolOp in BOOL_BIN_OPS])
test_sol.extend([Type(PrimitiveType('bool')) for i in range(len(BOOL_BIN_OPS))])


test_cases.extend([f'3 {comparison} (unNumero)' for comparison in COMPARISONS])
test_sol.extend([Type(PrimitiveType('bool')) for i in range(len(COMPARISONS))])

# ---------- Acotado ------------
test_cases.extend([f"''3' {numOp} '5''" for numOp in NUM_BIN_OPS])
test_sol.extend([Type(PrimitiveType('num')) for i in range(len(NUM_BIN_OPS))])

test_cases.extend([f"'true {boolOp} false'" for boolOp in BOOL_BIN_OPS])
test_sol.extend([Type(PrimitiveType('bool')) for i in range(len(BOOL_BIN_OPS))])


test_cases.extend([f"3 {comparison} 'unNumero'" for comparison in COMPARISONS])
test_sol.extend([Type(PrimitiveType('bool')) for i in range(len(COMPARISONS))])

# -----------Acceso a arreglos ----------
# En tabla de simbolos:
test_cases.append('arregloDeNumeros[2]')
test_sol.append(Type(PrimitiveType('num')))

test_cases.append('arregloDeBooleanos[2]')
test_sol.append(Type(PrimitiveType('bool')))

# Arreglos
test_cases.append('[1, 2, 3]')
test_sol.append(Type(TypeArray(PrimitiveType('num'))))

# Arreglos
test_cases.append('[1, 2, 3][2]')
test_sol.append(Type(PrimitiveType('num')))

test_cases.append('[1, unNumero]')
test_sol.append(Type(TypeArray(PrimitiveType('num'))))

# ----------- Definiciones ---------------
test_cases.append('num h := 2;')
test_sol.append(Type(PrimitiveType('void')))

test_cases.append('bool j := true;')
test_sol.append(Type(PrimitiveType('void')))

test_cases.append('[num] k := [2,3,4];')
test_sol.append(Type(PrimitiveType('void')))

test_cases.append('[bool] m := [true, false, true];')
test_sol.append(Type(PrimitiveType('void')))

# ------------ Asignaciones ----------------
test_cases.append('unNumero := 3;')
test_sol.append(Type(PrimitiveType('void')))

test_cases.append('unBooleano := true;')
test_sol.append(Type(PrimitiveType('void')))

test_cases.append('arregloDeNumeros[4] := 3;')
test_sol.append(Type(PrimitiveType('void')))

test_cases.append('arregloDeBooleanos[1] := false;')
test_sol.append(Type(PrimitiveType('void')))

test_cases.append('arregloDeNumeros := [1, 2, 5 ,1];')
test_sol.append(Type(PrimitiveType('void')))

test_cases.append('arregloDeBooleanos := [false, true, false];')
test_sol.append(Type(PrimitiveType('void')))


# ------------ Ejecucion de pruebas ---------------
cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_type_check(test_case:str, test_sol:object):
    symbols = {
        'x':
            Symbol(Type(PrimitiveType('num')), Number(42)),
        'y':
            Symbol(Type(PrimitiveType('bool')), Boolean(True)),
        'unNumero':
            Symbol(Type(PrimitiveType('num')), Number(616)),
        'unBooleano':
            Symbol(Type(PrimitiveType('bool')), Boolean(False)),
        'arregloDeNumeros':
            Symbol(Type(TypeArray(PrimitiveType('num'))), Array(ElemList(Number(42)))),
        'arregloDeBooleanos': 
            Symbol(Type(TypeArray(PrimitiveType('bool'))), Array(ElemList(Boolean(False))))
    }
    out = parser.parse(test_case).type_check(symbols)
    assert out == test_sol