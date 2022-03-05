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
import tokenrules

# Clase que implementa la máquina virtual

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
        self.errors = []

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

        # Compone la salida de la función en "<prefijo>: <sufijo>", para
        # mantener un solo return al final en las siguientes etapas
        # (puede cambiar, por ahora es una propuesta)

        try:
            # Se puede lanzar una excepción por cada error, y que este sea
            # atrapado y se hace lo debido (formatear la salida, guardar el
            # error en una lista, etc.)
            raise NotImplementedError
        except NotImplementedError:
            prefix = 'ERROR'
            suffix = 'interpretación no implementada'
        
        return f'{prefix}: {suffix}'

    def lextest(self, command: str, line = -1) -> list[str]:
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
            'ERROR: caracter inválido (“@”) en la entrada'
        """

        # Analiza el comando con el lexer de la instancia
        self.lex.input(command)

        # Lista vacia que recolecta todos los tokens encontrados en el comando
        tokens = []
        for token in self.lex:
            if token.type == 'IllegalCharacter':                
                # Crea una entrada de error por token de tipo caracter ilegal
                self.errors.append({
                    "type": 'Caracter invalido',
                    "token": token,
                    "line": line
                })
            elif token.type == 'IllegalID':
                # Crea una entrada de error por token de tipo ID ilegal
                self.errors.append({
                    "type": 'ID ilegal',
                    "token": token,
                    "line": line
                })
            
            else:
                tokens.append(token)

        # Formatea la salida
        output = []
        if (len(self.errors)):
            for error in self.errors:
                output.append(self.error2str(error))
        else :
            output = [f'OK: lex("{command}") ==> {tokens}']

        return output

    def reset_errors(self):
        """Reinicia el contador de errores general de la VM
        """
        self.errors = []

    # -------------- MÉTODOS BÁSICOS --------------
    def error2str(self, error) -> str:
        output = f'ERROR: {error["type"]} ("{error["token"].value}")'

        if (error["line"] != -1):
            output = f'ERROR: {error["type"]} ("{error["token"].value}") en la linea {error["line"]}'

        return output


# Sobreescritura del método __repr__ de los tokens de ply

def custom_repr(t: lex.LexToken):
    val = ''
    if t.type == 'TkId':
        val = f'("{t.value}")'
    elif t.type == 'TkNumber':
        val = f'({t.value})'

    return f'{t.type}{val}'

lex.LexToken.__repr__ = custom_repr