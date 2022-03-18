import pytest
from REPL import StokhosCMD
from utils.constants import *


repl = StokhosCMD()
test_cases, test_sol = [], []
# -----------------------------  Pruebas .load ---------------------------
# Archivo con instrucciones
sol1 = ['OK: lex("x") ==> [TkId("x")]', 'OK: lex("true + 2") ==> [TkTrue, TkPlus, TkNumber(2)]', 'OK: lex("x ^ 2") ==> [TkId("x"), TkPower, TkNumber(2)]']
test_cases.append(lambda :repl.default(r'.load tests\tests_load\t_1.txt'))
test_sol.append(sol1)

# Archivo con instrucciones y lineas en blanco
sol2 = ['OK: lex("false || true") ==> [TkFalse, TkOr, TkTrue]', 'OK: lex("32") ==> [TkNumber(32)]', 'OK: lex("algoAlejado") ==> [TkId("algoAlejado")]']
test_cases.append(lambda :repl.default(r'.load tests\tests_load\t_2.txt'))
test_sol.append(sol2)

# Llamar al primer archivo con otro
test_cases.append(lambda :repl.default(r'.load tests\tests_load\t_3.txt'))
test_sol.append(sol1)

# Llamar a los dos primeros archivos
test_cases.append(lambda :repl.default(r'.load tests\tests_load\t_4.txt'))
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

# ------------------------ Pruebas .failed y .reset -------------------

def print_error_list_with_test_sol(test_sol):
    repl.handle_output('[', RED)
    for error in test_sol:
        if isinstance(error, dict):
            repl.handle_output(f'    ( {error["error"]}, archivo "{error["file"]}", linea {error["line"]} )', RED)
        else:
            repl.handle_output(f'    ( {error} )', RED)
    repl.handle_output(']', RED)
    
def str_invalid_char(c:str) -> str:
    return f'Caracter inválido("{c}")'

def str_invalid_Id(id:str) -> str:
    return f'ID ilegal("{id}")'

# Probar lista vacia
repl = StokhosCMD()
def test_empty_failed(capsys):
    repl.default(r'.failed')
    captured1 = capsys.readouterr()
    print_error_list_with_test_sol([])
    captured2 = capsys.readouterr()
    assert captured1 == captured2


test_cases, test_sol = [], []
# Error de caracter invalido
test_cases.append([r'.lex @'])
test_sol.append([str_invalid_char('@')])

# Comandos con errores enlazados
test_cases.append([r'.lex 2', r'.lex $', r'.lex hola', r'.lex @'])
test_sol.append([str_invalid_char('$'), str_invalid_char('@')])

# .load que contiene errores
test_cases.append([r'.load tests\tests_load\t_error_1.txt'])
test_sol.append([{'error' : str_invalid_char('@'), 'file': 't_error_1.txt', 'line': 1}])

cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_failed(test_case:str, test_sol:object, capsys):

    # Ejecutar los comandos en el caso prueba
    for command in test_case:
        repl.default(command)
    # No importan los prints ejecutados
    capsys.readouterr()
    # Mostrar la lista de errores y capturarla
    repl.default(r'.failed')
    captured1 = capsys.readouterr()

    # Imprimir la solucion esperada y capturarla
    print_error_list_with_test_sol(test_sol)
    captured2 = capsys.readouterr()

    # Reiniciar la lista de errores y despejar salida estandar
    repl.default(r'.reset')
    capsys.readouterr()

    # Comprobar las salidas
    assert captured1.out == captured2.out
