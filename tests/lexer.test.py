'''Módulo de prueba de lextest.'''

from StokhosVM import StokhosVM as SVM

vm = SVM()

test_cases = [
    '56a _1a25',
    '''( ) [ ] { } ! ^ * / % \\ - < <= > >= = <> && || ' , := ; :''',
    '''()[]{}!^*/%\\-<<=>>==<>&&||',:=;:''',
    'num _sum := 25',
    'bool ci3725 := true || false',
    ''' z = 'x+y' ''',
]

for case in test_cases:
    print(vm.lextest(case))