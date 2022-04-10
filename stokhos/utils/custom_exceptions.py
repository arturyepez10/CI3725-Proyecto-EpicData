"""Excepciones de utilidad para el proyecto.
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
class ParseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class SemanticError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class NotEnoughInfoError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class StkRuntimeError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

# Errores de validadores semánticos
class UndefinedSymbolError(Exception):
    def __init__(self, _id: str):
        # Se guarda solo la id del símbolo que no se encontró
        self.id = _id
        super().__init__(self._id)

class NotAFunctionError(Exception):
    def __init__(self, _id: str):
        # Se guarda solo la id de la función que se intentó llamar
        self.id = _id
        super().__init__(self._id)
