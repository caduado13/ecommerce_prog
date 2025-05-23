import re

def check_email(email): #checha se o email está no formato correto
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.fullmatch(regex, email) is not None

def check_pass(password):#checha se a senha está no formato correto
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.fullmatch(regex, password) is not None

def check_cpf(cpf):#checha se o cpf está no formato correto
    regex = r'^\d{11}$'
    return re.fullmatch(regex, cpf) is not None

