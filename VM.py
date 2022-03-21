"""Implementación de máquina virtual para interpretar Stókhos.

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

from typing import Union

import ply.lex as lex
import ply.yacc as yacc

import AST
import tokenrules
import grammar
from utils.custom_exceptions import ParseError

class StokhosVM:
    """Máquina Virtual intérprete del lenguaje Stókhos.
    
    Atributos:
        lex:
            Instancia de Lexer con el analizador lexicográfico
            generado por la librería ply.
        errors:
            Lista de errores generados en el análisis del último comando/archivo.
    """

    def __init__(self):
        self.lex = lex.lex(module=tokenrules)
        self.parser = yacc.yacc(module=grammar)

    def process(self, command: str, line = -1) -> str:
        """Procesa y ejecuta un comando de Stókhos.

        Transforma el comando en un arbol abstracto, evalúa expresiones y las
        ejecuta en el contexto de las variables existentes en memoria.

        Retorna:
            Una cadena de caracteres con el resultado de ejecutar el comando
            pasado como argumento, dependiendo del caso:

            Caso 1: El comando es una acción válida.
                'OK: <expresión> ==> <resultado>'

                donde <expresión> es el comando y <resultado> es el resultado
                calculado por la VM.

            Caso 2: El comando es una acción válida.
                'ACK: <acción>'

                donde <acción> es el comando.
            
            Caso 3: El comando no tiene una sintaxis correcta, o no se pudo
                ejecutar exitosamente.
                'ERROR: <mensaje>'

                donde <mensaje> es un mensaje de error descriptivo.
        """

        try:
            raise NotImplementedError
        except NotImplementedError:
            prefix = 'ERROR'
            suffix = 'interpretación no implementada'
        
        return f'{prefix}: {suffix}'

    def lextest(self, command: str) -> list[str]:
        """Llama al lexer de Stókhos y construye una secuencia de tokens.

        Retorna:
            Una cadena de caracteres con el resultado del análisis
            lexicográfico del comando. Por ejemplo:

            >>> lextest("CI := 3725 * 5")
            'OK: lex("CI := 3725 * 5") ==> [TkId('CI'), TkAssign,
            TkNumber(3725), TkMult, TkNumber(5)'

            >>> lextest("  ")
            'OK: lex("  ") ==> []'

            >>> lextest("entrada mal@")
            'ERROR: Caracter inválido (“@”) en la entrada'
        """

        # Analiza el comando con el lexer de la instancia
        self.lex.input(command)

        # Lista vacia que recolecta todos los tokens encontrados en el comando
        tokens = []

        # Lista vacia que recolecta todos los tokens de error encontrados en el comando
        error_tokens = []
        for token in self.lex:
            if token.type == 'IllegalCharacter':
                # Crea una entrada de error por token de tipo caracter ilegal
                error_tokens.append(f'ERROR: Caracter inválido ("{token.value}")')
            elif token.type == 'IllegalID':
                # Crea una entrada de error por token de tipo ID ilegal
                error_tokens.append(f'ERROR: ID ilegal ("{token.value}")')
            
            else:
                tokens.append(token)

        # Formatea la salida
        output = []
        if len(error_tokens):
            output = error_tokens
        else :
            output = [f'OK: lex("{command}") ==> {tokens}']

        return output

    def parse(self, command: str) -> AST:
        try:
            return self.parser.parse(command, lexer=self.lex, tracking=True)
        except ParseError as e:
            return AST.Error(e.message)
        
    def testparser(self, command: str) -> str:
        try:
            out = self.parse(command)
            if isinstance(out, AST.Error):
                return f'ERROR: {out.cause}'
        except Exception as e:
            print(e)
            return 'TODO: Error sin handler'
        
        return f'OK: ast("{command}") ==> {out}'

# Sobreescritura del método __repr__ de los tokens de ply

def custom_repr(t: lex.LexToken):
    val = ''
    if t.type == 'TkId':
        val = f'("{t.value}")'
    elif t.type == 'TkNumber':
        val = f'({t.value})'

    return f'{t.type}{val}'

lex.LexToken.__repr__ = custom_repr