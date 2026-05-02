f = int(input("há fumaça? digite 1 para sim ou 0 para não\n"))
b = int(input("o botão de emergência está acionado? digite 1 para sim ou 0 para não\n"))
c = int(input("a chave de segurança está ativa? digite 1 para sim ou 0 para não\n"))
m = int(input("tem movimento na área restrita? digite 1 para sim ou 0 para não\n"))

# Verifica se todos os valores são 0 ou 1

if any(x not in [0, 1] for x in [f, b, c, m]):
    print("Entrada inválida. Use apenas 0 ou 1.")
else:
    # nível 1. há fumaça
    if f == 1:
        print("alarme de incêndio acionado. vá para o ponto de encontro\n")
    else:
        print("não há incêndio\n")

# nível 2. botão de emergência mais chave de segurança

    if b == 1 and c == 1:
        print("alarme de incêndio acionado. vá para o ponto de encontro\n")
    else:
        print("não há incêndio\n")

# movimento na área restrita e sem chave
    if m == 1 and c == 0:
        print("alarme de incêndio acionado. vá para o ponto de encontro\n")
    else:
        print("não há incêndio\n")

# último nível todos juntos | As variáveis estão em maiúsculo para não conflitar com as anteriores

def alarme_4():
    try:
        F = int(input("Fumaça (1/0): "))
        B = int(input("Botão de Emergência (1/0): "))
        C = int(input("Chave de Segurança (1/0): "))
        M = int(input("Movimento em área restrita (1/0): "))

# Verifica se todos os valores são 0 ou 1

        if any(x not in [0, 1] for x in [F, B, C, M]):
            print("Entrada inválida. Use apenas 0 ou 1.")
            return

        alarme = (C and (F or B)) or M

        if alarme:
            print("Alarme DISPARADO! vá para o ponto de encontro ")
        else:
            print("não há incendio")
    except ValueError:
        print("Entrada inválida. Digite apenas números inteiros (0 ou 1).")

alarme_4()
