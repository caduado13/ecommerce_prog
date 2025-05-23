import ecom_register
import utils

menu_message = f'ECommerce, Bem vindo!\nDigite:\n[1] - Para logar na sua conta\n[2] - Registro de novo usuário\n[3] - Fechar o sistema!\nDigite: '


while True:
    try:
        menu_gui = int(input(menu_message))
        if menu_gui == 1:
            email_to_login = input("Digite seu email: ")
            password_to_login = input("Digite sua senha: ")
            utils.check_login(email_to_login, password_to_login)
        elif menu_gui == 2:
            ecom_register.register_user()
        elif menu_gui == 3:
            break
    except:
        input('[ERRO]Por favor digite um número!\nPressione enter para voltar ao sistema!')
