"""Modulos de pruebas para las reglas en grammar.py. Se prueban las reglas de manera individual""" 

import os, sys, pytest


sys.path.insert(1, os.path.abspath('.'))

import ply.yacc as yacc
from tokenrules import tokens
from VM import StokhosVM as SVM
import grammar
import AST
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
# Operaciones Binarias numericas
test_cases.extend(list((f'3{binOp}3' for binOp in NUM_BIN_OPS)))

# Operaciones Binarias Booleanas
test_cases.extend(list((f'true{binOp}false' for binOp in BOOL_BIN_OPS)))

# Comparaciones
test_cases.extend(list((f'epa{comp}caballero' for comp in COMPARISONS)))

# Unarias
test_cases.extend(list((f'{unaryOp}xNoNecesariamenteBooleana' for unaryOp in BOOL_UN_OPS)))
test_cases.extend(list((f'{unaryOp}soulCalibur' for unaryOp in NUM_UN_OPS)))

# Definiciones 
test_cases.extend(
    ['num x := 3;', 
    'bool x := true;',
    '[num] r := [1,2];',
    '[bool] F := [true,false];'
    ])

# Asignaciones (Faltan los variaciones con arreglos)
test_cases.extend(
    ['x := 2;', 
    'y:= false;', 
    'z:= esto_cansa;',
    'arr := [3,1,2];',
    'arreglo[2] := 5;'
    ])

# Acceso a arreglos
test_cases.append('g[2]')
# Llamadas a funcion
test_cases.extend(
    ['h()',
    'hola(2)',
    'unosCuantos(2,true,qlq)'])

# Parentesis
test_cases.append("'y'")
test_cases.append('(y)')


# ------------ Soluciones esperadas ------------ #
# Terminales
test_sol = [
    AST.Number(2),
    AST.Boolean('true'),
    AST.Id('Ramon'),
]

# Operaciones Binarias numericas
test_sol.extend(list(AST.NumberBinOp(op, AST.Number(3), AST.Number(3)) for op in NUM_BIN_OPS))

# Operaciones Binarias Booleanas
test_sol.extend(list(AST.BooleanBinOp(op, AST.Boolean('true'), AST.Boolean('false')) for op in BOOL_BIN_OPS))

# Comparaciones
test_sol.extend(list(AST.Comparison(op, AST.Id('epa'), AST.Id('caballero')) for op in COMPARISONS))

# Unarias
test_sol.extend(list(AST.BooleanUnOp(op, AST.Id('xNoNecesariamenteBooleana')) for op in BOOL_UN_OPS))
test_sol.extend(list(AST.NumberUnOp(op, AST.Id('soulCalibur')) for op in NUM_UN_OPS))


# Definiciones
test_sol.extend([
    AST.SymDef(AST.Type('num'), AST.Id('x'), AST.Number(3)), 
    AST.SymDef(AST.Type('bool'), AST.Id('x'), AST.Boolean('true')),
    AST.SymDef(AST.Type(AST.TypeArray(AST.Type('num'))), AST.Id('r'), AST.ElemList(None).__debug_Init__([AST.Number(1), AST.Number(2)])),
    AST.SymDef(AST.Type(AST.TypeArray(AST.Type('bool'))), AST.Id('F'), AST.ElemList(None).__debug_Init__([AST.Boolean('true'), AST.Boolean('false')]))
    ])


# Asignaciones
test_sol.extend([
    AST.Assign(AST.Id('x'), AST.Number(2)),
    AST.Assign(AST.Id('y'), AST.Boolean('false')),
    AST.Assign(AST.Id('z'), AST.Id('esto_cansa')),
    AST.AssignArray(AST.Id('arr'), AST.ElemList(None).__debug_Init__([AST.Number(3), AST.Number(1), AST.Number(2)])),
    AST.AssignArrayElement(AST.ArrayAccess(AST.Id('arreglo'), AST.Number(2)), AST.Number(5))
    ])
'arreglo[2] := 5;'
# Acceso a arreglos
test_sol.append(AST.ArrayAccess(AST.Id('g'), AST.Number(2)))

# Llamada a funcion
test_sol.extend([
    AST.Function(AST.Id('h'), AST.ElemList(None)),
    AST.Function(AST.Id('hola'), AST.ElemList(AST.Number(2))),
    AST.Function(AST.Id('unosCuantos'), AST.ElemList(None).__debug_Init__([AST.Number(2), AST.Boolean('true'), AST.Id('qlq')]))])

# Acotado
test_sol.append(AST.Quoted(AST.Id('y')))

# Parentesis
test_sol.append(AST.Parentheses(AST.Id('y')))


cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_individual_rules(test_case:str, test_sol:object):
    assert parser.parse(test_case) == test_sol
    