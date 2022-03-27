"""Módulo con funciones que generan strings de error para la salida estándar.
Copyright (C) 2022 Arturo Yepez - Jesus Bandez - Christopher Gómez
CI3725 - Traductores e Interpretadores

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
def error_file_not_found(file_full_patch: str) -> str:
    return f'No se encuentra el archivo {file_full_patch}'

def error_is_a_directory() -> str:
    return 'Ha indicado un directorio'

def error_nonspecified_path() -> str:
    return 'No se ha indicado ninguna ruta'

def error_circular_dependency(filename: str = None) -> str:
    if filename:
        return  f'Detectadas dependencias circulares, el archivo {filename} ya se encuentra cargado'
    else:
        return 'Detectadas dependencias circulares'

def error_invalid_char(char: str, column: int) -> str:
    return f'Caracter inválido ("{char}") (columna {column})'

def error_invalid_id(_id: str, column: int) -> str:
    return f'ID ilegal ("{_id}") (columna {column})'

def error_missing_semicolon(column: int):
    return f'Punto y coma faltante al final (columna {column})'

def error_expression_expected(column: int):
    return f'Se esperaba una expresión (columna {column})'

def error_id_expected(column: int):
    return f'Se esperaba un identificador (columna {column})'

def error_unclosed_array_constructor(column: int):
    return f'Constructor de arreglo sin cerrar (corchetes desbalanceados) (columna {column})'

def error_unopened_array_constructor(column: int): 
    return f'Constructor de arreglo sin abrir (corchetes desbalanceados) (columna {column})'

def error_invalid_expression_access(column: int):
    return f'Acceso inválido a expresión (columna {column})'

def error_invalid_syntax_generic(offender:str = None, column: int = None):
    if not offender and not column:
        return 'Sintaxis inválida al final de la línea'
    else:
        return f'Sintaxis inválida en "{offender}" (columna {column})'

def error_unbalance_parentheses():
    return 'Paréntesis desbalanceados'

def error_nonexistent_special_command():
    return 'Comando especial inexistente'

def error_non_implemented_interpretation():
    return 'interpretación no implementada'

def error_invalid_arguments(command: str):
    return f'{command} no acepta argumentos'

def prefix_error(err) -> str:
    return f"ERROR: {err}"