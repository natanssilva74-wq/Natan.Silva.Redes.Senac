pesos = [0, 25, 50, 0, 75, 100]

def meu_len(lista):
    contador = 0
    for i in lista:
        contador += 1
    return contador

soma = 0
quantidade = 0
indice = 0
tamanho = meu_len(pesos)

while indice < tamanho:
    if pesos[indice] == 0:
        print("Alerta: Peso zero encontrado na posição", indice)
    else:
        soma = soma + pesos[indice]
        quantidade = quantidade + 1
    indice = indice + 1

if quantidade == 0:
    print("Não há pesos válidos para calcular.")
else:
    media = soma / quantidade
    print("Total dos pesos (sem zeros):", soma, "g")
    print("Média dos pesos (sem zeros):", round(media, 2), "g")
    print("Quantidade de pesos válidos:", quantidade)