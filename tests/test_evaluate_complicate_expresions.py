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

test_cases.append('(35 + 7)%(5/1) * length([-1*2, -2, -3+2, -4, -5, -6, -7])') 
test_sol.append(Number(14))

test_cases.append('sum([-42, 42, -42/2, 42/2, -42/(2+2), 42/(2+2)]) * 10^100') 
test_sol.append(Number(0))

test_cases.append('avg([-42, 42, -42/2, 42/2, -42/(2+2), 42/(2+2), 7]) + 1') 
test_sol.append(Number(2))

# Indeterminaciones numericas
test_cases.append('0^0') 
test_sol.append(Number(1)) 

# Operaciones booleanas
test_cases.append('!!!!!!((!!!!true || !!false) && !false && !!!!!!!!!!!false)') 
test_sol.append(Boolean(True))

test_cases.append('false || false || false || false || false || false ||false || !false') 
test_sol.append(Boolean(True))

test_cases.append('false && true && true || false') 
test_sol.append(Boolean(False))

# Operaciones con acotaciones
test_cases.append("'2' + '1'")
test_sol.append(Number(3))

test_cases.append("'2' - '1'")
test_sol.append(Number(1))

test_cases.append("'2' * '5'")
test_sol.append(Number(10))

test_cases.append("'6' / '2'")
test_sol.append(Number(3))

test_cases.append("'6' ^ '2'")
test_sol.append(Number(36))

test_cases.append("'3' % '2'")
test_sol.append(Number(1))

test_cases.append("-'3'")
test_sol.append(Number(-3))

test_cases.append("+'3'")
test_sol.append(Number(3))

test_cases.append("!'false'")
test_sol.append(Boolean(True))

test_cases.append("'false' && 'true'")
test_sol.append(Boolean(False))

test_cases.append("'false' || 'true'")
test_sol.append(Boolean(True))

test_cases.append("'2' < '3'")
test_sol.append(Boolean(True))

test_cases.append("'2' <= '3'")
test_sol.append(Boolean(True))

test_cases.append("'3' >= '3'")
test_sol.append(Boolean(True))

test_cases.append("'2' >= '3'")
test_sol.append(Boolean(False))

test_cases.append("'2' = '3'")
test_sol.append(Boolean(False))

test_cases.append("'2' <> '3'")
test_sol.append(Boolean(True))

test_cases.append("'true' = 'false'")
test_sol.append(Boolean(False))

test_cases.append("'true' <> 'false'")
test_sol.append(Boolean(True))

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

test_cases.append('(4 = 4) = true') 
test_sol.append(Boolean(True))

test_cases.append('(4 <> 4) <> true') 
test_sol.append(Boolean(True))

test_cases.append('4 <> 5 && true || false') 
test_sol.append(Boolean(True))

test_cases.append("'4' <> '5' && true || false") 
test_sol.append(Boolean(True))

test_cases.append("'4' <> '5' && 'true' || 'false'") 
test_sol.append(Boolean(True))

# Expresiones con aplicaciones de la funcion if
test_cases.append('if(true, 1, 2)') 
test_sol.append(Number(1))

test_cases.append('if(false, 1, 2)') 
test_sol.append(Number(2))

test_cases.append('(if(true, 1, 2) + 9) * 6') 
test_sol.append(Number(60))

test_cases.append('(if(false, 1, 2) / 4)') 
test_sol.append(Number(0.5))

test_cases.append('if(true||!false, --1*7%5, 2+9) + 8') 
test_sol.append(Number(10))

test_cases.append('if(if(if(length([1,2,3]) <> 3, true = true, false = true), false || false, true && true), --1*7%5, 2+9) + 8') 
test_sol.append(Number(10))

test_cases.append('if(true, (([1,2,3])), (([1,2,3])))[2] + 3') 
test_sol.append(Number(6))

# Funciones predefinidas
test_cases.append('ln(exp(1))') # Funcion exp
test_sol.append(Number(1))

test_cases.append('ln(2) + ln(3) = ln(2*3)') 
test_sol.append(Boolean(True))

test_cases.append('ln(4) - ln(2) = ln(4/2)') 
test_sol.append(Boolean(True))

test_cases.append('cos(pi())') 
test_sol.append(Number(-1))

test_cases.append('array(2*3, 3+1)') 
test_sol.append(Array([Number(4), Number(4), Number(4), Number(4), Number(4), Number(4)]))

test_cases.append('array(0.5*12., 3+1)') 
test_sol.append(Array([Number(4), Number(4), Number(4), Number(4), Number(4), Number(4)]))

test_cases.append('array(2.0*3.0, 3+1)') 
test_sol.append(Array([Number(4), Number(4), Number(4), Number(4), Number(4), Number(4)]))

cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_evaluate_complicate_expresions(test_case:str, test_sol:object):
    ast = VM.parse(test_case)
    if isinstance(ast, Error):
        # No se construye el AST
        assert False, f'{ast}'
    
    val = VM.validate(ast)
    if isinstance(val, Error):
        # AST invalido
        assert False, f'{val}'

    res = VM.eval(ast)
    
    assert res == test_sol


# Pruebas de histogram
def test_histogram0():
    samples = 20
    ast = VM.parse(f'histogram(1, {samples}, 10, 1, 10)')
    if isinstance(ast, Error):
        # No se construye el AST
        assert False, f'{ast}'

    val = VM.validate(ast)
    if isinstance(val, Error):
        # AST invalido
        assert False, f'{val}'

    res = VM.eval(ast)

    assert sum(res, Number(0)).value == samples

def test_histogram1():
    samples = 20
    ast = VM.parse(f"histogram('1/0', {samples}, 10, 1, 10)")
    if isinstance(ast, Error):
        # No se construye el AST
        assert False, f'{ast}'

    val = VM.validate(ast)
    if isinstance(val, Error):
        # AST invalido
        assert False, f'{val}'

    res = VM.eval(ast)

    assert sum(res, Number(0)).value == 0



# ------ Pruebas que deben arrojar errores en la VM ---------
test_cases = []
# En la prueba se definen x e y como arreglos de num y bool, respectivamente,
# de tamanio 3

# Expresiones acotadas no terminales con otras operaciones
test_cases.extend([f"'2 {op0} 1' {op1} 2" for op0 in NUM_BIN_OPS for op1 in NUM_BIN_OPS])
test_cases.extend([f"'true {op0} false' {op1} false" for op0 in BOOL_BIN_OPS for op1 in BOOL_BIN_OPS])
test_cases.extend([f"'{op0} false' {op1} false" for op0 in BOOL_UN_OPS for op1 in BOOL_BIN_OPS])

test_cases.append("''2'' + '1'")
test_cases.append("''2'' - '1'")
test_cases.append("''2'' * '5'")
test_cases.append("''6'' / '2'")
test_cases.append("''6'' ^ '2'")
test_cases.append("''3'' % '2'")
test_cases.append("-''3''")

test_cases.append("+''3''")
test_cases.append("!''false''")
test_cases.append("''false'' && 'true'")
test_cases.append("''false'' || 'true'")
test_cases.append("'2' < ''3''")
test_cases.append("'2' <= ''3''")
test_cases.append("''3'' >= ''3''")
test_cases.append("'2' >= ''3''")
test_cases.append("'2' = ''3''")
test_cases.append("'2' <> ''3''")
test_cases.append("'true' = ''false''")
test_cases.append("'true' <> ''false''")

# Accesos invalidos a arreglos
test_cases.append('[1,2,3,4][-1]')
test_cases.append('[1,2,3,4][4]')
test_cases.append('[1,2,3,4][1.1]')
test_cases.append('[1,2,3,4][2.3]')
test_cases.append('x[-1]')
test_cases.append('x[4]')
test_cases.append('x[1.1]')
test_cases.append('x[2.3]')
test_cases.append('y[-1]')
test_cases.append('y[4]')
test_cases.append('y[1.1]')
test_cases.append('y[2.3]')


# Funciones predefinidas mal usadas
test_cases.append('length(3)')
test_cases.append('floor([2])')
test_cases.append('sum(123)')
test_cases.append('avg(123)')
test_cases.append('ln(0)')
test_cases.append('ln(-1)')
test_cases.append('ln([1])')
test_cases.append('exp([3])')
test_cases.append('cos([1])')
test_cases.append('sin([1])')

test_cases.append('length(true)')
test_cases.append('floor(true)')
test_cases.append('sum(true)')
test_cases.append('avg(true)')
test_cases.append('ln(true)')
test_cases.append('ln(true)')
test_cases.append('ln(true)')
test_cases.append('exp(true)')
test_cases.append('cos(true)')
test_cases.append('sin(true)')

test_cases.append('array(-1, 3)')
test_cases.append('array(0.1, 3)')
test_cases.append('array(-1.1, 3)')
test_cases.append('array(12.76, 3)')
test_cases.append('array([12.76], 3)')
test_cases.append('array(true, 3)')
test_cases.append('array(x, 3)')

test_cases.append('histogram(1, 2.1, 5, 1, 5)')
test_cases.append('histogram(1, -2.1, 5, 1, 5)')
test_cases.append('histogram(1, -2, 5, 1, 5)')
test_cases.append('histogram(1, 5, 2.1, 1, 5)')
test_cases.append('histogram(1, 5, -2.1, 1, 5)')
test_cases.append('histogram(1, 5, -2, 1, 5)')
test_cases.append('histogram(1, 5, -2, 7, 5)')


@pytest.mark.parametrize("test_case", test_cases)
def test_evaluate_bad_complicate_expresions(test_case:str):
    # Generar VM y definirle algunos arreglos
    VM = SVM()
    process_command(VM, '[num] x := [1,2,3];')
    process_command(VM, '[bool] y := [true, false, true];')

    process_bad_command(VM, test_case)


def process_bad_command(VM, command:str):
    'Procesa un comando invalido en la VM y comprueba que no sea valido'
    out = VM.process(command)

    if not out.startswith("ERROR: "):        
        assert False, f'{out}'


def process_command(VM, command:str):
    'Procesa un comando en la VM y comprueba que sea valido'
    out = VM.process(command)
    
    if out.startswith("ERROR: "):        
        assert False, f'{out}'