"""REPL cliente de la VM del lenguaje Stókhos.

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

import os
import re
from cmd import Cmd
from textwrap import dedent
from typing import Union

from StokhosVM import StokhosVM as SVM
from utils.colors import *
from utils.constants import VERSION

class StokhosCMD(Cmd):
    """Intérprete de línea de comandos para la REPL cliente de Stókhos.
    
    Aplica los métodos principales para la REPL de Stókhos. Utiliza los métodos
    base de Cmd, personalizados para ofrecer las funcionalidades especificadas.
    
    Atributos:
        vm: Instancia de la máquina virtual que interpreta Stókhos.
    """

    def __init__(self):
        # Llama el constructor de la superclase e inicializa la máquina virtual
        Cmd.__init__(self)
        self.vm = SVM()

    # Mensajes de la REPL
    prompt = f'{RESET}< Stókhos > {BOLD}'
    intro = (f'¡Bienvenido a Stókhos v{VERSION}!\n'
        'Utiliza "?" para mostrar los comandos disponibles.')
    doc_header = ('''Lista de comandos basicos (escribe 'help <nombre>' para '''
        'informacion detallada)')
    misc_header = ('''Lista de funciones disponibles (escribe 'help <nombre>' '''
        'para informacion detallada)')
    
    # ----------- MÉTODOS DE LA VIRTUAL MACHINE -----------
    def send_lexer(self, command: str):
        '''Envía un comando al analizador lexicográfico de Stókhos.

        El analizador procesa la entrada y construye un arreglo con los tokens
        hallados. Imprime el retorno de la VM en la salida estándar.
        '''

        # Análisis lexicográfico de la entrada por la VM
        out = self.vm.lextest(command)
        print_formatted(out)

    def send_process(self, command: str):
        '''Envia un comando al intérprete de Stókhos.

        Transforma el comando en un arbol abstracto, evalúa expresiones y las
        ejecuta en el contexto de las variables existentes en memoria.
        
        Imprime el retorno de la VM en la salida estándar.
        '''

        # Entrada procesada de la VM
        out = self.vm.process(command)
        print_formatted(out)

    def send_failed(self):
        print_formatted('ERROR: ".failed" no implementado.')

    def send_reset(self):
        print_formatted('ERROR: ".reset" no implementado.')

    # ---------- DOCUMENTACION DE COMANDOS ----------
    def help_lexer(self):
        print(dedent('''
            Aplica el analizador lexicográfico de Stókhos a un comando en
            particular.

            El analizador se encarga de procesar la entrada para construir 
            un arreglo de tokens segun el comando que se le envie y luego
            imprime en pantalla esa lista. En caso de error, se le notifica
            al usuario cual token presenta un error.

            Su ejecucion se realiza mediante:
            >>> .lex <comando>'''))

    def help_load(self):
        print(dedent('''
            Carga un archivo de instrucciones para Stókhos y las pasa al procesador
            de entrada por defecto

            Su ejecucion se realiza mediante:
            >>> .load <ruta_de_archivo>'''))

    def help_failed(self):
        print(dedent('''
            Imprime la lista de errores de la VM, uno por línea.

            Su ejecucion se realiza mediante:
            >>> .failed'''))

    def help_reset(self):
        print(dedent('''
            Limpia la lista de errores de la VM.

            En futuras iteraciones tendra mas responsabilidades.

            Su ejecucion se realiza mediante:
            >>> .reset'''))

    # -------------- MÉTODOS BÁSICOS --------------
    def cmdloop(self, intro=None):
        '''Ver clase base. Agrega manejo de interrupciones del teclado.'''
        print(self.intro)
        while True:
            try:
                super(StokhosCMD, self).cmdloop(intro='')
                break
            except KeyboardInterrupt:
                print_formatted(f'\n{BLUE}(Para salir, utiliza el comando . o escribe exit){RESET}')

    def do_exit(self, line: str) -> bool:
        '''Finaliza el CMD/REPL de Stókhos. Retorna True.
        
        Se puede ejecutar de dos maneras:
            >>> exit
            >>> .
        '''
        return True

    def do_clear(self, line: str):
        '''Limpia la pantalla de la terminal de los comandos anteriores.'''
        command = 'clear'

        # Si el SO es Windows, cambia el comando
        if os.name in ('nt', 'dos'):
            command = 'cls'
        os.system(command)

    def emptyline(self) -> bool:
        '''Procesador de lineas en blanco. Retorna False.
        
        El comportamiendo por defecto es no hacer nada.
        '''
        return False

    def default(self, line: str) -> Union[bool, None]:
        '''Procesador de entrada por defecto.

        Si la entrada posee alguno de los comandos reservados o funciones
        mágicas, pide su ejecucion especial a la VM. Estos comandos tienen la forma de:
            >>> .lex <comando>
            >>> .load <archivo>
            >>> .failed
            >>> .reset
        
        En el caso contrario, envia la entrada al procesador regular de la VM.

        Retorna:
            True si se termina la ejecucion de la VM.
            None cuando se interpreta un comando e imprime su salida.
        '''
        if line == ".":
            return self.do_exit(line)
        elif re.match(r'\.lex+($| )', line.strip()):
            # Corta de la entrada '.lex' y envía el comando a la VM
            command = line.lstrip('.lex').strip()
            return self.send_lexer(command)
        elif re.match(r'\.load+($| )', line.strip()):
            # Corta '.load' y carga el archivos
            path = line.lstrip('.load').strip()
            self.load(path)
        elif line == '.failed':
            self.send_failed()
        elif line == '.reset':
            self.send_reset()
        else:
            return self.send_process(line.strip())
    
    def load(self, path: str):
        '''Carga un archivo
        
        TODO:
            No implementado por completo todavía
            Llevar cuenta del contexto para eliminar el riesgo de dependencias
            circulares.
            Contexto debe tener:
                En qué directorio estás actualmente (para permitir rutas
                absolutas y relativas)
                Qué archivos se han cargado hasta el momento (para no permitir
                que se referencien entre ellos)
        '''
        try:
            with open(path) as fi:
                for line in fi.readlines():
                    self.default(line.strip())
        except FileNotFoundError:
            print_formatted(f'ERROR: no se encuentra el archivo {path}')