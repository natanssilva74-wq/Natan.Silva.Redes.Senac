def soma(a, b):
    return a + b;

def subtracao(a, b):
    return a - b;

def multiplicacao(a, b):
    return a * b;

def divisao(a, b):
    if b == 0:
        return None
    return a / b;

def menu():

    print("\n Calculadora Simples ");
    print("1. Soma");
    print("2. Subtração");
    print("3. Multiplicação");
    print("4. Divisão");
    print("5. Sair");

def main():
    while True:
        menu()
        escolha = input("Escolha uma opçaõ (1-5): ");

        if escolha == '5':
            print("Encerrando calculadora. até logo");
            break

        if escolha not in {'1', '2', '3', '4'}:
            print("Opção invalida. Tente novamente.");
            continue

        try:
            a = float(input("Digite o primeiro numero: "));
            b = float(input("Digite o sehundo numero: "));
        except ValueError:
            print("Numero inválida, Digite um numero valido ");
            continue

        if escolha == '1':
            resultado = soma(a, b);
            operador = '+';
        elif escolha == '2':
            resultado = subtracao(a, b);
            operador = '-';
        elif escolha == '3':
            resultado = multiplicacao(a, b);
            operador = '*';
        elif escolha == '4':
            if b == 0:
                print("Impossivel dividir por zero");
                continue
            resultado = divisao(a, b);
            operador = '/';

        print(f"\n{a} {operador} {b} = {resultado}\n");
if __name__ == '__main__':
    main()
