# revisão da materia. cadastro de produtos e adição deles em um dicionario

n_produto = input("qual o nome do produto?\n");
n_serie = input("qual o numero de serie?\n");
quantidade = input("quantidade = \n");
preco = float(input("qual o preço do produto?\n"));

prod1 = {
    "nome" : n_produto,
    "n_serie" : n_serie,
    "quantidade" : quantidade,
    "preco" : preco
}

lista = []
lista.append(prod1);

n_produto_2 = input("qual o nome do produto?\n");
n_serie_2 = input("qual o numero de serie?\n");
quantidade_2 = input("quantidade = \n");
preco_2 = float(input("qual o preço do produto?\n"));

prod2 = {
    "nome" : n_produto_2,
    "n_serie" : n_serie_2,
    "quantidade" : quantidade_2,
    "preco" : preco_2
}


lista.append(prod2);

print (lista[0])
print (lista[1])

