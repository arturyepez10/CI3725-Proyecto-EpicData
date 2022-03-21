"""Modulo con funciones que retornan strings con formatos de errores"""
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

def error_invalid_syntax(offender:str =None , column: int =None):
    if not offender and not column:
        return 'Sintaxis inválida al final de la línea'
    else:
        return f'Sintaxis inválida en "{offender}" (columna {column})'

def error_unbalance_parentheses():
    return 'Paréntesis desbalanceados'

def prefix_error(err) -> str:
    return f"ERROR: {err}"

