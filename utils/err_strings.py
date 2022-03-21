"""Excepciones de utilidad para el proyecto.
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

def error_circular_dependence(file_name:str) -> str:
    return  f'Detectadas dependencias circulares, el archivo {file_name} ya se encuentra cargado'

def error_invalid_char(char:str, column:int) -> str:
    return f'Caracter inválido ("{char}") (columna {column})'

def error_invalid_id(Id:str, column:int) -> str:
    return f'ID ilegal ("{Id}") (columna {column})'

def error_missing_semicolon(column:int):
    return f'Punto y coma faltante al final (columna {column})'

def error_expression_expected(column: int):
    return f'Se esperaba una expresión (columna {column})'

def error_id_expected(column: int):
    return f'Se esperaba un identificador (columna {column})'

def error_array_constructor_expected(column: int):
    return f'Constructor de arreglo faltante del lado derecho de la asignación (columna {column})'

def error_unclosed_array_constructor(column: int):
    return f'Constructor de arreglo sin cerrar (corchetes desbalanceados) (columna {column})'

def error_unopened_array_constructor(column: int): 
    return f'Constructor de arreglo sin abrir (corchetes desbalanceados) (columna {column})'

def error_invalid_expression_access(column: int):
    return f'Acceso inválido a expresión (columna {column})'

def error_invalid_syntax_generic(offender:str =None , column: int =None):
    if not offender and not column:
        return 'Sintaxis inválida al final de la línea'
    else:
        return f'Sintaxis inválida en "{offender}" (columna {column})'

def error_unbalance_parentheses():
    return 'Paréntesis desbalanceados'

def prefix_error(err) -> str:
    return f"ERROR: {err}"

