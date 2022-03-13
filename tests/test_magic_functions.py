import pytest
from REPL import StokhosCMD
from utils.constants import *


repl = StokhosCMD()
test_cases, test_sol = [], []

# Archivo con instrucciones
sol1 = ['OK: lex("x") ==> [TkId("x")]', 'OK: lex("true + 2") ==> [TkTrue, TkPlus, TkNumber(2)]', 'OK: lex("x ^ 2") ==> [TkId("x"), TkPower, TkNumber(2)]']
test_cases.append(lambda :repl.default(r'.load tests\lexer\t_1.txt'))
test_sol.append(sol1)

# Archivo con instrucciones y lineas en blanco
sol2 = ['OK: lex("false || true") ==> [TkFalse, TkOr, TkTrue]', 'OK: lex("32") ==> [TkNumber(32)]', 'OK: lex("algoAlejado") ==> [TkId("algoAlejado")]']
test_cases.append(lambda :repl.default(r'.load tests\lexer\t_2.txt'))
test_sol.append(sol2)

# Llamar al primer archivo con otro
test_cases.append(lambda :repl.default(r'.load tests\lexer\t_3.txt'))
test_sol.append(sol1)

# Llamar a los dos primeros archivos
test_cases.append(lambda :repl.default(r'.load tests\lexer\t_4.txt'))
test_sol.append(sol1 + sol2)


cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_load(test_case:str, test_sol:object, capsys):

    # Ejecutar el caso prueba y caputurar la salida estandar
    test_case()
    captured1 = capsys.readouterr()

    # Aplicar el formato de salida e imprimir la solucion esperada
    for line in test_sol:
        repl.handle_output(line)
    captured2 = capsys.readouterr()

    # Comprobar las salidas
    assert captured1.out == captured2.out