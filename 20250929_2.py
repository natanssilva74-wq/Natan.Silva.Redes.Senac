import random

sorteio = random.randint(1,300) 

while sorteio != 241:
    print("numero sorteado",sorteio)
    sorteio = random.randint(1,300) 
print("você ganhou", sorteio)