import utils
count = 0
menu_interface = f'Pressione:\n[1] - Para efetuar o login (máx 5 tentativas)\n[2] - Esqueceu a senha\n[3] - Voltar\nDigite e aperte enter: '

while True:
    if count == 5:
        print('Você excedeu o limite de tentativas')
        break
    print(count)
    login_gui = int(input(menu_interface))
    if login_gui == 1:
        email_to_login = input("Digite seu email: ")
        password_to_login = input("Digite sua senha: ")
        if utils.check_login(email_to_login, password_to_login) == True:
            break
        count += 1
    elif login_gui == 2:
        print("esqueceu a senha")
    elif login_gui == 3:
        break