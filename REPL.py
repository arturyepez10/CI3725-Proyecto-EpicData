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
from cmd import Cmd
from textwrap import dedent
from typing import Union

from utils.constants import *
from utils.helpers import *
from VM import StokhosVM as SVM


class StokhosCMD(Cmd):
    """Intérprete de línea de comandos para la REPL cliente de Stókhos.
    
    Aplica los métodos principales para la REPL de Stókhos. Utiliza los métodos
    base de Cmd, personalizados para ofrecer las funcionalidades especificadas.
    
    Variables de clase:
        vm: Instancia de la máquina virtual que interpreta Stókhos.
        context: direccion desde donde se ejecuta la REPL.
        loaded: conjunto de nombres de archivos que se han cargado al sistema.
        current_file: direccion del archivo actual que se esta cargando (si aplica).
        line_no: numero de linea del archivo que se lee (si aplica).
        exit: variable para salida del metodo para cargar archivos.
        errors: Lista de errores manejada en la sesion.
    """
    # Mensajes de la REPL
    prompt = f'{RESET}< Stókhos > {BOLD}'
    intro = (f'¡Bienvenido a Stókhos v{VERSION}!\n'
        'Utiliza "?" para mostrar los comandos disponibles.')
    doc_header = ('''Lista de comandos basicos (escribe 'help <nombre>' '''
        'para informacion detallada)')
    misc_header = ('''Lista de funciones disponibles (escribe 'help '''
        '''<nombre>' para informacion detallada)''')

    def __init__(self):
        # Llama el constructor de la superclase e inicializa la máquina virtual
        Cmd.__init__(self)
        self.vm = SVM()

        # Directorio desde el que se corre el REPL y conjunto con archivos
        # cargados hasta el momento.
        self.context = os.getcwd()
        self.loaded = set()
        self.current_file = '<consola>'
        self.line_no = -1

        # True si hay una condición de error urgente
        self.exit = False 

        # Lista de tripletas de errores
        self.errors = []
    
    # ----------- MÉTODOS QUE ENVIAN A LA VIRTUAL MACHINE -----------
    def send_lextest(self, command: str):
        """Envía un comando al analizador lexicográfico de Stókhos.

        El analizador procesa la entrada y construye un arreglo con los tokens
        hallados. Imprime el retorno de la VM en la salida estándar.
        """

        # Análisis lexicográfico de la entrada por la VM
        out = self.vm.lextest(command)
        self.handle_output(out)

    def send_process(self, command: str):
        """Envia un comando al intérprete de Stókhos.

        Transforma el comando en un arbol abstracto, evalúa expresiones y las
        ejecuta en el contexto de las variables existentes en memoria.
        
        Imprime el retorno de la VM en la salida estándar.
        """

        # Entrada procesada de la VM
        out = self.vm.process(command)
        self.handle_output(out)

    def send_load(self, path: str):
        """Carga un archivo lleno de instrucciones para la VM, y los envia
        al reconocedor de instrucciones deL REPL.
        """
        full_path = os.path.join(self.context, path)
        _dir = os.path.dirname(full_path)
        filename = os.path.basename(full_path)
        self.exit = False

        if filename in self.loaded:
            self.exit = True

            # Se deshace al contexto inicial del REPL
            self.context = os.getcwd()
            self.current_file = '<consola>'
            self.line_no = -1
            self.loaded.clear()

            self.handle_output(f'ERROR: Detectadas dependencias circulares, '
                f'el archivo {filename} ya se encuentra cargado')

            return

        temp1 = self.context
        temp2 = self.current_file
        temp3 = self.line_no
        try:
            # En Windows los directorios no abren con `open(full_path)`
            if os.path.isdir(full_path):
                raise IsADirectoryError

            with open(full_path) as fi:
                # Configura el nuevo contexto y actualiza conjunto de cargados
                self.context = _dir
                self.loaded.add(filename)
                self.current_file = filename
                self.line_no = 1

                for line in fi.readlines():
                    _input = line.strip()
                    if _input:
                        self.default(_input)
                    
                    if self.exit:
                        return

                    self.line_no += 1

            # Terminó la carga del archivo, deshace el contexto
            self.loaded.remove(filename)
            self.context = temp1
            self.current_file = temp2
            self.line_no = temp3

        except FileNotFoundError:
            self.exit = True
            self.handle_output(f'ERROR: No se encuentra el archivo {full_path}')
            return
        except IsADirectoryError:
            self.exit = True
            self.handle_output(f'ERROR: Ha indicado un directorio')
            return

    def send_ast(self, command: str):
        # Análisis lexicográfico de la entrada por la VM
        out = self.vm.testparser(command)
        self.handle_output(out)

    def send_failed(self):
        """Le pide la lista de errores a la VM de Stókhos y luego imprime
        los tokens de error almacenados hasta el momento de ejecucion en 
        la salida estándar.

        MODIFICAR ESTOS DOCS
        """

        self.handle_output('[', RED)
        for err_tuple in self.errors:
            _str = f'    ({err_tuple[0]}, {err_tuple[1]}, {err_tuple[2]})'
            self.handle_output(_str, RED)
        self.handle_output(']', RED)

    def send_reset(self):
        """Llama a la VM de Stókhos y le pide vaciar su lista de errores.
        """
        self.errors.clear()
        self.handle_output('OK: Lista de errores vaciada correctamente')

    # ---------- COMANDOS DE DOCUMENTACION DE COMANDOS EN REPL ----------
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
    
    def help_ast(self):
        print(dedent('''
            Ejecuta el analizador sintáctico (parser) con la entrada.

            El parser construye un arbol abstracto con la entrada y una funcion 
            especial retorna el arbol en formato de string, para que el usuario
            vea la construccion de este y pueda validar su correcto funcionamiento.

            Su ejecucion se realiza mediante:
            >>> .ast <entrada>'''))

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

    # -------------- MÉTODOS SUPERCLASE CUSTOMIZADOS --------------
    def cmdloop(self, intro=None):
        """Ver clase base. Agrega manejo de interrupciones del teclado."""
        print(self.intro)
        while True:
            try:
                super(StokhosCMD, self).cmdloop(intro='')
                break
            except KeyboardInterrupt:
                self.handle_output(f'\n(Para salir, utiliza el comando . o escribe exit)')

    def do_exit(self, line: str) -> bool:
        """Finaliza el CMD/REPL de Stókhos. Retorna True.
        
        Se puede ejecutar de dos maneras:
            >>> exit
            >>> .
        """
        return True

    def do_clear(self, line: str):
        """Limpia la pantalla de la terminal de los comandos anteriores."""
        command = 'clear'

        # Si el SO es Windows, cambia el comando
        if os.name in ('nt', 'dos'):
            command = 'cls'
        os.system(command)

    def emptyline(self) -> bool:
        """Procesador de lineas en blanco. Retorna False.
        
        El comportamiendo por defecto es no hacer nada.
        """
        return False        

    def default(self, line: str) -> Union[bool, None]:
        """Procesador de entrada por defecto.

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
        """

        if line == ".":
            return self.do_exit(line)

        elif line.startswith('#'):
            # Soporte para comentarios
            return self.emptyline()

        elif match_magic_command('lex', line):
            # Corta de la entrada '.lex' y envía el comando a la VM
            command = line[4:].strip()
            return self.send_lextest(command)

        elif match_magic_command('load', line):
            # Corta '.load' y carga el archivo
            path = line[5:].strip()
            if path:
                self.send_load(path)
            else:
                self.handle_output('ERROR: No se ha indicado ninguna ruta')

        elif match_magic_command('ast', line):
            # Corta de la entrada '.ast' e invoca al parse (entrega 2)
            command = line.lstrip('.ast').strip()
            self.send_ast(command)

        elif match_magic_command('failed', line):
            # Corta de la entrada '.failed' e imprime la lista de errores
            rem = line[7:].strip()

            # Si había en la línea algo más que .failed se usó mal el comando
            if rem:
                self.handle_output(f'ERROR: .failed no acepta argumentos')
                return
            
            self.send_failed()

        elif match_magic_command('reset', line):
            # Corta de la entrada '.reset' e imprime la lista de errores
            rem = line[6:].strip()

            # Si había en la línea algo más que .reset se usó mal el comando
            if rem:
                self.handle_output(f'ERROR: .reset no acepta argumentos')
                return
            
            self.send_reset()

        elif line.startswith('.'):
            self.handle_output('ERROR: Comando especial inexistente.')
            
        else:
            return self.send_process(line.strip())

    # -------- MISCELÁNEA --------

    def handle_output(self, line: str, color: str = BLUE):
        """Imprime con un color en especifico los resultados de la REPL al usuario.

            Segun el enunciado, la salida standard de las respuestas de Stókhos debe ser en color azul.
            
            Retorna:
                Nada, dado que los resultados se imprimen al usuario.
        """
        if line.startswith('ERROR:'):
            color = RED
            error_tuple = (self.current_file, self.line_no, line[7:])
            self.errors.append(error_tuple)

        print(f'{RESET}{color}{line}{RESET}')