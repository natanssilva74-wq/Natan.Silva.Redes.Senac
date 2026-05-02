# velho e novo

idade = float(input("qual a sua idade?\n"));
if idade > 30:
    print("você é velho");
else :
    print("você é novo");

nome = input("qual seu nome?\n");
if nome == "Afonso" or nome == "afonso":
    print ("professor");
else:
    print("aluno");

A = 0
B = 1
if A == 1 and B == 1:
    print("saida 1")
else:
    print("saida 0")

# pedágio

concar = input ("o veiculo tem conect car? 's' ou 'n' \n");
vel = float(input("qual a velocida d veiculo\n"));

if concar == "n":
    print("não tem conect car!");
else:
    ("pode prosseguir");

if vel < 40:
    print("pode prosseguir");
else:
    print("freia disgraça");

# cassino

escolha = input("qual a escolha do otário?\n");
if escolha == "coroa":
    print("deu cara. você perdeu");
else:
    print("deu coroa. você perdeu");

# sacar dinheiro casado

ass1 = float(input("o marido assinou? 1 para sim. 0 para não\n"));
ass2 = float(input("a esposa assinou? 1 para sim. 0 para não\n"));
if ass1 == 1 and ass2 == 1:
    print("pode sacar");
else:
    print("não pode sacar");



