"""Modulo de pruebas para la precedencia de los operadores de las reglas definidas en grammar.py"""

from ast import Num
import os, sys, pytest


sys.path.insert(1, os.path.abspath('.'))

import ply.yacc as yacc
from tokenrules import tokens
from VM import StokhosVM as SVM
import grammar
from AST import *

# Inicializar el parser
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
test_sol.append(UnOp('-', BinOp('^', Number(3), Number(4))))

test_cases.extend(list(f'- 3 {binOp} 4' for binOp in NUM_BIN_OPS[1:]))
test_sol.extend(list(BinOp(binOp, UnOp('-', Number(3)), Number(4)) for binOp in NUM_BIN_OPS[1:]))

test_cases.append('+ 3 ^ 4')
test_sol.append(UnOp('+', BinOp('^', Number(3), Number(4))))


# Suma y resta vs multiplicaciones
test_cases.extend(list(f'2 + 3 {binOp} 4' for binOp in ['^', '*', '%', '/'])) 
test_sol.extend(list(BinOp('+', Number(2), BinOp(binOp, Number(3), Number(4))) for binOp in ['^', '*', '%', '/']))

test_cases.extend(list(f'2 - 3 {binOp} 4' for binOp in ['^', '*', '%', '/']))
test_sol.extend(list(BinOp('-', Number(2), BinOp(binOp, Number(3), Number(4))) for binOp in ['^', '*', '%', '/']))

# Potencia vs otras multiplicaciones
test_cases.extend(list(f'x ^ y {op} 1' for op in ['*', '%', '/']))
test_sol.extend(list(BinOp(op, BinOp('^', Id('x'), Id('y')), Number(1)) for op in ['*', '%', '/']))

# Modulo vs otras multiplicaciones 
test_cases.extend(list(f'x % y {op} 1' for op in ['*', '/']))
test_sol.extend(list( BinOp(op, BinOp('%', Id('x'), Id('y')), Number(1)) for op in ['*', '/']))


# Operaciones binarias numericas (excepto '^') vs comparaciones
test_cases.extend(list(f'+ 3 {binOp} 4' for binOp in NUM_BIN_OPS[1:])) 
test_sol.extend(list(BinOp(binOp, UnOp('+', Number(3)), Number(4)) for binOp in NUM_BIN_OPS[1:]))

test_cases.extend(list(f'2 {binOp} 3 {comparison} 4' for comparison in COMPARISONS for binOp in NUM_BIN_OPS))
test_sol.extend(list(Comparison(comparison, BinOp(binOp, Number(2), Number(3)), Number(4)) for comparison in COMPARISONS for binOp in NUM_BIN_OPS))

# Operaciones Booleanas 
# && vs ||
test_cases.append('P && Q || R')
test_sol.append(BinOp('||', BinOp('&&', Id('P'), Id('Q')), Id('R')))

# Negacion
test_cases.append('!P && Q || !R')
test_sol.append(BinOp('||', BinOp('&&', UnOp('!',Id('P')), Id('Q')), UnOp('!', Id('R'))))

# Comparaciones
test_cases.extend(list((f'P {binBoolOp} 4 {comparison} 5' for binBoolOp in BOOL_BIN_OPS for comparison in COMPARISONS)))
test_sol.extend(list(( BinOp(binBoolOp, Id('P'), Comparison(comparison, Number(4), Number(5))) for binBoolOp in BOOL_BIN_OPS for comparison in COMPARISONS)))

# Operaciones de mismo operador con asosiacion de izquierda a derecha binarias
ops = ['*', '%', '/', '+', '-', '&&', '||']
test_cases.extend(list(( f'x {binOp} y {binOp} z {binOp} w {binOp} v' for binOp in ops )))
test_sol.extend(list((BinOp(binOp, BinOp(binOp, BinOp(binOp, BinOp(binOp, Id('x'), Id('y')), Id('z')), Id('w')), Id('v')) for binOp in ops )))

# Operaciones con combiancion de operadores de izquierda a derecha de misma precedencia
ops = ['*', '%', '/']
test_cases.extend(list(( f'x {binOp0} y {binOp1} z {binOp2} w'  for binOp0 in ops for binOp1 in ops for binOp2 in ops )))
test_sol.extend(list((BinOp(binOp2, BinOp(binOp1, BinOp(binOp0, Id('x'), Id('y')), Id('z')), Id('w')) for binOp0 in ops for binOp1 in ops for binOp2 in ops )))

ops = ['+', '-']
test_cases.extend(list(( f'x {binOp0} y {binOp1} z'  for binOp0 in ops for binOp1 in ops)))
test_sol.extend(list((BinOp(binOp1, BinOp(binOp0, Id('x'), Id('y')), Id('z'))) for binOp0 in ops for binOp1 in ops))

# Asociacion del '^'
test_cases.append('x ^ y ^ z ^ w ^ v')
test_sol.append(BinOp('^', Id('x'), BinOp('^', Id('y'), BinOp('^', Id('z'), BinOp('^', Id('w'), Id('v'))))))

# ------------ Ejecucion de pruebas -------------------------#
cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_precedence_rules(test_case:str, test_sol:object):
    assert parser.parse(test_case) == test_sol
