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

import ply.lex as lex
import ply.yacc as yacc

import stokhos.grammar as grammar
import stokhos.tokenrules as tokenrules

from . import AST
from .utils.custom_exceptions import ParseError
from .utils.err_strings import error_invalid_char, error_invalid_id
from .utils.helpers import NullLogger


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
        # No se imprime ningún mensaje que pueda generar ply
        self.lex = lex.lex(module=tokenrules)
        self.parser = yacc.yacc(module=grammar, errorlog=NullLogger)

        self.symbols = {}

    def process(self, command: str) -> str:
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
        ast = self.parse(command)

        if isinstance(ast, AST.Error):
            return f'ERROR: {ast.cause}'
        
        ast.type_check(self.symbols)

        # --- FORMA 1 ---
        # ast = self.validate(ast)
        # if type(ast) in [AST.SymDef, AST.Assign, AST.AssignArray]:
        #     res = self.execute(ast)
        #     return f'ACK: {command} ==> {res}'
        # elif type(ast) == AST.Error:
        #     return f'ERROR: {ast.cause}'
        # else:
        #     res = self.eval(ast)
        #     return f'OK: {res}'

        # --- FORMA 2 ---
        # if type(ast) in [AST.SymDef, AST.Assign, AST.AssignArray]:
        #     res = self.execute(ast)
        #     return f'ACK: {command}'
        # else:
        #     res = self.eval(ast)
        #     return f'OK: {res}'

        prefix = 'OK'
        suffix = 'TODO'
        return f'{prefix}: {suffix}'

    def lextest(self, command: str) -> str:
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
            'ERROR: Caracter inválido ("@") (columna 1)'
        """

        # Analiza el comando >con el lexer de la instancia
        self.lex.input(command)

        # Lista vacia que recolecta todos los tokens encontrados en el comando
        tokens = []

        for token in self.lex:
            if token.type == 'IllegalCharacter':
                return f'ERROR: {error_invalid_char(token.value, token.lexpos + 1)}'
            elif token.type == 'IllegalID':
                return f'ERROR: {error_invalid_id(token.value, token.lexpos + 1)}'
            else:
                tokens.append(token)

        # Formatea la salida
        return f'OK: lex("{command}") ==> {tokens}'

    def parse(self, command: str) -> AST:
        """Llama al parser de Stókhos y construye el Árbol de Sintaxis Abstracta.

        Retorna:
            Una subclase de AST con el Árbol de Sintaxis Abstracta resultado
            del análisis sintáctico del comando.
        """
        try:
            return self.parser.parse(command, lexer=self.lex, tracking=True)
        except ParseError as e:
            return AST.Error(e.message)

    def testparser(self, command: str) -> str:
        """Llama a parse(command) y convierte el Árbol de Sintaxis Abstracta
        que retorna en una cadena de caracteres para imprimirla de manera
        adecuada en la salida estándar.

        Retorna:
            Una cadena de caracteres con el resultado del análisis
            sintáctico del comando. Por ejemplo:

            >>> parse("num nota := 100;")
            'OK: ast("num nota := 100;") ==> SymDef(Type(num), Id(nota),
            Number(100))'

            >>> parse("x := x+1;")
            'OK: ast("x := x+1;") ==> Assign(Id(x), (Id(x) + Number(1)))'

            >>> parse("6+7 * true || p")
            'OK: ast("6+7 * true || p") ==> ((Number(6) + (Number(7) * 
            Boolean(true))) || Id(p))'

            >>> parse("num x:=1")
            'ERROR: Punto y coma faltante al final (columna 9)'
        """
        out = self.parse(command)
        if isinstance(out, AST.Error):
            return f'ERROR: {out.cause}'
        
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
