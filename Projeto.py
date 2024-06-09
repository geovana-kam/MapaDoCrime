import bcrypt
import termios
import sys
import tty
import webbrowser
import os
import random

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_usuario(usuario, usuarios):
    if len(usuario) < 4:
        print("Nome de usuário deve ter pelo menos 4 caracteres.")
        return False
    if usuario in usuarios:
        print("Nome de usuário já existe. Por favor, escolha outro.")
        return False
    return True

def exibir_mensagem_borda(mensagem):
    tamanho_borda = len(mensagem) + 8
    print("=" * tamanho_borda)
    print(f"| {mensagem} |")
    print("=" * tamanho_borda)

def hash_senha(senha):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode(), salt)

def verificar_senha(senha, senha_hash):
    return bcrypt.checkpw(senha.encode(), senha_hash)

def getpass(prompt="Password: ", show_asterisks=True):
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        print(prompt, end='', flush=True)
        password = ''
        while True:
            key = sys.stdin.read(1)
            if key == '\r' or key == '\n':
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

def salvar_boletim_ocorrencia(usuario, boletim):
    with open("boletins.txt", "a") as file:
        file.write(f"{usuario}:{boletim}\n\n")

def cadastrar_usuario(usuarios):
    while True:
        usuario = input("Digite seu nome de usuário: ").strip()
        if validar_usuario(usuario, usuarios):
            break
    senha = getpass("Digite sua senha: ", show_asterisks=True)
    while len(senha) < 6:
        senha = getpass("Senha inválida. A senha deve ter pelo menos 6 caracteres: ", show_asterisks=True)

    print()

    dica_seguranca = input("Dica de segurança(pet, cor, fruta): ").strip()
    resposta_seguranca = input("Digite a resposta à dica de segurança: ").strip()

    senha_hash = hash_senha(senha)
    usuarios[usuario] = {'senha_hash': senha_hash, 'dica_seguranca': dica_seguranca, 'resposta_seguranca': resposta_seguranca}
    salvar_usuario(usuario, senha_hash, dica_seguranca, resposta_seguranca)
    print("Usuário cadastrado com sucesso!")
    print()

def fazer_login(usuarios):
    limpar_terminal()
    exibir_mensagem_borda("Login de Usuário")
    username = input("Digite seu nome de usuário: ")
    senha = getpass("Digite sua senha: ")
    if username in usuarios and verificar_senha(senha, usuarios[username]['senha_hash']):
        global current_user
        current_user = username
        print("Login realizado com sucesso!")
        menu_principal(username, usuarios)
    else:
        print("Nome de usuário ou senha incorretos.")
        input("Pressione Enter para continuar...")

def redefinir_senha(usuarios):
    while True:
        usuario = input("Digite seu nome de usuário ou digite 1 para voltar: ").strip()
        if usuario.lower() == "1":
            break
        if usuario not in usuarios:
            print("Nome de usuário não encontrado.")
            return

        resposta_seguranca = input("Digite a resposta à dica de segurança: ").strip()

        dados = usuarios[usuario]
        if dados['resposta_seguranca'] == resposta_seguranca:
            senha_original = getpass("Digite sua nova senha: ", show_asterisks=False)
            senha_hash = hash_senha(senha_original)
            dados['senha_hash'] = senha_hash
            salvar_usuario(usuario, senha_hash, dados['dica_seguranca'], dados['resposta_seguranca'])
            print("Senha redefinida com sucesso!")
        else:
            print("Resposta incorreta. Por favor, tente novamente.")
        print()

def carregar_usuarios():
    usuarios = {}
    try:
        with open("usuarios.txt", "r") as file:
            for line in file.read().strip().split("\n"):
                parts = line.split(":")
                if len(parts) == 4: 
                    user, senha_hash, dica, resposta = parts
                    usuarios[user] = {'senha_hash': senha_hash.encode(), 'dica_seguranca': dica, 'resposta_seguranca': resposta}
                else:
                    print(f"Erro ao ler a linha: {line}. Formato inválido.")
    except FileNotFoundError:
        pass
    return usuarios

def salvar_usuarios(usuarios):
    with open("usuarios.txt", "w") as arquivo:
        for usuario, senha in usuarios.items():
            arquivo.write(f"{usuario}:{senha}\n")

def deletar_usuario(usuarios):
    usuario = input("Digite seu nome de usuário: ").strip()
    senha = input("Digite sua senha: ").strip()

    if usuario in usuarios:
        print("Tipo de dados da senha armazenada:", type(usuarios[usuario]['senha_hash']))
        print("Tipo de dados da senha fornecida:", type(senha))

        if verificar_senha(senha, usuarios[usuario]['senha_hash']):  
            confirmacao = input("Tem certeza que deseja excluir sua conta? (s/n): ").strip().lower()
            if confirmacao == "s":
                del usuarios[usuario]
                salvar_usuarios(usuarios)  
                print("Conta excluída com sucesso!")
                main()
            else:
                print("Operação cancelada.")
        else:
            print("Senha incorreta ou formato inválido.")
    else:
        print("Nome de usuário incorreto.")

    input("Pressione Enter para continuar...")


def preencher_boletim_ocorrencia(usuario, tipo_ocorrencia):
    print()
    print(f"Preenchendo Boletim de Ocorrência para Vítima de {tipo_ocorrencia}:")
    print()
    data = input("Data do ocorrido: ")
    descricao_fatos = input("Descrição dos fatos: ")
    como_ocorreu = input("Como ocorreu: ")
    envolvidos = input("Envolvidos: ")
    objetos = input("Objetos envolvidos: ")

    boletim = f"Tipo de Ocorrência: Vítima de {tipo_ocorrencia}\nData do Ocorrido: {data}\nDescrição dos Fatos: {descricao_fatos}\nComo Ocorreu: {como_ocorreu}\nEnvolvidos: {envolvidos}\nObjetos Envolvidos: {objetos}"
    
    salvar_boletim_ocorrencia(usuario, boletim)
    print("\nBoletim de ocorrência gerado com sucesso!")

    while True:
        opcao = input("Deseja visualizar o boletim gerado? (S/N): ").strip().upper()
        if opcao == 'S':
            limpar_terminal()
            print("\nBoletim de Ocorrência:")
            print(boletim)
            input("\nPressione Enter para continuar...")
            break
        elif opcao == 'N':
            break
        else:
            print("Opção inválida. Por favor, digite S para Sim ou N para Não.")

def menu_denuncia(usuario):
    exibir_mensagem_borda("Menu de Denúncia:")
    print()
    print("1. Vítima de Roubo")
    print("2. Vítima de Furto")
    print()
    opcao = input("Escolha a opção (1 ou 2) ou escolha s para sair: ")
    if opcao == "1":
        preencher_boletim_ocorrencia(usuario, "Roubo")
    elif opcao == "2":
        preencher_boletim_ocorrencia(usuario, "Furto")
    else:
        print("Opção inválida.")
    print()

horarios_emergencia = {
    "190": ("24 horas", "24 horas"),
    "192": ("24 horas", "24 horas"),
    "193": ("24 horas", "24 horas"),
    "197": ("24 horas", "24 horas"),
    "198": ("24 horas", "24 horas"),  
    "199": ("24 horas", "24 horas"),  
    "180": ("24 horas", "24 horas"),  
    "181": ("24 horas", "24 horas"),  
    "100": ("24 horas", "24 horas"),  
    "188": ("24 horas", "24 horas"),  
}

def exibir_numeros_emergencia():
    print("\nNúmeros de Emergência no Brasil:")
    print("190 - Polícia Militar: Emergências policiais, assaltos, roubos, agressões, ameaças.")
    print("192 - SAMU: Atendimento médico de urgência, problemas cardiorrespiratórios, intoxicações, afogamentos.")
    print("193 - Corpo de Bombeiros: Incêndios, acidentes, salvamentos, atendimento pré-hospitalar.")
    print("197 - Polícia Civil: Denúncias e informações para investigações.")
    print("198 - Polícia Rodoviária: Emergências em rodovias federais.")
    print("199 - Defesa Civil: Desastres naturais, alagamentos, deslizamentos.")
    print("180 - Central de Atendimento à Mulher: Violência contra a mulher.")
    print("181 - Disque Denúncia: Denúncias anônimas de crimes.")
    print("100 - Disque Direitos Humanos: Denúncias de violações de direitos humanos.")
    print("188 - CVV (Centro de Valorização da Vida): Prevenção ao suicídio.")
    print()

    print("\nNúmeros de Emergência no Brasil:")
    for numero, horarios in horarios_emergencia.items():
        print(f"{numero} - Horário de Atendimento: {horarios[0]} às {horarios[1]}")
    print()

numeros_emergencia_urls = {
    "190": "https://www.pm.pe.gov.br/",
    "192": "https://www.saude.gov.br/192-samu",
    "193": "https://www.bombeiros.pe.gov.br/",
    "197": "https://www.policiacivil.pe.gov.br/",
    "198": "https://www.prf.gov.br/",
    "199": "https://www.pe.gov.br/orgaos/secretaria-executiva-de-defesa-civil-de-pernambuco/",
    "180": "https://www.gov.br/mdh/pt-br",
    "181": "http://www.disquedenunciape.com.br/",
    "100": "https://www.gov.br/mdh/pt-br/ondh",
    "188": "https://www.cvv.org.br/"
}

def contatar_numero_emergencia():
    while True:
        input("Aqui você vai ser direcionado para O SITE do número de emergência que você deseja contatar! \nPressione Enter")
        numero = input("Digite o número de emergência que deseja contatar (ex: 192) ou 's' para voltar: ")
        if numero.lower() == "s":
            break
        elif numero in numeros_emergencia_urls:
            print(f"Você será redirecionado para o site do serviço de emergência {numero}.")
            webbrowser.open(numeros_emergencia_urls[numero])
            break
        else:
            print("Número de emergência inválido. Tente novamente.")
    print()

def verificar_ruas_bairros_perigosos():
    print("\nVerificação de ruas e bairros perigosos da região:")
    bairros_perigosos = [
        "Boa Vista",
        "Santo Amaro",
        "São José",
        "Coelhos",
        "Cabanga",
        "Santo Antônio",
        "Joana Bezerra",
        "Pina",
        "Afogados",
        "Imbiribeira"
    ]
    
    print("\nBairros com altos índices de criminalidade no Recife:")
    for bairro in bairros_perigosos:
        print(f"- {bairro}")

    print("\nExemplos de números de ocorrências (mensais) de roubos e furtos:")
    for bairro in bairros_perigosos:
        roubos = 12 + bairros_perigosos.index(bairro) * 10
        furtos = 20 + bairros_perigosos.index(bairro) * 5
        print(f"\nNo bairro de {bairro}, há em média {roubos} casos de roubo e {furtos} casos de furto por mês.")

    input("\nPressione Enter para continuar...")

def verificar_horarios_perigosos():
    while True:
        limpar_terminal()
        print("\nVerificação de horários com maior índice de roubos e furtos:")
        exibir_mensagem_borda("Verificar Ocorrências por Horário e Bairro:")
        print("\nOpções de Horários:")
        print("1. Madrugada (0h - 6h)")
        print("2. Manhã (6h - 12h)")
        print("3. Tarde (12h - 18h)")
        print("4. Noite (18h - 0h)")
        print()
        horario_opcao = input("Escolha o horário desejado (1, 2, 3, 4): ")
        
        if horario_opcao not in ['1', '2', '3', '4']:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            input("\nPressione Enter para continuar...")
            continue

        bairros_perigosos = ["Boa Vista", "Santo Amaro",
        "São José",
        "Coelhos",
        "Cabanga",
        "Santo Antônio",
        "Joana Bezerra",
        "Pina",
        "Afogados",
        "Imbiribeira"]
        
        print("\nBairros disponíveis para consulta:")
        for index, bairro in enumerate(bairros_perigosos, start=1):
            print(f"{index}. {bairro}")

        bairro_escolhido = input("\nDigite o nome do bairro que deseja verificar: ").strip().title()
        
        if bairro_escolhido not in bairros_perigosos:
            print("Bairro não encontrado na lista de bairros perigosos.")
            input("\nPressione Enter para continuar...")
            continue
        
        horarios_ocorrencias = {
            '1': (0, 6),
            '2': (6, 12),
            '3': (12, 18),
            '4': (18, 24)
        }
        
        hora_inicio, hora_fim = horarios_ocorrencias[horario_opcao]
        hora_inicio = int(hora_inicio)
        hora_fim = int(hora_fim)  
        roubos = 10 + bairros_perigosos.index(bairro_escolhido) * 5 + hora_inicio * 2
        furtos = 15 + bairros_perigosos.index(bairro_escolhido) * 3 + hora_inicio * 2
        
        print(f"\nNo bairro de {bairro_escolhido}, entre as {hora_inicio}:00 e {hora_fim}:00, há em média {roubos} casos de roubo e {furtos} casos de furto.")
        
        escolha = input("\nDeseja fazer outra consulta? (s/n): ").strip().lower()
        if escolha == 'n':
            break

def carregar_boletins(usuario):
    boletins = []
    try:
        with open("boletins.txt", "r") as file:
            for line in file.read().strip().split("\n\n"):
                parts = line.split(":", 1)
                if len(parts) == 2: 
                    user, boletim = parts
                    if user == usuario:
                        boletins.append(boletim.strip())
    except FileNotFoundError:
        pass
    return boletins

def exibir_boletins(usuario):
    boletins = carregar_boletins(usuario)
    if boletins:
        print("\nBoletins de Ocorrência:")
        for i, boletim in enumerate(boletins, 1):
            print(f"\nBoletim {i}:")
            print(boletim)
    else:
        print("\nNenhum boletim encontrado para este usuário.")
    input("\nPressione Enter para continuar...")
    
def greet():
    greetings = ["Olá, como posso ajudá-lo?"]
    return random.choice(greetings)

def responder_p():
    faqs = {
        1: ("Como posso fazer uma denúncia de roubo?", "Você pode fazer uma denúncia de roubo preenchendo um boletim de ocorrência pelo nosso sistema."),
        2: ("Quais são os números de emergência no Brasil?", "Você pode verificar a lista completa de números de emergência no menu principal, selecionando a opção 'Exibir Números de Emergência'."),
        3: ("O que devo fazer em caso de perda de documentos?", "Em caso de perda de documentos, você deve fazer um boletim de ocorrência na delegacia mais próxima ou online através da Polícia Civil do seu estado."),
        4: ("Como posso entrar em contato com a Polícia Civil?", "Você pode entrar em contato com a Polícia Civil pelo número 197 ou visitando o site da Polícia Civil do seu estado."),
        5: ("O que é o SAMU e quando devo ligar para eles?", "O SAMU (Serviço de Atendimento Móvel de Urgência) pode ser contatado pelo número 192 para atendimento médico de emergência, como problemas cardiorrespiratórios e acidentes graves."),
    }

    while True:
        print("\np:")
        for key, (question, answer) in faqs.items():
            print(f"{key}. {question}")
        print("0. Voltar ao menu principal")
        
        opcao = input("\nDigite o número da pergunta que você deseja saber a resposta ou 0 para voltar: ")
        if opcao.isdigit():
            opcao = int(opcao)
            if opcao == 0:
                break
            if opcao in faqs:
                print(f"\n{faqs[opcao][0]}")
                print(f"Resposta: {faqs[opcao][1]}\n")
                input("Pressione Enter para continuar...")
            else:
                print("Opção inválida. Tente novamente.")
        else:
            print("Opção inválida. Tente novamente.")

def respond(user_input):
    faqs = {
        "denúncia de roubo": "Você pode fazer uma denúncia de roubo preenchendo um boletim de ocorrência pelo nosso sistema.",
        "números de emergência": "Você pode verificar a lista completa de números de emergência no menu principal, selecionando a opção 'Exibir Números de Emergência'.",
        "perda de documentos": "Em caso de perda de documentos, você deve fazer um boletim de ocorrência na delegacia mais próxima ou online através da Polícia Civil do seu estado.",
        "contato polícia civil": "Você pode entrar em contato com a Polícia Civil pelo número 197 ou visitando o site da Polícia Civil do seu estado.",
        "samu": "O SAMU (Serviço de Atendimento Móvel de Urgência) pode ser contatado pelo número 192 para atendimento médico de emergência, como problemas cardiorrespiratórios e acidentes graves.",
    }
    
    for keyword, response in faqs.items():
        if keyword in user_input:
            return response

    return "Desculpe, não tenho a resposta para essa pergunta no momento, ainda estou em processo de implementação. Por favor, no momento tente consultar nossas Perguntas Frequentes digitando p."

def assistente():
    print("\nBem-vindo a sua Assistente Virtual!")
    print("\nDigite 's' para sair a qualquer momento.")
    print(greet())
    while True:
        user_input = input("Você: ").lower()
        if user_input == "s":
            print("Até logo!")
            break
        elif user_input == "p":
            responder_p()
        else:
            response = respond(user_input)
            print("MiniAssistente:", response)
    input("\nPressione Enter para voltar ao Menu de Suporte...")


def exibir_menu_suporte():
    while True:
        limpar_terminal()
        exibir_mensagem_borda("Menu de Suporte:")
        print()
        print("1. Política de Privacidade")
        print("2. Sobre Nós")
        print("3. Contato da Equipe")
        print("4. Assistente Virtual")
        print("5. Voltar ao Menu Principal")
        print()
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            print("\nPolítica de Privacidade:")
            print()
            print("""A sua privacidade é importante para nós.
O site Oxe!Denúncia respeita a privacidade dos usuários e coleta informações pessoais apenas quando necessário para fornecer serviços. 
Os dados são protegidos contra perdas e roubos, e não são compartilhados publicamente. 
O uso contínuo do aplicativo implica aceitação das práticas de privacidade. 
Os usuários também devem se comprometer a não realizar atividades ilegais ou prejudiciais no site.""")
            input("\nPressione Enter para voltar ao Menu de Suporte...")
        elif opcao == "2":
            print("\nSobre Nós:")
            print()
            print("""Somos um grupo comprometido em tornar o mundo um lugar mais seguro para todos. 
Nosso objetivo é oferecer uma plataforma simples e eficaz para que as pessoas possam denunciar crimes e contribuir para um ambiente mais tranquilo e protegido. 
Valorizamos a transparência, a confiança e a colaboração em tudo o que fazemos. 
Junte-se a nós nessa missão de criar laços mais fortes e promover uma cultura de segurança.""")
            input("\nPressione Enter para voltar ao Menu de Suporte...")
        elif opcao == "3":
            print("\nContato da Equipe:")
            print("E-mail: oxedenuncia@gmail.com")
            input("\nPressione Enter para voltar ao Menu de Suporte...")
        elif opcao == "4":
            assistente()
        elif opcao == "5":
            return
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            input("\nPressione Enter para voltar ao Menu de Suporte...")

def menu_configuracoes():
    while True:
        limpar_terminal()
        exibir_mensagem_borda("Menu de Configurações:")
        print("1. Ajustar Resolução de Tela")
        print("2. Ajustar Brilho")
        print("3. Alterar Tema")
        print("4. Voltar ao Menu Principal")
        print()
        
        opcao = input("Escolha uma opção (1, 2, 3 ou 4): ")
        
        if opcao == "1":
            print("\nAjustar Resolução de Tela:")
            print("\nEsta funcionalidade ainda não está implementada.")
            input("Pressione Enter para continuar...")
        elif opcao == "2":
            print("\nAjustar Brilho:")
            print("\nEsta funcionalidade ainda não está implementada.")
            input("Pressione Enter para continuar...")
        elif opcao == "3":
            print("\nAlterar tema:")
            print("\nEsta funcionalidade ainda não está implementada.")
            input("Pressione Enter para continuar...")
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            print()

def menu_prevencao(usuario):
    while True:
        limpar_terminal()
        exibir_mensagem_borda("Menu de Prevenção:")
        print()
        print("1. Dicas de Segurança Pessoal")
        print("2. Números de Emergência")
        print("3. Contatar Número de Emergência")
        print("4. Verificar ruas e bairros perigosos da região.")
        print("5. Verificar horários com maior índice de roubos e furtos.")
        print("6. Visualizar Boletins Registrados")
        print("7. Voltar ao Menu Principal")
        print()
        
        opcao = input("Escolha uma opção (1, 2, 3, 4, 5, 6 ou 7): ")
        
        if opcao == "1":
            print("Você escolheu a opção de Dicas de Segurança Pessoal.\n")
            print("Aqui estão algumas dicas de segurança pessoal:\n")
            print("""- Esteja alerta: Evite mexer no celular ou usar fones de ouvido enquanto caminha. 
  Isso pode distraí-lo e torná-lo um alvo fácil. Mantenha-se atento aos arredores.

- Observe os arredores: Evite passar por grupos de pessoas à noite. 
  Use o sistema OODA (observar, orientar-se, decidir e agir) para avaliar situações potencialmente perigosas.

- Ande com confiança: Mova-se com passos fortes e mantenha a cabeça erguida. 
  Isso faz você parecer menos vulnerável.

- Fique perto do meio-fio: Evite áreas escuras e passe perto do meio-fio. 
  Se sentir que alguém é suspeito, siga em frente sem parar.

- Evite locais escuros e desertos: Ruas com boa iluminação são comprovadamente 
  mais seguras do que trajetos mal iluminados.

- Evite andar sozinho: Procure caminhar no centro da calçada e contra o sentido do trânsito, 
  dessa maneira é mais fácil perceber a aproximação de algum veículo suspeito; 
  Ao parar em pontos de ônibus, dê preferência aos que se situam em locais de grande movimento, 
  como aqueles localizados próximos a estabelecimentos comerciais.

- Em transportes públicos: Dentro da condução coloque a bolsa, mochila, pacotes ou sacolas 
  na frente do seu corpo. Muita atenção em conduções muito cheias! Deixe sua bolsa à frente 
  do corpo para dificultar a ação de marginais. Quando estiver em um coletivo e o mesmo for 
  invadido por ladrões, mantenha-se calmo e não tente nada arriscado. Não encare diretamente 
  os assaltantes e nem tente dialogar com eles. Se houver oportunidade de se desfazer de 
  alguns de seus valores, faça-o. De maneira nenhuma reaja a um assalto, pois sua vida não tem preço.

- Encontre as chaves antes de ir em direção ao carro: Quem dirige precisa tomar uma série de 
  cuidados para não ser abordado por criminosos, inclusive no momento de entrar no carro.

- Não fique dentro do veículo parado: Ao assumir o volante, também evite ficar parado sem motivo 
  dentro do veículo, principalmente à noite e em locais mais afastados de grandes fluxos de pessoas.
""")
            input("Pressione Enter para continuar...")

        elif opcao == "2":
            exibir_numeros_emergencia()
            input("Pressione Enter para continuar...")

        elif opcao == "3":
            contatar_numero_emergencia()

        elif opcao == "4":
            verificar_ruas_bairros_perigosos()

        elif opcao == "5":
            verificar_horarios_perigosos()

        elif opcao == "6":
            exibir_boletins(usuario)
            print("6. Visualizar Boletins Registrados")

        elif opcao == "7":
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            print()

def menu_principal(usuario, usuarios):
    while True:
        limpar_terminal()
        exibir_mensagem_borda(f"Bem-vindo(a), {usuario}!")
        print("\nMenu Principal:")
        print("1. Fazer Denúncia")
        print("2. Prevenção")
        print("3. Configurações")
        print("4. Suporte")
        print("5. Deletar Usuário")
        print("6. Sair")
        print()
        opcao = input("Escolha uma opção (1, 2, 3, 4, 5 ou 6): ")
        if opcao == "1":
            menu_denuncia(usuario)
        elif opcao == "2":
            menu_prevencao(usuario)
        elif opcao == "3":
            menu_configuracoes()
        elif opcao == "4":
            exibir_menu_suporte()
        elif opcao == "5":
            deletar_usuario(usuarios)
        elif opcao == "6":
            print("Saindo... Até mais!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            print()

def main():
    usuarios = carregar_usuarios()
    while True:
        limpar_terminal()
        ascii_art = """
╭
░█████╗░██╗░░██╗███████╗  ██████╗░███████╗███╗░░██╗██╗░░░██╗███╗░░██╗░█████╗░██╗░█████╗░
██╔══██╗╚██╗██╔╝██╔════╝  ██╔══██╗██╔════╝████╗░██║██║░░░██║████╗░██║██╔══██╗██║██╔══██╗
██║░░██║░╚███╔╝░█████╗░░  ██║░░██║█████╗░░██╔██╗██║██║░░░██║██╔██╗██║██║░░╚═╝██║███████║
██║░░██║░██╔██╗░██╔══╝░░  ██║░░██║██╔══╝░░██║╚████║██║░░░██║██║╚████║██║░░██╗██║██╔══██║
╚█████╔╝██╔╝╚██╗███████╗  ██████╔╝███████╗██║░╚███║╚██████╔╝██║░╚███║╚█████╔╝██║██║░░██║
░╚════╝░╚═╝░░╚═╝╚══════╝  ╚═════╝░╚══════╝╚═╝░░╚══╝░╚═════╝░╚═╝░░╚══╝░╚════╝░╚═╝╚═╝░░╚═╝
"""

        print(ascii_art)

        exibir_mensagem_borda("Bem-vindo(a) ao Oxe!Denúncia, o seu Sistema de Denúncias e Prevenção de Crimes!")
        print()
        print("1. Cadastrar Usuário")
        print("2. Fazer Login")
        print("3. Redefinir Senha")
        print("4. Sair")
        print()
        opcao = input("Escolha uma opção (1, 2, 3 ou 4): ")
        if opcao == "1":
            cadastrar_usuario(usuarios)
        elif opcao == "2":
            fazer_login(usuarios)
        elif opcao == "3":
            redefinir_senha(usuarios)
        elif opcao == "4":
            print("Saindo... Até mais!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            print()

if __name__ == "__main__":
    main()

