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
# + y - unario vs operaciones binarias numericas
test_cases.append('- 3 ^ 4')
test_sol.append(NumberUnOp('-', NumberBinOp('^', Number(3), Number(4))))

test_cases.extend(list(f'- 3 {binOp} 4' for binOp in NUM_BIN_OPS[1:]))
test_sol.extend(list(NumberBinOp(binOp, NumberUnOp('-', Number(3)), Number(4)) for binOp in NUM_BIN_OPS[1:]))

test_cases.append('+ 3 ^ 4')
test_sol.append(NumberUnOp('+', NumberBinOp('^', Number(3), Number(4))))


# Suma y resta vs multiplicaciones
test_cases.extend(list(f'2 + 3 {binOp} 4' for binOp in ['^', '*', '%', '/'])) 
test_sol.extend(list(NumberBinOp('+', Number(2), NumberBinOp(binOp, Number(3), Number(4))) for binOp in ['^', '*', '%', '/']))

test_cases.extend(list(f'2 - 3 {binOp} 4' for binOp in ['^', '*', '%', '/']))
test_sol.extend(list(NumberBinOp('-', Number(2), NumberBinOp(binOp, Number(3), Number(4))) for binOp in ['^', '*', '%', '/']))

# Potencia vs otras multiplicaciones
test_cases.extend(list(f'x ^ y {op} 1' for op in ['*', '%', '/']))
test_sol.extend(list(NumberBinOp(op, NumberBinOp('^', Id('x'), Id('y')), Number(1)) for op in ['*', '%', '/']))

# Modulo vs otras multiplicaciones # Fallan actualmente
test_cases.extend(list(f'x % y {op} 1' for op in ['*', '^', '/']))
test_sol.extend(list(NumberBinOp('%', Id('x'), NumberBinOp(op, Id('y'), Number(1))) for op in ['*', '^', '/']))


# Operaciones binarias numericas vs comparaciones
test_cases.extend(list(f'+ 3 {binOp} 4' for binOp in NUM_BIN_OPS[1:])) 
test_sol.extend(list(NumberBinOp(binOp, NumberUnOp('+', Number(3)), Number(4)) for binOp in NUM_BIN_OPS[1:]))

test_cases.extend(list(f'2 {binOp} 3 {comparison} 4' for comparison in COMPARISONS for binOp in NUM_BIN_OPS))
test_sol.extend(list(Comparison(comparison, NumberBinOp(binOp, Number(2), Number(3)), Number(4)) for comparison in COMPARISONS for binOp in NUM_BIN_OPS))

# Operaciones Booleanas 
# && vs ||
test_cases.append('P && Q || R')
test_sol.append(BooleanBinOp('||', BooleanBinOp('&&', Id('P'), Id('Q')), Id('R')))

# Negacion
test_cases.append('!P && Q || !R')
test_sol.append(BooleanBinOp('||', BooleanBinOp('&&', BooleanUnOp('!',Id('P')), Id('Q')), BooleanUnOp('!', Id('R'))))

# Comparaciones
test_cases.extend(list((f'P {binBoolOp} 4 {comparison} 5' for binBoolOp in BOOL_BIN_OPS for comparison in COMPARISONS)))
test_sol.extend(list(( BooleanBinOp(binBoolOp, Id('P'), Comparison(comparison, Number(4), Number(5))) for binBoolOp in BOOL_BIN_OPS for comparison in COMPARISONS)))


# ------------ Ejecucion de pruebas ---------------
cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_individual_rules(test_case:str, test_sol:object):
    assert parser.parse(test_case) == test_sol
