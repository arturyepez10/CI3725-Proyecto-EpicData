"""Definiciones de reglas para el tokenizer de Stókhos.

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

from ply.lex import LexToken

# Palabras reservadas del lenguaje
reserved = {
    'bool' : 'TkBool',
    'num' : 'TkNum',   
    'true' : 'TkTrue',
    'false' : 'TkFalse',
}

# Definicion de los tokens
tokens = [
    'TkOpenPar', 'TkClosePar','TkOpenBracket','TkCloseBracket', 'TkOpenBrace',
    'TkCloseBrace', 'TkNot', 'TkPower', 'TkMult', 'TkDiv', 'TkMod', 'TkPlus',
    'TkMinus','TkLT', 'TkLE', 'TkGE', 'TkGT', 'TkEq', 'TkNE', 'TkAnd', 'TkOr',
    'TkQuote', 'TkComma', 'TkAssign', 'TkSemicolon', 'TkColon', 'TkId',
    'TkNumber',
] + list(reserved.values())

# Se debe ignorar todo tipo de espacio en blanco
t_ignore = ' \t'

# Regex para obtener cada token de operadores y símbolos de agrupación
t_TkOpenPar = r'\('
t_TkClosePar = r'\)'
t_TkOpenBracket = r'\['
t_TkCloseBracket = r'\]'
t_TkOpenBrace = r'\{'
t_TkCloseBrace = r'\}'
t_TkNot = r'!'
t_TkPower = r'\^'
t_TkMult = r'\*'
t_TkDiv = r'/'
t_TkMod = r'%'
t_TkPlus = r'\+'
t_TkMinus = r'-'
t_TkLT = r'<'
t_TkLE = r'<='
t_TkGE = r'>='
t_TkGT = r'>'
t_TkEq = r'='
t_TkNE = r'<>'
t_TkAnd = r'&&'
t_TkOr = r'\|\|'
t_TkQuote = r'\''
t_TkComma = r','
t_TkAssign = r':='
t_TkSemicolon = r';'
t_TkColon = r':'

    
# Regex para numeros: positivos, negativos, enteros y decimales
def t_TkNumber(t: LexToken) -> LexToken:
    r'[-+]?[0-9]*\.?[0-9]+(?!\S)'

    # Intenta guardar el número como decimal, si da error, es entero
    try:
        t.value = int(t.value)
    except ValueError:
        t.value = float(t.value)
    
    return t

# Regex para los nombres de las variables y palabras reservadas
def t_TkId(t: LexToken) -> LexToken:
    r'[_0-9a-zA-Z_][a-zA-Z_0-9]*'

    # Se hace match de identificadores con numeros al comienzo, pero se
    # debe lanzar un error si esto ocurre

    # En caso de que se haya conseguido una palabra reservada del lenguaje,
    # se le asigna su respectivo tipo al token. En cualquier otro caso, el
    # el tipo del token es 'TkId'
    t.type = reserved.get(t.value,'TkId')    # Check for reserved words
    return t

# Maneja caracteres ilegales
def t_error(t: LexToken):
    # Instancia de la clase token con la información del caracter ilegal.
    tok = LexToken()
    tok.type = 'IllegalCharacter'
    tok.value = t.value[0]
    tok.lineno = t.lineno
    tok.lexpos = t.lexpos

    # Se salta el caracter ilegal
    t.lexer.skip(1)

    # Quizás se puede lanzar una excepción a ser manejada con la VM con el
    # caracter ilegal. El enunciado dice que no deberíamos manejar caracteres
    # ilegales como tokens.