"""
REPL para la VM del lenguaje Stókhos
    Autores: Arturo Yepez - Jesus Bandez - Christopher Gomez
    CI3725 - Traductores e Interpretadores
"""
# Libreria principal para construir REPL
from cmd import Cmd
import VM

"""
Clase StokhosCMD
    extiende:
        - Cmd
            Superclase que hereda con los metodos iniciales del CMD/REPL de nuestro
            lenguaje de programacion. Se utilza de la libreria de 'cmd'
    
    descripcion:
        Esta clase es donde se van a aplicar los metodos principales para crear la REPL del
        lenguaje de programacion 'Stókhos'. Utiliza de base los metodos ofrecidos de la
        libreria 'cmd' con una capa de customizacion para el actual proyecto.
"""
class StokhosCMD(Cmd):
    # El prompt del REPL
    prompt = '< Stókhos > '
    # Mensaje de introduccion al REPL de Stókhos
    intro = '¡Bienvenido! Utiliza "?" para mostrar los comeandos disponibles'

    # ---------------------------------------------- #
    # METODOS DE LA VIRTUAL MACHINE
    # ---------------------------------------------- #
    def send_lexer(self, line: str) -> None:
        print("Test lexer", line.split('.lexer '))

    # ---------------------------------------------- #
    # DOCUMENTACION DE COMANDOS DISPONIBLES
    # ---------------------------------------------- #
    def help_lexer(self) -> None:
        print('hola')

    # ---------------------------------------------- #
    # METODOS BASICOS
    # ---------------------------------------------- #
    def do_exit(self, line: str) -> bool:
        '''Cierra el CMD/REPL de Stókhos.'''
        return True

    def default(self, line: str) -> bool:
        if line == ".":
            return self.do_exit(line)
        elif line.startswith('.lexer ') or line.startswith('.lexer'):
            return self.send_lexer(line)
        else:
            VM.process(line)

# Se implementa ciclo principal del REPL
StokhosCMD().cmdloop()