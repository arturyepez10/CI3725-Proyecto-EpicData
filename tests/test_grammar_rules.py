"""Modulos de pruebas para las reglas en grammar.py. Se prueban las reglas de manera individual""" 

import os
import sys

import pytest

sys.path.insert(1, os.path.abspath('.'))

import ply.yacc as yacc
from stokhos.AST import *
import stokhos.grammar as grammar
from stokhos.tokenrules import tokens
from stokhos.VM import StokhosVM as SVM

# Build the parser
parser = yacc.yacc(debug=True, module=grammar)
vm = SVM()

NUM_BIN_OPS = ['^', '+', '-', '*', '%', '/']
BOOL_BIN_OPS = ['&&', '||']
COMPARISONS = ['<', '<=', '>', '>=', '=', '<>']
BOOL_UN_OPS = ['!']
NUM_UN_OPS = ['+', '-']

BIN_OPS = NUM_BIN_OPS + BOOL_BIN_OPS

# Casos pruebas para cada reglas de forma individual

# Terminales:
test_cases = [
    '2',
    'true',
    'Ramon',    
]
test_sol = [
    Number(2),
    Boolean(True),
    Id('Ramon'),
]
# Operaciones Binarias numericas
test_cases.extend(list((f'3{binOp}3' for binOp in NUM_BIN_OPS)))
test_sol.extend(list(BinOp(op, Number(3), Number(3)) for op in NUM_BIN_OPS))


# Operaciones Binarias Booleanas
test_cases.extend(list((f'true{binOp}false' for binOp in BOOL_BIN_OPS)))
test_sol.extend(list(BinOp(op, Boolean(True), Boolean(False)) for op in BOOL_BIN_OPS))


# Comparaciones
test_cases.extend(list((f'epa{comp}caballero' for comp in COMPARISONS)))
test_sol.extend(list(Comparison(op, Id('epa'), Id('caballero')) for op in COMPARISONS))

# Unarias
test_cases.extend(list((f'{unaryOp}xNoNecesariamenteBooleana' for unaryOp in BOOL_UN_OPS)))
test_cases.extend(list((f'{unaryOp}soulCalibur' for unaryOp in NUM_UN_OPS)))
test_sol.extend(list(UnOp(op, Id('xNoNecesariamenteBooleana')) for op in BOOL_UN_OPS))
test_sol.extend(list(UnOp(op, Id('soulCalibur')) for op in NUM_UN_OPS))


# Definiciones 
test_cases.extend(
    ['num x := 3;', 
    'bool x := true;',
    '[num] r := [1,2];',
    '[bool] F := [true,false];'
    ])
# Definiciones
test_sol.extend([
    SymDef(Type('num'), Id('x'), Number(3)), 
    SymDef(Type('bool'), Id('x'), Boolean(True)),
    SymDef(Type(TypedArray('num')), Id('r'), Array([Number(1), Number(2)])),
    SymDef(Type(TypedArray('bool')), Id('F'), Array([Boolean(True), Boolean(False)]))
    ])

# Asignaciones 
test_cases.extend(
    ['x := 2;', 
    'y:= false;', 
    'z:= esto_cansa;',
    'arr := [3,1,2];',
    'arreglo[2] := 5;'
    ])
test_sol.extend([
    Assign(Id('x'), Number(2)),
    Assign(Id('y'), Boolean(False)),
    Assign(Id('z'), Id('esto_cansa')),
    Assign(Id('arr'), Array([Number(3), Number(1), Number(2)])),
    AssignArrayElement(ArrayAccess(Id('arreglo'), Number(2)), Number(5))
    ])

# Acceso a arreglos
test_cases.append('g[2]')
test_sol.append(ArrayAccess(Id('g'), Number(2)))

# Llamadas a funcion
test_cases.extend(
    ['h()',
    'hola(2)',
    'unosCuantos(2,true,qlq)'])
test_sol.extend([
    FunctionCall(Id('h'), []),
    FunctionCall(Id('hola'), [Number(2)]),
    FunctionCall(Id('unosCuantos'), [Number(2), Boolean(True), Id('qlq')])])

# Parentesis y acotado
test_cases.append("'y'")
test_sol.append(Quoted(Id('y')))

test_cases.append('(y)')
test_sol.append(Id('y'))

cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_individual_rules(test_case:str, test_sol:object):
    assert parser.parse(test_case) == test_sol
    