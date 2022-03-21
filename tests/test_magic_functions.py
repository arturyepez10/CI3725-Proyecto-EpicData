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

from utils.err_strings import *

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
def test_load(test_case:str, test_sol:object, capsys):

    # Ejecutar el caso prueba y capturar la salida estandar
    test_case()
    captured1 = capsys.readouterr()

    # Aplicar el formato de salida e imprimir la solucion esperada
    for line in test_sol:
        repl.handle_output(line)
    captured2 = capsys.readouterr()

    # Comprobar las salidas
    assert captured1.out == captured2.out
