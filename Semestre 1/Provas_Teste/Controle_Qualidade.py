setor = ['linhap', 'lote', {'brix', 'ph', 'nivel'}]

print("qual a linha de produção\n");
linhap = input ();

print("\nqual o lote?\n");
lote = input();

print("\ninsira o Brix\n");
brix = float(input());

print("\ninsira o PH\n");
ph = float(input());

print("\ninsira o nível em ML'S\n");
nivel = float(input());

if brix < 10.5:
    print("\n erro. lote com nivel de açucar muito baixo por favor constatar setor de qualidade");

elif brix > 11.2:
    print("\n erro. lote com nivel de açucar muito alto por favor constatar setor de qualidade");

else :
    print("\n nivel Brix correto");

if ph < 2.3:
    print("\n erro. lote muito ácido por favor constatar o setor de qualidade ");

elif ph > 2.6:
    print("\n erro. lote muito alcalino por favor constatar o setor de qualidade");

else :
    print("\n ácidez correta");

if nivel < 195:
    print ("\n erro. quantida abaixo do esperado constatar a engenharia\n");

elif nivel > 205:
    print("\n erro. quantidade acima do esperado constatar a engenharia\n");

else :
    print("\n quantidade correta\n")
