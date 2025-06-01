from app import ecom_register
from app import ecom_login

menu_message = f'ECommerce, Bem vindo!\nDigite:\n[1] - Para logar na sua conta\n[2] - Registro de novo usuário\n[3] - Fechar o sistema!\nSua ação: '
count = 0

while True:
    try:
        menu_gui = int(input(menu_message))
        if menu_gui == 1:
            ecom_login.login_menu(count)
            print(count)
        elif menu_gui == 2:
            ecom_register.register_user()
        elif menu_gui == 3:
            break
    except:
        input('[ERRO]Por favor digite um número!\nPressione enter para voltar ao sistema!')
