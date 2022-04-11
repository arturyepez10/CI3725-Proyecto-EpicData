import os
import sys
sys.path.insert(1, os.path.abspath('.'))
import pytest
from stokhos.REPL import StokhosCMD
from stokhos.utils.constants import *
from stokhos.utils.err_strings import *

repl = StokhosCMD()
test_cases, test_sol = [], []

# Error generico
test_cases.append(lambda: repl.default(r'.ast 2;'))
test_sol.append([prefix_error(error_invalid_syntax_generic(';', 2))])

# Caracter  invalido
test_cases.append(lambda: repl.default(r'.ast @'))
test_sol.append([prefix_error(error_invalid_char('@', 2))])

# ID invalido
test_cases.append(lambda: repl.default(r'.ast .hola'))
test_sol.append([prefix_error(error_invalid_id('.hola', 1))])

# ; faltante
test_cases.append(lambda: repl.default(r'.ast x := 2'))
test_sol.append([prefix_error(error_missing_semicolon())])

# Se esperaba una expresion
test_cases.append(lambda: repl.default(r'.ast x := ;'))
test_sol.append([prefix_error(error_expression_expected(5))])

# Se esperaba el identificador
test_cases.append(lambda: repl.default(r'.ast [num] := [1];'))
test_sol.append([prefix_error(error_id_expected(6))])

# Acceso invalido a expresion
test_cases.append(lambda: repl.default(r'.ast true[2]'))
test_sol.append([prefix_error(error_invalid_expression_access(5))])

# Error de sintaxis generico
test_cases.append(lambda: repl.default(r'.ast (2+3'))
test_sol.append([prefix_error(error_invalid_syntax_generic())])

test_cases.append(lambda: repl.default(r'.ast 2+3)'))
test_sol.append([prefix_error(error_invalid_syntax_generic(')', 4))])

test_cases.append(lambda: repl.default(r'.ast [2+3'))
test_sol.append([prefix_error(error_invalid_syntax_generic())])

test_cases.append(lambda: repl.default(r'.ast 2+3]'))
test_sol.append([prefix_error(error_invalid_syntax_generic(']', 4))])


cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_syntax_errors(test_case:str, test_sol:object, capsys):

    # Ejecutar el caso prueba y caputurar la salida estandar
    test_case()
    captured1 = capsys.readouterr()

    # Aplicar el formato de salida e imprimir la solucion esperada
    for line in test_sol:
        repl.handle_output(line)
    captured2 = capsys.readouterr()

    # Comprobar las salidas
    assert captured1.out == captured2.out
