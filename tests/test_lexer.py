"""Modulos de pruebas del lexer"""

import os
import sys

p = os.path.abspath('.')
sys.path.insert(1, p)

from stokhos.VM import StokhosVM as SVM

vm = SVM()

test_cases = [
    '56 _1a25',
    '''( ) [ ] { } ! ^ * / % - < <= > >= = <> && || ' , := ; :''',
    '''()[]{}!^*/%-<<=>>==<>&&||',:=;:''',
    'num _sum := 25',
    'bool ci3725 := true || false',
    ''' z = 'x+y' ''',
    '@',
    '.2 2.1 1.',
    '2Hola'
]

def test_lexer0():
    assert vm.lextest(test_cases[0]) == 'OK: lex("56 _1a25") ==> [TkNumber(56), TkId("_1a25")]'

def test_lexer1():
    assert vm.lextest(test_cases[1]) == '''OK: lex("( ) [ ] { } ! ^ * / % - < <= > >= = <> && || ' , := ; :") ==> [TkOpenPar, TkClosePar, TkOpenBracket, TkCloseBracket, TkOpenBrace, TkCloseBrace, TkNot, TkPower, TkMult, TkDiv, TkMod, TkMinus, TkLT, TkLE, TkGT, TkGE, TkEq, TkNE, TkAnd, TkOr, TkQuote, TkComma, TkAssign, TkSemicolon, TkColon]'''

def test_lexer2():
    assert vm.lextest(test_cases[2]) == '''OK: lex("()[]{}!^*/%-<<=>>==<>&&||',:=;:") ==> [TkOpenPar, TkClosePar, TkOpenBracket, TkCloseBracket, TkOpenBrace, TkCloseBrace, TkNot, TkPower, TkMult, TkDiv, TkMod, TkMinus, TkLT, TkLE, TkGT, TkGE, TkEq, TkNE, TkAnd, TkOr, TkQuote, TkComma, TkAssign, TkSemicolon, TkColon]'''

def test_lexer3():
    assert vm.lextest(test_cases[3]) == 'OK: lex("num _sum := 25") ==> [TkNum, TkId("_sum"), TkAssign, TkNumber(25)]'

def test_lexer4():
    assert vm.lextest(test_cases[4]) == 'OK: lex("bool ci3725 := true || false") ==> [TkBool, TkId("ci3725"), TkAssign, TkTrue, TkOr, TkFalse]'

def test_lexer5():
    assert vm.lextest(test_cases[5]) == '''OK: lex(" z = 'x+y' ") ==> [TkId("z"), TkEq, TkQuote, TkId("x"), TkPlus, TkId("y"), TkQuote]'''

def test_lexer6():
    assert vm.lextest(test_cases[7]) == 'OK: lex(".2 2.1 1.") ==> [TkNumber(0.2), TkNumber(2.1), TkNumber(1.0)]'
