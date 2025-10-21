agua=18
cimento=50
areia=100
pedra=200
total=agua+cimento+areia+pedra
print("a quantidade total de kg dos materiais e:", total)

def proporcoes (agua, cimento, areia, pedra, total):
    proporcao_agua=agua/total*100
    proporcao_cimento=cimento/total*100
    proporcao_areia=areia/total*100
    proporcao_pedra=pedra/total*100
    print(f"a proporção de agua e: {proporcao_agua:.2f}%")
    print(f"a proporção de cimento e: {proporcao_cimento:.2f}%")
    print(f"a proporção de areia e: {proporcao_areia:.2f}%")
    print(f"a proporção de pedra e: {proporcao_pedra:.2f}%")
proporcoes (agua, cimento, areia, pedra, total)