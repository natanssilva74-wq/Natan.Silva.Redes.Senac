# revisão da materia. aqui foi adicionado while para cadasrar os produtos indefinidamente
# esse código é uma releitura do anterior (20250908.1) com algumas melhorias

lista = []

while True:
    n_produto = input("Qual o nome do produto?\n");
    n_serie = input("Qual o número de série?\n");
    quantidade = input("Quantidade = \n");
    preco = float(input("Qual o preço do produto?\n"));

    produto = {
        "nome": n_produto,
        "n_serie": n_serie,
        "quantidade": quantidade,
        "preco": preco
    }

    lista.append(produto)

    continuar = input("Deseja adicionar mais um produto? (s/n): ").strip().lower()
    if continuar != 's':
        break

print("\nProdutos cadastrados:");
for i, p in enumerate(lista, start=1):
    print(f"{i}. Nome: {p['nome']}, Série: {p['n_serie']}, Quantidade: {p['quantidade']}, Preço: R$ {p['preco']:.2f}");
