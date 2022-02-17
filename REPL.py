""" REPL para la VM del lenguaje Stókhos
Autores: Arturo Yepez
         Jesus Bandez
"""
import VM

print('<Stókhos> ', end='')
comando = input().strip()

while comando != '.':
    # Se ignoran las lineas vacias
    if comando == '':
        pass
    
    # Comando '.lex <texto>': se llama a la funcion lextest de la VM
    # con el el input '<texto>'
    elif comando.startswith('.lex'):
        VM.lextest(comando.replace('.lex', '').strip())
       

    # Comando '.load <archivo>': Se cargan las lineas del archivo '<archivo>' una a una y
    # se procesan como si el usuario las hubiese escrito directamente
    elif comando.startswith('.load'):
        print('testLoad')

    # Comando '.failed': imprime la lista de errores, uno por linea. (Ver enunciado para el fomato) (fase1 pg 6)
    elif comando.startswith('.failed'):
        print('testFailed')

    # Comando '.reset': Por ahora, solo vacia la lista de errores
    elif comando.startswith('.reset'):
        print('testReset')

    # En cualquier otro caso, el comando es una asignacion o una expresión por lo que se debe
    # pasar a la VM. Por ahora, imprime un error
    else:
        VM.process(comando)

    print('<Stókhos> ', end='')
    comando = input().strip()


    # El REPL debe tener colores en su interfaz. Las entradas del usuario deben estar en negrillas y la respuesta 
    # de la VM en azul