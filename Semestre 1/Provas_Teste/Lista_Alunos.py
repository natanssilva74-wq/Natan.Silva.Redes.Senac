# aqui vou listar os alunos dentro de outa lista

alunos = []

def cadastro(nome, idade, altura, ativo, notas):
    aluno = {
        "nome": nome,
        "idade": idade,
        "altura": altura,
        "ativo": ativo,
        "notas": notas,
        }

    alunos.append(aluno)

def media (aluno):
    if aluno["notas"]:
        return sum(aluno["notas"]) / len(aluno["notas"]);
    else:
        return 0

# Mostra somente os alunos ativos

def mostrar_ativos(ativos=True):
    for aluno in alunos:
        if aluno["ativo"] == ativos:

            print(f"Nome: {aluno['nome']}");
            print(f"Idade: {aluno['idade']}");
            print(f"Altura: {aluno['altura']} m");
            print(f"Ativo: {aluno['ativo']}");
            print(f"Notas: {aluno['notas']}");
            print(f"Média: {media(aluno):.2f}");
            print("-" * 30);

# Mostra todos os alunos

def mostrar_todos():

    for aluno in alunos:
        print(f"Nome: {aluno['nome']}");
        print(f"Idade: {aluno['idade']}");
        print(f"Altura: {aluno['altura']} m");
        print(f"Ativo: {aluno['ativo']}");
        print(f"Notas: {aluno['notas']}");
        print(f"Média: {media(aluno):.2f}");
        print("-" * 30);

# Aqui é onde acontece o cadastro

cadastro("camilly",21,1.65,True,[7.0,9.5,8.5,10.0]);
cadastro("alexandre",40,1.80,True,[8.0,7.5,6.0,4.5]);
cadastro("hanako",16,1.58,False,[9.0,7.0,3.5]);
cadastro("manoella",19,1.70,False,[3.5,2.0,6.5,5.5]);
cadastro("natan",21,1.82,True,[10.0,10.0,10.0,10.0]);

# Aqui exibe as informações

print("Alunos Ativos ")
mostrar_ativos(ativos=True);

print(" Alunos Inativos ")
mostrar_ativos(ativos=False);

print(" Todos os Alunos ")
mostrar_todos();




