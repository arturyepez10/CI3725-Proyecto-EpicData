"""REPL cliente de la VM del lenguaje Stókhos

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

from sys import argv

from stokhos.REPL import StokhosCMD

repl = StokhosCMD()

def main():
    repl.cmdloop()

if __name__ == '__main__':
    enter = True

    if len(argv) != 1:
        for path in argv[1:]:
            repl.send_load(path)

        print('¿Quieres acceder al REPL de Stokhos? [y/n]: ')
        while True:
            answer = input().strip().lower()
            if answer in ['yes', 'y']:
                break
            elif answer in ['no', 'n']:
                enter = False
                break
    if enter:
        main()
