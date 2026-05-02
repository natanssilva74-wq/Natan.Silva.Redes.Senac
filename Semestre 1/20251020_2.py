def triangulo_area(x, y):
    x = float(input("qual a altura do triangulo em metros?\n"))
    y = float(input("qual a largura do triangulo em metros?\n"))
    area = (x * y) / 2
    print(f"a area do triangulo e: {area} metros quadrados")
def triangulo_area_positiva(x, y):
    if x >= 0 and y >= 0:
        return triangulo_area(x, y)
    if x < 0 and y < 0:
        x = -x
        y = -y
        return triangulo_area(x, y) 