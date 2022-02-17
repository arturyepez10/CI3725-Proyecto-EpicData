""" Maquina Virtual para la interpretacion de Stókhos
Autores: Arturo Yepez
         Jesus Bandez
"""

from ply.lex import lex

def process(comando:str):
    """Procesa una comando para reconocerlo (fase 2), transformarlo en un arbol abstracto (fase 3) para evaluar
    expresiones y ejecuta acciones en el conetexto de las variables existentes en memoria"""

    # Por ahora solo debe imprimir un error xd
    print('ERROR: interpretacion no implementada')

def lextest(comando:str):
    """Funcion que llama a la funcion interna para reconocer tokens y construye una secuencia de tokens.
    Ver enunciado para el formato pedido (fase 1, pag 5)"""
    print('testLexstest. Comando: "{}"'.format(comando))