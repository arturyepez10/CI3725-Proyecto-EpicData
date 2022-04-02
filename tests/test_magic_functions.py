import os
import pytest
from stokhos.REPL import StokhosCMD
from stokhos.utils.constants import *
from stokhos.utils.err_strings import *

def lex_error_invalid_char(char:str) -> str:
    return f'Caracter inválido ("{char}")'

def lex_error_invalid_id(Id:str) -> str:
    return f'ID ilegal ("{Id}")'

def error_with_line_and_file(error:str, line:int, file:str) -> str:
    return  f'{error} en la línea {line} del archivo "{file}" '

def append_column(string:str, column:str) -> str:
    return f'{string}(columna {column})'

repl = StokhosCMD()
test_cases, test_sol = [], []

TEST_FOLDER = "load"

# -------------------- .loads sencillos ------------
# Archivo con instrucciones
sol1 = ['OK: lex("x") ==> [TkId("x")]', 'OK: lex("true + 2") ==> [TkTrue, TkPlus, TkNumber(2)]', 'OK: lex("x ^ 2") ==> [TkId("x"), TkPower, TkNumber(2)]']
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_1.txt")}'))
test_sol.append(sol1)

# Archivo con instrucciones y lineas en blanco
sol2 = ['OK: lex("false || true") ==> [TkFalse, TkOr, TkTrue]', 'OK: lex("32") ==> [TkNumber(32)]', 'OK: lex("algoAlejado") ==> [TkId("algoAlejado")]']
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_2.txt")}'))
test_sol.append(sol2)

# Llamar al primer archivo con otro
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_3.txt")}'))
test_sol.append(sol1)

# Llamar a los dos primeros archivos
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_4.txt")}'))
test_sol.append(sol1 + sol2)

# Archivo que llama al archivo que llama a los primeros dos archivos
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_5.txt")}'))
test_sol.append(sol1 + sol2)
# -----------------------------------------------------------------------

# ------------------- Dependencia circular ---------------------------------
# Cargarse a si mismo
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_self.txt")}'))
test_sol.append([prefix_error( error_with_line_and_file( error_circular_dependency('t_self.txt'), 1, "t_self.txt"))])

# Archivo que carga una dependecia circular
file_name = "t_6_1.txt"
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, file_name)}'))
test_sol.append([prefix_error(error_with_line_and_file(error_circular_dependency(file_name), 1, "t_6_2.txt"))])

# Archivo que carga otra dependecia circular
file_name = "t_6_3.txt"
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, file_name)}'))
test_sol.append([prefix_error(error_with_line_and_file(error_circular_dependency("t_6_1.txt"), 1, "t_6_2.txt"))])

# Cargar desde un archivo repeticion de los primeros dos archivos
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_7.txt")}'))
test_sol.append(sol1 + sol2 + sol1 + sol2 + sol1 + sol2)
#-------------------------------------------------------------------

# --------------- Archivos que contienen errores ------------------
# Archivo con un error de caracter invalido
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_error_1.txt")}'))
test_sol.append([append_column(prefix_error(error_with_line_and_file(lex_error_invalid_char("@"), 1, 't_error_1.txt')), 9)])

# Con expresion valida, seguida de error, seguida expresion valida
sol3 = ['OK: lex("3 * 2") ==> [TkNumber(3), TkMult, TkNumber(2)]']
sol4 = ['OK: lex("y && true") ==> [TkId("y"), TkAnd, TkTrue]']
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_error_2.txt")}'))
test_sol.append(sol3 + [append_column(prefix_error(error_with_line_and_file(lex_error_invalid_id("2add"), 2, 't_error_2.txt')), 1)] +  sol4)

# Cargar archivo que carga archivos con errores
sol3 = ['OK: lex("3 * 2") ==> [TkNumber(3), TkMult, TkNumber(2)]']
sol4 = ['OK: lex("y && true") ==> [TkId("y"), TkAnd, TkTrue]']
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_error_3.txt")}'))
test_sol.append(sol3 + [append_column(prefix_error(error_with_line_and_file(lex_error_invalid_id("2add"), 2, "t_error_2.txt")), 1)] +  sol4)

# -----------------------------------------------------------------

# Archivo que llama al archivo que llama a los primeros dos archivos
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_5.txt")}'))
test_sol.append(sol1 + sol2)
# -----------------------------------------------------------------------

# --------------- Archivos que contienen errores ------------------
# Archivo con un error de caracter invalido
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_error_1.txt")}'))
test_sol.append([append_column(prefix_error(error_with_line_and_file(lex_error_invalid_char("@"), 1, "t_error_1.txt")), 9)])

# Con expresion valida, seguida de error, seguida expresion valida
sol3 = ['OK: lex("3 * 2") ==> [TkNumber(3), TkMult, TkNumber(2)]']
sol4 = ['OK: lex("y && true") ==> [TkId("y"), TkAnd, TkTrue]']
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_error_2.txt")}'))
test_sol.append(sol3 + [append_column(prefix_error(error_with_line_and_file(lex_error_invalid_id("2add"), 2, "t_error_2.txt")), 1)] +  sol4)

# Cargar archivo que carga archivos con errores
sol3 = ['OK: lex("3 * 2") ==> [TkNumber(3), TkMult, TkNumber(2)]']
sol4 = ['OK: lex("y && true") ==> [TkId("y"), TkAnd, TkTrue]']
test_cases.append(lambda :repl.default(f'.load {os.path.join("tests", TEST_FOLDER, "t_error_3.txt")}'))
test_sol.append(sol3 + [append_column(prefix_error(error_with_line_and_file(lex_error_invalid_id("2add"), 2, "t_error_2.txt")), 1)] +  sol4)

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
        return f'({file}, {line}, {error})'
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
test_sol.append([simulate_error_failed_format(error_missing_semicolon())])

# Se esperaba una expresion
test_cases.append([r'.ast x := ;'])
test_sol.append([simulate_error_failed_format(error_expression_expected(5))])

# Se esperaba el identificador
test_cases.append([r'.ast [num] := [1];'])
test_sol.append([simulate_error_failed_format(error_id_expected(6))])

# Se esperaba el constructor del arreglo
#test_cases.append([r'.ast [num] x := ;'])
#test_sol.append([simulate_error_failed_format(error_array_constructor_expected(11))])

#test_cases.append([r'.ast [num] x := 1,2,3;'])
#test_sol.append([simulate_error_failed_format(error_array_constructor_expected(11))])


# Acceso invalido a expresion
test_cases.append([r'.ast true[2]'])
test_sol.append([simulate_error_failed_format(error_invalid_expression_access(5))])

# Error de sintaxis generico
test_cases.append([r'.ast (2+3'])
test_sol.append([simulate_error_failed_format(error_invalid_syntax_generic())])

test_cases.append([r'.ast 2+3)'])
test_sol.append([simulate_error_failed_format(error_invalid_syntax_generic(')', 4))])

test_cases.append([r'.ast [2+3'])
test_sol.append([simulate_error_failed_format(error_invalid_syntax_generic())])

test_cases.append([r'.ast 2+3]'])
test_sol.append([simulate_error_failed_format(error_invalid_syntax_generic(']', 4))])

# ------ Errores de lextest deben cumplir con el fomato en .failed ------

test_cases.append([r'.lex @'])
test_sol.append([simulate_error_failed_format(error_invalid_char('@', 1))])

test_cases.append([r'.lex 1Ramon'])
test_sol.append([simulate_error_failed_format(error_invalid_id('1Ramon', 1))])

# ------- Errores de comandos en el formato .failed -----
test_cases.append([r'.Cabaiero'])
test_sol.append([simulate_error_failed_format(error_nonexistent_special_command())])

test_cases.append([r'2+2;'])
test_sol.append([simulate_error_failed_format(error_non_implemented_interpretation())])

# --- Errores derivados por el .load -------

# Dependencia circular
file_patch = os.path.join('tests', TEST_FOLDER, 't_self.txt')
test_cases.append([f'.load {file_patch}'])
test_sol.append([simulate_error_failed_format(error_circular_dependency("t_self.txt"), file_patch, 1)])

# Archivo inexistente
test_cases.append([f'.load 2'])
test_sol.append([simulate_error_failed_format(error_file_not_found(os.path.abspath('2')))])
# Cargando directorio
file_patch = os.path.join('tests')
test_cases.append([f'.load {file_patch}'])
test_sol.append([simulate_error_failed_format(error_is_a_directory())])


# --------------------- Comprobar formato de .failed por errores cargados mediante .load --------

# Errores de syntax:
file_path = os.path.join('tests', 'parser', 't_syntax_errors.stk')
test_cases.append([f'.load {file_path}'])
test_syntax_sol = [
    simulate_error_failed_format(error_missing_semicolon(), file_path, 6),
    simulate_error_failed_format(error_expression_expected(9), file_path, 12),
    simulate_error_failed_format(error_id_expected(7), file_path, 15),
#    simulate_error_failed_format(error_array_constructor_expected(11), file_path, 18),
    # simulate_error_failed_format(error_unopened_array_constructor(19), file_path, 21),
    simulate_error_failed_format(error_expression_expected(5), file_path, 26),
    simulate_error_failed_format(error_id_expected(1), file_path, 29),
    # simulate_error_failed_format(error_unclosed_array_constructor(25), file_path, 32),
    simulate_error_failed_format(error_invalid_id('.id', 1), file_path, 36),    
    simulate_error_failed_format(error_invalid_expression_access(14), file_path, 41),
    simulate_error_failed_format(error_invalid_syntax_generic('!', 29), file_path, 44),
    simulate_error_failed_format(error_invalid_syntax_generic(')', 34), file_path, 47)    
]
test_sol.append(test_syntax_sol)

# Archivo que llama a archivo con errores de syntax
file_path = os.path.join('tests', 'parser', 't_syntax_errors1.stk')
test_cases.append([f'.load {file_path}'])
test_sol.append(test_syntax_sol)

# Errores de lex
file_path = os.path.join('tests', TEST_FOLDER, 't_error_4.txt')
test_cases.append([f'.load {file_path}'])
test_lexer_sol = [
    simulate_error_failed_format(error_invalid_char('@', 5), file_path, 1),
    simulate_error_failed_format(error_invalid_id('a.23', 1), file_path, 2)
    ]
test_sol.append(test_lexer_sol)

# Archivo que llamar archivo con errores de lex
file_path = os.path.join('tests', TEST_FOLDER, 't_error_5.txt')
test_cases.append([f'.load {file_path}'])
test_sol.append(test_lexer_sol)


# Errores del .load
# Cargar archivo que lleva a dependencia circular
file_path = os.path.join('tests', TEST_FOLDER, 't_6_3.txt')
test_cases.append([f'.load {file_path}'])
test_sol.append([simulate_error_failed_format(error_circular_dependency('t_6_1.txt'), os.path.join('tests', TEST_FOLDER, 't_6_2.txt'), 1)])

# Cargar archivo que carga archivo inexistente
file_path = os.path.join('tests', TEST_FOLDER, 't_load_non_existent.txt')
non_existent_file_path = os.path.join('tests', TEST_FOLDER, 'NOEXISTO.txt')
test_cases.append([f'.load {file_path}'])
test_sol.append([simulate_error_failed_format(error_file_not_found(os.path.abspath(non_existent_file_path)), file_path, 1)])

# Cargar archivo que carga un directorio
file_path = os.path.join('tests', TEST_FOLDER, 't_load_directory.txt')
test_cases.append([f'.load {file_path}'])
test_sol.append([simulate_error_failed_format(error_is_a_directory(), file_path, 1)])


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
