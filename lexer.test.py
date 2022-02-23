'''Módulo de prueba de lextest.

Se supone que debe estar en tests pero falta refactorizar cosas para convertir
el código en un paquete de Python
'''

from StokhosVM import StokhosVM as SVM
from utils.colors import BLUE, RESET

vm = SVM()

test_cases = [
    '56a _1a25',
    '''( ) [ ] { } ! ^ * / % \\ - < <= > >= = <> && || ' , := ; :''',
    '''()[]{}!^*/%\\-<<=>>==<>&&||',:=;:''', 'num _sum := 25',
    'bool ci3725 := true || false', ''' z = 'x+y' ''', '5', '123.321', '1.a',
    'a.1', '.123', '123.', '3a', '123.32a', '23a.2', '12.e' , '+12 -12',
    '+1.a', '-a.2', '0.-4', '0+4', '0-4', '-.2-.1-2.-1'
]

for case in test_cases:
    print(f'''{BLUE}Prueba con:'{RESET}{case}{BLUE}'{RESET}\n''')
    print(vm.lextest(case))
    print('----------------------------------------')