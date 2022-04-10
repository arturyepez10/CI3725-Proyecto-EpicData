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

from . import grammar, tokenrules
from .AST import AST, VOID, Assign, AssignArrayElement, Error
from .symtable import SymTable, SymVar
from .utils.custom_exceptions import *
from .utils.err_strings import error_invalid_char, error_invalid_id
from .utils.evaluators import ASTEvaluator
from .utils.helpers import NullLogger
from .utils.validators import ASTValidator


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
        self.symbol_table = SymTable()
        self.validator = ASTValidator(self.symbol_table)
        self.evaluator = ASTEvaluator(self.symbol_table)

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
        if isinstance(ast, Error):
            return f'ERROR: {ast.cause}'
        
        validation = self.validate(ast)
        if isinstance(validation, Error):
            return f'ERROR: {validation.cause}'

        # Si se llega a esta línea de código, el AST era válido
        # Si el validator retornó solo
        if validation == VOID:
            # Si el validador retornó VOID era una SymDef/Assign
            # El arbol ya está anotado con el tipo del lado derecho
            res = self.execute(ast)
            if isinstance(res, Error):
                return f'ERROR: {res.cause}'
            return f'ACK: {res}'
        else:
            res = self.eval(ast)
            if isinstance(res, Error):
                return f'ERROR: {res.cause}'
            return f'OK: {command} ==> {res}'

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
            return Error(e.message)

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
        if isinstance(out, Error):
            return f'ERROR: {out.cause}'
        
        return f'OK: ast("{command}") ==> {out.ast2str()}'

    def validate(self, ast: AST) -> AST:
        """Valida un Árbol de Sintaxis Abstracta.

        Retorna:
            Una subclase de AST con el tipo del AST validado, si el arbol
            de entrada era válido, o un árbol de Error con la causa en
            caso contrario.
        """
        try:
            return self.validator.validate(ast)
        except SemanticError as e:
            return Error(e.message)

    def execute(self, ast: AST) -> AST:
        """Ejecuta un Árbol de Sintaxis Abstracta.

        Retorna:
            Una subclase de AST con el resultado de ejecutar el Árbol de
            Sintaxis Abstracta pasado como argumento.
        """
        try:
            # Evalua el lado derecho
            res  = self.eval(ast.rhs)

            # Si es una asignación a un elemento de un arreglo
            if isinstance(ast, AssignArrayElement):
                array_access = ast.array_access
                _id = array_access.expr.value
                index = array_access.index.value

                self.symbol_table.lookup(_id).value.elements[index] = res

                return f'{ast.array_access} := {res}'
            else:
                # Si es una asignación a variable
                if isinstance(ast, Assign):
                    self.symbol_table.update(ast.id.value, res)
                    return f'{ast.id} := {res}'

                # Si es una definición
                else:
                    new_symbol = SymVar(ast.type, res)
                    self.symbol_table.insert(ast.id.value, new_symbol)
                    return f'{ast.type} {ast.id} := {res}'

        except (SemanticError, NotEnoughInfoError, StkRuntimeError) as e:
            return Error(e.message)

    def eval(self, ast: AST) -> AST:
        """Evalúa un Árbol de Sintaxis Abstracta.

        Retorna:
            Una subclase de AST con el resultado de evaluar el Árbol de
            Sintaxis Abstracta pasado como argumento.
        """
        # Casi se garantiza que no puede haber errores en este punto,
        # pero no! todavía es posible
        try:
            # Tener cuidado en casos de acotación
            return self.evaluator.evaluate(ast)
        except (SemanticError, StkRuntimeError) as e:
            return Error(e.message)

# Sobreescritura del método __repr__ de los tokens de ply
def custom_repr(t: lex.LexToken):
    val = ''
    if t.type == 'TkId':
        val = f'("{t.value}")'
    elif t.type == 'TkNumber':
        val = f'({t.value})'

    return f'{t.type}{val}'

lex.LexToken.__repr__ = custom_repr
