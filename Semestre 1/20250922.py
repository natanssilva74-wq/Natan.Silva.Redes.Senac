valor = float(input("qual o valor da compra?\n"));

if valor >= 500.00:
    desconto = valor * 0.15
    print (f"o valor da compra {valor} \ndesconto {desconto} \ntotal: {valor - desconto} ");

elif valor >= 200:
    desconto = valor * 0.10
    print (f"o valor da compra {valor} \ndesconto {desconto} \ntotal: {valor - desconto} ");

elif valor < 200:
    print (f"não há descontos. o valor da compra é de {valor} ");
