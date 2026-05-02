while True:

    valor = float(input("\ninsira o valor da compra\n"));
    pag = input("insira a forma de pagamento\n 1.Dinheiro 2.Cartão de credito 3.Cartão de debito 4.Pix 5.Sair\n");

    match pag:
        case "1":
            desconto = valor * 0.05
            print(f" valor total: R${valor}\n valor com desconto de 5%: R${valor - desconto}");
        case "2":
            desconto = valor * 0.02
            print(f" valor total: R${valor}\n valor com acréscimo de 2%: R${valor + desconto}");
        case "3":
            print(f"valor total: R${valor}\n não há desconto");
        case "4":
            desconto = valor * 0.10
            print(f"valor total: R${valor}\n valor com desconto de 10%: R${valor - desconto}");
        case "5":
            break
        case _:
            print("operação invalida Retornando ao inicio");

