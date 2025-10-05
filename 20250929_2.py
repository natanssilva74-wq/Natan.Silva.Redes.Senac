import random

sorteio = random.randint(1,300) 

a = 0

while sorteio != 29:
    print("numero sorteado\n",sorteio)
    sorteio = random.randint(1,300) 
    a += 1
    print("tentativa de numero:", a)
print("\nvocê ganhou", sorteio)
