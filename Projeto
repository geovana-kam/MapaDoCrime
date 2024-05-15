import bcrypt
import termios
import sys
import tty
import webbrowser

def validar_usuario(usuario, usuarios):
    if len(usuario) < 4:
        print("Nome de usuário deve ter pelo menos 4 caracteres.")
        return False
    if usuario in usuarios:
        print("Nome de usuário já existe. Por favor, escolha outro.")
        return False
    return True

def hash_senha(senha):
    
    salt = bcrypt.gensalt()
    
    return bcrypt.hashpw(senha.encode(), salt)

def verificar_senha(senha, senha_hash):
    
    return bcrypt.checkpw(senha.encode(), senha_hash)

def getpass(prompt="Password: ", show_asterisks=True):
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        print(prompt, end='', flush=True)
        password = ''
        while True:
            key = sys.stdin.read(1)
            if key == '\r':
                break
            elif key == '\x7f':
                if password:
                    password = password[:-1]
                    print('\b \b', end='', flush=True)
            else:
                password += key
                if show_asterisks:
                    print('*', end='', flush=True)
                else:
                    print(key, end='', flush=True)
        print()  
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return password

def salvar_usuario(usuario, senha_hash, dica_seguranca, resposta_seguranca):
    with open("usuarios.txt", "a") as file:
        file.write(f"{usuario}:{senha_hash.decode()}:{dica_seguranca}:{resposta_seguranca}\n")

def salvar_boletim_ocorrencia(boletim):
    with open("boletins.txt", "a") as file:
        file.write(boletim + "\n\n")

def cadastrar_usuario(usuarios):
    while True:
        usuario = input("Digite seu nome de usuário: ").strip()
        if validar_usuario(usuario, usuarios):
            break
    senha = getpass("Digite sua senha: ", show_asterisks=True)
    while len(senha) < 6:
        senha = getpass("Senha inválida. A senha deve ter pelo menos 6 caracteres: ", show_asterisks=True)

    print()  

    dica_seguranca = input("Digite uma dica de segurança: ").strip()
    resposta_seguranca = input("Digite a resposta à dica de segurança: ").strip()

    senha_hash = hash_senha(senha)
    usuarios[usuario] = {'senha_hash': senha_hash, 'dica_seguranca': dica_seguranca, 'resposta_seguranca': resposta_seguranca}
    salvar_usuario(usuario, senha_hash, dica_seguranca, resposta_seguranca)
    print("Usuário cadastrado com sucesso!")
    print()  

def fazer_login(usuarios):
    usuario = input("Digite seu nome de usuário: ").strip()
    senha = getpass("Digite sua senha: ", show_asterisks=True)

    if usuario in usuarios and verificar_senha(senha, usuarios[usuario]['senha_hash']):
        print("\nLogin bem-sucedido!")
        menu_principal(usuario)
    else:
        print("\nNome de usuário ou senha incorretos. Por favor, tente novamente.")
    print()  

def recuperar_senha(usuarios):
    usuario = input("Digite seu nome de usuário: ").strip()
    if usuario not in usuarios:
        print("Nome de usuário não encontrado.")
        return

    resposta_seguranca = input("Digite a resposta à dica de segurança: ").strip()

    dados = usuarios[usuario]
    if dados['dica_seguranca'] == resposta_seguranca:
        senha_original = getpass("Digite sua nova senha: ", show_asterisks=False)
        senha_hash = hash_senha(senha_original)
        dados['senha_hash'] = senha_hash
        salvar_usuario(usuario, senha_hash, dados['dica_seguranca'], dados['resposta_seguranca'])
        print("Senha redefinida com sucesso!")
    else:
        print("Dica de segurança ou resposta incorretos. Por favor, tente novamente.")
    print() 

def carregar_usuarios():
    usuarios = {}
    try:
        with open("usuarios.txt", "r") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 4:
                    usuario, senha_hash, dica_seguranca, resposta_seguranca = parts
                    usuarios[usuario] = {'senha_hash': senha_hash.encode(), 'dica_seguranca': dica_seguranca, 'resposta_seguranca': resposta_seguranca}
                else:
                    print("A linha no arquivo 'usuarios.txt' não possui o formato esperado:", line)
    except FileNotFoundError:
        pass
    return usuarios

def preencher_boletim_ocorrencia(tipo_ocorrencia):
    print()
    print(f"Preenchendo Boletim de Ocorrência para Vítima de {tipo_ocorrencia}:")
    print()
    data = input("Data do ocorrido: ")
    descricao_fatos = input("Descrição dos fatos: ")
    como_ocorreu = input("Como ocorreu: ")
    envolvidos = input("Envolvidos: ")
    objetos = input("Objetos envolvidos: ")

    boletim = f"Tipo de Ocorrência: Vítima de {tipo_ocorrencia}\nData do Ocorrido: {data}\nDescrição dos Fatos: {descricao_fatos}\nComo Ocorreu: {como_ocorreu}\nEnvolvidos: {envolvidos}\nObjetos Envolvidos: {objetos}"
    
    salvar_boletim_ocorrencia(boletim)
    print("\nResumo do Boletim de Ocorrência:")
    print(boletim)
    print("\nBoletim de ocorrência gerado com sucesso!")

def menu_denuncia():
    print("\nMenu de Denúncia:")
    print()
    print("1. Vítima de Roubo")
    print("2. Vítima de Furto")
    print()
    opcao = input("Escolha uma opção (1 ou 2): ")
    if opcao == "1":
        preencher_boletim_ocorrencia("Roubo")
    elif opcao == "2":
        preencher_boletim_ocorrencia("Furto")
    else:
        print("Opção inválida.")
    print()  

def exibir_numeros_emergencia():
    print("\nNúmeros de Emergência no Brasil:")
    print("190 - Polícia Militar: Emergências policiais, assaltos, roubos, agressões, ameaças[1][2][4]")
    print("192 - SAMU: Atendimento médico de urgência, problemas cardiorrespiratórios, intoxicações, afogamentos[1][2][4]")
    print("193 - Corpo de Bombeiros: Incêndios, acidentes, salvamentos, atendimento pré-hospitalar[1][3][4]")
    print("197 - Polícia Civil: Denúncias e informações para investigações[2][4]")
    print("198 - Polícia Rodoviária: Emergências em rodovias federais[4][5]")
    print("199 - Defesa Civil: Desastres naturais, alagamentos, deslizamentos[1][3]")
    print("180 - Central de Atendimento à Mulher: Violência contra a mulher[3][5]")
    print("181 - Disque Denúncia: Denúncias anônimas de crimes[4][5]")
    print("100 - Disque Direitos Humanos: Denúncias de violações de direitos humanos[3]")
    print("188 - CVV (Centro de Valorização da Vida): Prevenção ao suicídio[3]")
    print() 

def contatar_numero_emergencia():
    numero = input("Digite o número de emergência que deseja contatar (ex: 192): ")
    if numero == "190":
        print("Você será redirecionado para a Polícia Militar.")
        webbrowser.open("tel:190")
    elif numero == "192":
        print("Você será redirecionado para o SAMU.")
        webbrowser.open("tel:192")
    elif numero == "193":
        print("Você será redirecionado para o Corpo de Bombeiros.")
        webbrowser.open("tel:193")
    elif numero == "197":
        print("Você será redirecionado para a Polícia Civil.")
        webbrowser.open("tel:197")
    elif numero == "198":
        print("Você será redirecionado para a Polícia Rodoviária.")
        webbrowser.open("tel:198")
    elif numero == "199":
        print("Você será redirecionado para a Defesa Civil.")
        webbrowser.open("tel:199")
    elif numero == "180":
        print("Você será redirecionado para a Central de Atendimento à Mulher.")
        webbrowser.open("tel:180")
    elif numero == "181":
        print("Você será redirecionado para o Disque Denúncia.")
        webbrowser.open("tel:181")
    elif numero == "100":
        print("Você será redirecionado para o Disque Direitos Humanos.")
        webbrowser.open("tel:100")
    elif numero == "188":
        print("Você será redirecionado para o CVV (Centro de Valorização da Vida).")
        webbrowser.open("tel:188")
    else:
        print("Número de emergência inválido.")
    print()  

def menu_prevencao():
    print("\nMenu de Prevenção:")
    print()
    print("1. Dicas de Segurança Pessoal")
    print("2. Números de Emergência")
    print("3. Contatar Número de Emergência")
    print()
    opcao = input("Escolha uma opção (1, 2 ou 3): ")
    if opcao == "1":
        print("Você escolheu a opção de Dicas de Segurança Pessoal.")
        
    elif opcao == "2":
        exibir_numeros_emergencia()
    elif opcao == "3":
        contatar_numero_emergencia()
    else:
        print("Opção inválida.")
    print()  

def menu_principal(usuario):
    while True:
        print("\nMenu Principal:")
        print()
        print("1. Denúncia")
        print("2. Prevenção")
        print("3. Sair")
        print()
        opcao = input("Escolha uma opção (1, 2 ou 3): ")
        if opcao == "1":
            menu_denuncia()
        elif opcao == "2":
            menu_prevencao()
        elif opcao == "3":
            print()
            print(f"Até logo, {usuario}!")
            break
        else:
            print("Opção inválida.")
        print()  

def main():
    usuarios = carregar_usuarios()

    while True:
        opcao = input("Deseja fazer login (L), se cadastrar (C) ou recuperar senha (R)? ").upper()
        if opcao == "C":
            cadastrar_usuario(usuarios)
        elif opcao == "L":
            fazer_login(usuarios)
        elif opcao == "R":
            recuperar_senha(usuarios)
        else:
            print("Opção inválida.")
        print()  

if __name__ == "__main__":
    main()
