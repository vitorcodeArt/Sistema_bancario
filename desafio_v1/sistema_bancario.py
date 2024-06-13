from datetime import datetime

login = """
=================== LOGIN ===================
[e] Entrar conta
[c] Criar conta
[x] Sair
=============================================
=> """

menu = """
=================== MENU ====================
[d] Depositar
[s] Sacar
[e] Extrato
[x] Sair
==============================================
=> """

def validar_data(data):
    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def limite_caracteres(prompt, limit):
    while True:
        text = input(prompt)
        if len(text) == limit:
            return text
        print(f"Campo inválido, utilize {limit} caracteres.")

def cpf_existe(clientes, cpf):
    for cliente in clientes:
        if cpf in cliente:
            return True
    return False

def converter_cpf():
    while True:
        chave_cpf = limite_caracteres("Informe o CPF (somente números): ", 11)
        break
    cpf = f"{chave_cpf[:3]}.{chave_cpf[3:6]}.{chave_cpf[6:9]}-{chave_cpf[9:11]}"
    return cpf

def criar_usuario(clientes, chave, contas):


    if cpf_existe(clientes, chave):
        print("CPF já cadastrado.")
        criar_conta(contas, chave)      
        return

    cliente = { chave: {"nome": '', "data_nasc": '', "endereco": '',}}

    cliente_nome = input("Nome completo: ")

    while True:
        cliente_data_nasc = limite_caracteres("Data de nascimento (dd/mm/aaaa): ", 10)

        if validar_data(cliente_data_nasc):
            break
        else:
            print("Data de nascimento inválida.")

    logradouro = input("Logradouro (nome da rua): ")
    numero = input("Numero: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = limite_caracteres("Estado (sigla): ", 2)
    cliente_endereco = f"{logradouro}, {numero} - {bairro}, {cidade}, {estado}"

    cliente[chave]["nome"] = cliente_nome
    cliente[chave]["data_nasc"] = cliente_data_nasc
    cliente[chave]["endereco"] = cliente_endereco

    clientes.append(cliente)

    criar_conta(contas, chave)

def criar_conta(contas, usuario):

    conta = {'agencia': "", 'num_conta': "", "usuario": ""}
    conta["agencia"] = len(contas) + 1
    conta["num_conta"] = "0001"
    conta["usuario"] = usuario

    contas.append(conta)
    for conta in contas:
        print(f"""
=========================================
Agência:\t{conta["agencia"]}
C/C:\t\t{conta["num_conta"]}
Títular:\t{conta["usuario"]}
""")

def data_e_hora():

    data_hora_atual = datetime.now()
    data_hora_em_texto = data_hora_atual.strftime('%d/%m/%Y %H:%M:%S')
    return data_hora_em_texto


usuario = "Jõao"
saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

def depositar(saldo, valor, extrato):

    data = data_e_hora()

    if valor > 0:
        saldo += valor
        dep_extrato = f"Deposito:\t+R$ {valor:.2f}\tData: {data}"
        extrato.append(dep_extrato)
        print("Depósito realizado com sucesso!")
        print(f"Saldo atual: R$ {saldo:.2f}")
    else:
        print("Valor inválido!")
        print(f"Saldo atual: R$ {saldo:.2f}") 
    return saldo, extrato 

def sacar(*, saldo, valor, extrato, numero_saques, LIMITE_SAQUES, limite):
    data = data_e_hora()

    data_ult_saque = ""
    data_atual = datetime.now().strftime('%d/%m/%Y')

    if numero_saques < LIMITE_SAQUES:
        if valor > 0 and valor <= limite:
            if data_ult_saque == data_atual or data_ult_saque == "":
                numero_saques += 1
                saldo -= valor
                saque_extrato = f"Saque:\t\t-R$ {valor:.2f}\tData: {data}"
                extrato.append(saque_extrato)
                print(f"Saldo atual: R$ {saldo:.2f}")

            else:
                numero_saques = 1
                data_ult_saque = data_atual
                saldo -= valor
                saque_extrato = f"Saque: - R$ {valor:.2f}   -   Data: {data}"
                saldo -= valor
                saque_extrato = f"Saque:\t- R$ {valor:.2f}\t\tData: {data}"
                extrato.append(saque_extrato)
                print(f"Saldo atual: R$ {saldo:.2f}")
        else:
            print("Valor de saque inválido")
    else:
        print("Limite de saques excedido!")
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n================== EXTRATO ==================")
    for transacao in extrato:
        print(transacao)
    print(f"\nSaldo\tR$ {saldo:.2f}")
    print("\n=============================================")
    return saldo, extrato


def main():
    clientes = []
    contas = []
    saldo = 0
    extrato = []

    while True:
        home_page = input(login)

        if home_page == "e":
            chave = converter_cpf()
            if cpf_existe(clientes, chave):
                for cliente in clientes:
                    if chave in cliente:
                        usuario_nome = cliente[chave]['nome'].split()
                        print(f"Seja bem vindo, {usuario_nome[0].capitalize()}!")

                while True:
                    opcao = input(menu)
                    if opcao == "d":
                        valor = int(input("Valor do deposito: "))
                        saldo, extrato = depositar(saldo, valor, extrato)
                    elif opcao == "s":
                        valor_saque = int(input("Valor do saque: "))
                        saldo, extrato = sacar(
                            saldo=saldo, 
                            valor=valor_saque, 
                            extrato=extrato, 
                            numero_saques=0, 
                            LIMITE_SAQUES=3, 
                            limite=500
                            )
                    elif opcao == "e":
                        saldo, extrato = exibir_extrato(saldo, extrato=extrato)
                    elif opcao == "x":
                        break
                    else:
                        print("Opção inválida!")

        elif home_page == "c":
            chave = converter_cpf()
            criar_usuario(clientes, chave, contas)
        elif home_page == "x":
            break
        else:
            print("Opção inválida!")
main()    
