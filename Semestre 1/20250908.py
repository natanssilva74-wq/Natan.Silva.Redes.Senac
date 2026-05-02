# revisão da materia. aqui fala sobre lista e dicionario

nome = input (" qual seu nome\n");
print ("\n é um prazer te conhecer ",nome);

idade = float (input ("\n qual a sua idade?\n"));
print (" daqui a cinco anos você tera ",idade + 5 );

cidade = input ("\n qual cidade você reside?\n");

corf = input ("\n qual sua cor favorita?\n");
print ("\n sua cor favorita é ",corf);

a = float(input("\n digite um numero\n"));
b = float(input("\n digite mais um numero\n"));
print ("\n a soma dos dois numero é ",a + b);

num = float(input("\n me diga um numero e eu direi o dobro\n"));
print (num * 2);

dic = {
    "nome" : nome,
    "idade" : idade,
    "corf" : corf,
    "cidade" : cidade
    }
lista = []
lista.append(dic);

print (lista);
