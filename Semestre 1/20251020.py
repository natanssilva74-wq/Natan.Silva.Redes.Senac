def sub (x,y):
    x = int(input ("digite dois numeros para subtrair\n"))
    y = int(input ())
    subtracao = (x - y)
    return subtracao if subtracao >= 0 else -subtracao
resultado = sub (0,0)
print ("o valor absoluto da subtracao e:", resultado)