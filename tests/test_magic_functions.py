import os

import pytest
from REPL import StokhosCMD
from utils.constants import *
from utils.err_strings import *

def lex_error_invalid_char(char:str) -> str:
    return f'Caracter inválido ("{char}")'

def lex_error_invalid_id(Id:str) -> str:
    return f'ID ilegal ("{Id}")'

def error_with_line_and_file(error:str, line:int, file:str) -> str:
    return  f'{error} en la linea {line} del archivo "{file}"'



repl = StokhosCMD()
test_cases, test_sol = [], []

# -------------------- .loads sencillos ------------
# Archivo con instrucciones
sol1 = ['OK: lex("x") ==> [TkId("x")]', 'OK: lex("true + 2") ==> [TkTrue, TkPlus, TkNumber(2)]', 'OK: lex("x ^ 2") ==> [TkId("x"), TkPower, TkNumber(2)]']
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_1.txt")}'))
test_sol.append(sol1)

# Archivo con instrucciones y lineas en blanco
sol2 = ['OK: lex("false || true") ==> [TkFalse, TkOr, TkTrue]', 'OK: lex("32") ==> [TkNumber(32)]', 'OK: lex("algoAlejado") ==> [TkId("algoAlejado")]']
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_2.txt")}'))
test_sol.append(sol2)

# Llamar al primer archivo con otro
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_3.txt")}'))
test_sol.append(sol1)

# Llamar a los dos primeros archivos
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_4.txt")}'))
test_sol.append(sol1 + sol2)

# Archivo que llama al archivo que llama a los primeros dos archivos
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_5.txt")}'))
test_sol.append(sol1 + sol2)
# -----------------------------------------------------------------------

# ------------------- Dependencia circular ---------------------------------
# Cargarse a si mismo
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_self.txt")}'))
test_sol.append([prefix_error(error_circular_dependence('t_self.txt'))])

# Archivo que carga una dependecia circular
file_name = "t_6_1.txt"
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", file_name)}'))
test_sol.append([prefix_error(error_circular_dependence(file_name))])

# Archivo que carga otra dependecia circular
file_name = "t_6_3.txt"
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", file_name)}'))
test_sol.append([prefix_error(error_circular_dependence("t_6_1.txt"))])

# Cargar desde un archivo repeticion de los primeros dos archivos
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_7.txt")}'))
test_sol.append(sol1 + sol2 + sol1 + sol2 + sol1 + sol2)
#-------------------------------------------------------------------

# --------------- Archivos que contienen errores ------------------
# Archivo con un error de caracter invalido
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_error_1.txt")}'))
test_sol.append([prefix_error(error_with_line_and_file(lex_error_invalid_char("@"), 1, 't_error_1.txt'))])

# Con expresion valida, seguida de error, seguida expresion valida
sol3 = ['OK: lex("3 * 2") ==> [TkNumber(3), TkMult, TkNumber(2)]']
sol4 = ['OK: lex("y && true") ==> [TkId("y"), TkAnd, TkTrue]']
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_error_2.txt")}'))
test_sol.append(sol3 + [prefix_error(error_with_line_and_file(lex_error_invalid_id("2add"), 2, 't_error_2.txt'))] +  sol4)

# Cargar archivo que carga archivos con errores
sol3 = ['OK: lex("3 * 2") ==> [TkNumber(3), TkMult, TkNumber(2)]']
sol4 = ['OK: lex("y && true") ==> [TkId("y"), TkAnd, TkTrue]']
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_error_3.txt")}'))
test_sol.append(sol3 + [prefix_error(error_with_line_and_file(lex_error_invalid_id("2add"), 2, "t_error_2.txt"))] +  sol4)

# -----------------------------------------------------------------

# Archivo que llama al archivo que llama a los primeros dos archivos
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_5.txt")}'))
test_sol.append(sol1 + sol2)
# -----------------------------------------------------------------------

# ------------------- Dependencia circular ---------------------------------
# Cargarse a si mismo
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_self.txt")}'))
test_sol.append([prefix_error(error_circular_dependence('t_self.txt'))])

# Archivo que carga una dependecia circular
file_name = "t_6_1.txt"
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", file_name)}'))
test_sol.append([prefix_error(error_circular_dependence(file_name))])

# Archivo que carga otra dependecia circular
file_name = "t_6_3.txt"
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", file_name)}'))
test_sol.append([prefix_error(error_circular_dependence("t_6_1.txt"))])

# Cargar desde un archivo repeticion de los primeros dos archivos
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_7.txt")}'))
test_sol.append(sol1 + sol2 + sol1 + sol2 + sol1 + sol2)
#-------------------------------------------------------------------

# --------------- Archivos que contienen errores ------------------
# Archivo con un error de caracter invalido
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_error_1.txt")}'))
test_sol.append([prefix_error(error_with_line_and_file(lex_error_invalid_char("@"), 1, "t_error_1.txt"))])

# Con expresion valida, seguida de error, seguida expresion valida
sol3 = ['OK: lex("3 * 2") ==> [TkNumber(3), TkMult, TkNumber(2)]']
sol4 = ['OK: lex("y && true") ==> [TkId("y"), TkAnd, TkTrue]']
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_error_2.txt")}'))
test_sol.append(sol3 + [prefix_error(error_with_line_and_file(lex_error_invalid_id("2add"), 2, "t_error_2.txt"))] +  sol4)

# Cargar archivo que carga archivos con errores
sol3 = ['OK: lex("3 * 2") ==> [TkNumber(3), TkMult, TkNumber(2)]']
sol4 = ['OK: lex("y && true") ==> [TkId("y"), TkAnd, TkTrue]']
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", "tests_load", "t_error_3.txt")}'))
test_sol.append(sol3 + [prefix_error(error_with_line_and_file(lex_error_invalid_id("2add"), 2, "t_error_2.txt"))] +  sol4)

# -----------------------------------------------------------------

cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_magic_functions(test_case:str, test_sol:object, capsys):

    # Ejecutar el caso prueba y capturar la salida estandar
    test_case()
    captured1 = capsys.readouterr()

    # Aplicar el formato de salida e imprimir la solucion esperada
    for line in test_sol:
        repl.handle_output(line)
    captured2 = capsys.readouterr()

    # Comprobar las salidas
    assert captured1.out == captured2.out


# Pruebas para .failed
def simulate_failed(test_sol:list):
    repl.handle_output('[', RED)
    for line in test_sol:
        output = f'    {line}'

        repl.handle_output(output, RED)
    repl.handle_output(']', RED)

def simulate_error_failed_format(error:str, file:str=None, line:int=None):
    if file and line:
        return f'({file}), {line}, {error})'
    else:
        return f'(<consola>, -1, {error})'


repl_failed_tests = StokhosCMD()
test_cases, test_sol = [], []

# ------ Pruebas de errores de sintaxis deben complir con el formato en .failed ------
# Error generico
test_cases.append([r'.ast 2;'])
test_sol.append([simulate_error_failed_format(error_invalid_syntax_generic(';', 2))])

# Caracter  invalido
test_cases.append([r'.ast @'])
test_sol.append([simulate_error_failed_format(error_invalid_char('@', 2))])

# ID invalido
test_cases.append([r'.ast .hola'])
test_sol.append([simulate_error_failed_format(error_invalid_id('.hola', 1))])

# ; faltante
test_cases.append([r'.ast x := 2'])
test_sol.append([simulate_error_failed_format(error_missing_semicolon(7))])

# Se esperaba una expresion
test_cases.append([r'.ast x := ;'])
test_sol.append([simulate_error_failed_format(error_expression_expected(5))])

# Se esperaba el identificador
test_cases.append([r'.ast [num] := [1];'])
test_sol.append([simulate_error_failed_format(error_id_expected(6))])

# Se esperaba el constructor del arreglo
test_cases.append([r'.ast [num] x := ;'])
test_sol.append([simulate_error_failed_format(error_array_constructor_expected(11))])

test_cases.append([r'.ast [num] x := 1,2,3;'])
test_sol.append([simulate_error_failed_format(error_array_constructor_expected(11))])

# Constructor de arreglo sin cerrar
test_cases.append([r'.ast [num] x := [1,2,3 ;'])
test_sol.append([simulate_error_failed_format(error_unclosed_array_constructor(18))])

# Constructor de arreglo sin abrir
test_cases.append([r'.ast [num] x := 1,2,3];'])
test_sol.append([simulate_error_failed_format(error_unopened_array_constructor(11))])

# Acceso invalido a expresion
test_cases.append([r'.ast true[2]'])
test_sol.append([simulate_error_failed_format(error_invalid_expression_access(5))])

# Error de sintaxis generico
test_cases.append([r'.ast (2+3'])
test_sol.append([simulate_error_failed_format(error_invalid_syntax_generic())])

test_cases.append([r'.ast 2+3)'])
test_sol.append([simulate_error_failed_format(error_invalid_syntax_generic(')', 4))])

test_cases.append([r'.ast [2+3'])
test_sol.append([simulate_error_failed_format(error_invalid_syntax_generic("2", 2))])

test_cases.append([r'.ast 2+3]'])
test_sol.append([simulate_error_failed_format(error_invalid_syntax_generic(']', 4))])

# ------ Errores de lextest deben cumplir con el fomato en .failed ------

test_cases.append([r'.lex @'])
test_sol.append([simulate_error_failed_format(lex_error_invalid_char('@'))])

test_cases.append([r'.lex 1Ramon'])
test_sol.append([simulate_error_failed_format(lex_error_invalid_id('1Ramon'))])

# ------- Errores de comandos en el formato .failed -----
test_cases.append([r'.Cabaiero'])
test_sol.append([simulate_error_failed_format(error_nonexistent_special_command())])

test_cases.append([r'2+2;'])
test_sol.append([simulate_error_failed_format(error_non_implemented_interpretation())])

# --- Errores derivados por el .load -------

# Dependencia circular
file_patch = os.path.join('tests', 'tests_load', 't_self.txt')
test_cases.append([f'.load {file_patch}'])
test_sol.append([simulate_error_failed_format(error_circular_dependence(), file_patch, 1)])

# Archivo inexistente
test_cases.append([f'.load 2'])
test_sol.append([simulate_error_failed_format(error_file_not_found(os.path.abspath('2')))])
# Cargando directorio
file_patch = os.path.join('tests')
test_cases.append([f'.load {file_patch}'])
test_sol.append([simulate_error_failed_format(error_is_a_directory())])



cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_failed(test_case:str, test_sol:object, capsys):
    # Resetear la lista de errores
    repl_failed_tests.default('.reset')

    # Ejecutar el caso prueba y desechar la salida estandar
    for command in test_case:
        repl_failed_tests.default(command)
    capsys.readouterr()

    # Ejecutar el .failed y capturarlo
    repl_failed_tests.default(r'.failed')
    captured1 = capsys.readouterr()

    # Simular la salida esperada del caso prueba y capturarla
    simulate_failed(test_sol)
    captured2 = capsys.readouterr()

    # Comprobar las salidas
    assert captured1.out == captured2.out