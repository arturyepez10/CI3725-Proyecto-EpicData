import pytest
from REPL import StokhosCMD
from utils.constants import *


repl = StokhosCMD()
test_cases, test_sol = [], []


sol1 = ['OK: lex("x") ==> [TkId("x")]', 'OK: lex("true + 2") ==> [TkTrue, TkPlus, TkNumber(2)]', 'OK: lex("x ^ 2") ==> [TkId("x"), TkPower, TkNumber(2)]']
test_cases.append(lambda :repl.default(r'.load tests\lexer\t_1.txt'))
test_sol.append(sol1)


sol2 = ['OK: lex("false || true") ==> [TkFalse, TkOr, TkTrue]', 'OK: lex("32") ==> [TkNumber(32)]', 'OK: lex("algoAlejado") ==> [TkId("algoAlejado")]']
test_cases.append(lambda :repl.default(r'.load tests\lexer\t_2.txt'))
test_sol.append(sol2)




test_cases.append(lambda :repl.default(r'.load tests\lexer\t_3.txt'))
test_sol.append(sol1)






cases = list(zip(test_cases, test_sol))
@pytest.mark.parametrize("test_case,test_sol", cases)
def test_individual_rules(test_case:str, test_sol:object, capsys):

    test_case()
    captured1 = capsys.readouterr()
    for line in test_sol:
        repl.handle_output(line)
    captured2 = capsys.readouterr()
    assert captured1.out == captured2.out