import os, sys

sys.path.insert(1, os.path.abspath('.'))

import pytest
from REPL import StokhosCMD
from utils.constants import *
from utils.err_strings import *
repl = StokhosCMD()
test_cases, test_sol = [], []

test_cases.append(lambda: repl.default(r'.ast 2;'))
test_sol.append([prefix_error(error_invalid_syntax(';', 2))])

test_cases.append(lambda: repl.default(r'.ast @'))
test_sol.append([prefix_error(error_invalid_char('@', 2))])

test_cases.append(lambda: repl.default(r'.ast .hola'))
test_sol.append([prefix_error(error_invalid_id('.hola', 1))])

test_cases.append(lambda: repl.default(r'.ast x := 2'))
test_sol.append([prefix_error(error_missing_semicolon(7))])

test_cases.append(lambda: repl.default(r'.ast x := ;'))
test_sol.append([prefix_error(error_expression_expected(5))])

test_cases.append(lambda: repl.default(r'.ast [num] := [1];'))
test_sol.append([prefix_error(error_id_expected(6))])

test_cases.append(lambda: repl.default(r'.ast [num] x := ;'))
test_sol.append([prefix_error(error_array_constructor_expected(11))])

test_cases.append(lambda: repl.default(r'.ast [num] x := 1,2,3;'))
test_sol.append([prefix_error(error_array_constructor_expected(11))])

test_cases.append(lambda: repl.default(r'.ast [num] x := [1,2,3 ;'))
test_sol.append([prefix_error(error_unclosed_array_constructor(18))])

test_cases.append(lambda: repl.default(r'.ast [num] x := 1,2,3];'))
test_sol.append([prefix_error(error_unopened_array_constructor(11))])

test_cases.append(lambda: repl.default(r'.ast true[2]'))
test_sol.append([prefix_error(error_invalid_expression_access(5))])

test_cases.append(lambda: repl.default(r'.ast (2+3'))
test_sol.append([prefix_error(error_invalid_syntax())])

test_cases.append(lambda: repl.default(r'.ast 2+3)'))
test_sol.append([prefix_error(error_invalid_syntax(')', 4))])

test_cases.append(lambda: repl.default(r'.ast [2+3'))
test_sol.append([prefix_error(error_invalid_syntax("2", 2))])

test_cases.append(lambda: repl.default(r'.ast 2+3]'))
test_sol.append([prefix_error(error_invalid_syntax(']', 4))])


#test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "parser", "1.stk")}'))
#test_sol([error_missing_semicolon(58), error_missing_semicolon(27)])

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
