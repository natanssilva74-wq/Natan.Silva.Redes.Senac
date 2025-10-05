estudante = {
    "usuario" : "natan",
    "passwd" : "31415"
}

admin = {
    "usuario_a" : "admin",
    "passwd_a" : "1234"
}


user = input("login\n");
senha = input("senha\n");
student = input("usuario é estudante? s/n \n")
h = int(input("qual o horario?\n"))

if admin ["usuario_a"] == user and admin ["passwd_a"] == senha:
    print ("você está liberado"); 

elif estudante ["usuario"] == user and estudante ["passwd"] == senha:
    if h >= 8 and h <= 18:
        print("você está liberado");
    else:
        print("acesso negado!")
else :
    print("você não vai passar!");
