from datetime import datetime

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[x] Sair

=> """

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

def depositar():
    global saldo, extrato
    deposito = int(input("Valor do deposito: "))
    data = data_e_hora()
    if deposito > 0:
        saldo += deposito
        dep_extrato = f"Deposito: +R$ {deposito:.2f}   -   Data: {data}"
        extrato.append(dep_extrato)
        print("Depósito realizado com sucesso!")
        print(f"Saldo atual: R$ {saldo:.2f}")
    else:
        print("Valor inválido!")
        print(f"Saldo atual: R$ {saldo:.2f}")  
        
def sacar(LIMITE_SAQUES, limite):
    global saldo, numero_saques, extrato
    valor_saque = int(input("Valor saque: "))
    data = data_e_hora()
    
    data_ult_saque = ""
    data_atual = datetime.now().strftime('%d/%m/%Y')
    
    if numero_saques < LIMITE_SAQUES:
        if valor_saque > 0 and valor_saque <= limite:
            if data_ult_saque == data_atual or data_ult_saque == "":
                numero_saques += 1
                saldo -= valor_saque
                saque_extrato = f"Saque: -R$ {valor_saque:.2f}   -   Data: {data}"
                extrato.append(saque_extrato)
                print(f"Saldo atual: R$ {saldo:.2f}")
                
            else:
                numero_saques = 1
                data_ult_saque = data_atual
                saldo -= valor_saque
                saque_extrato = f"Saque: - R$ {valor_saque:.2f}   -   Data: {data}"
                extrato.append(saque_extrato)
                print(f"Saldo atual: R$ {saldo:.2f}")
        else:
            print("Valor de saque inválido")
    else:
        print("Limite de saques excedido!")
        
def extrato_hist(extrato):
    print("\n================== EXTRATO ==================")
    for transacao in extrato:
        print(transacao)
    print(f"\nSaldo R$ {saldo:.2f}")
    print("\n=============================================")
    

while True:
    opcao = input(menu)
    
    if opcao == "d":
        depositar()
    elif opcao == "s":
        sacar(LIMITE_SAQUES, limite)
    elif opcao == "e":
        extrato_hist(extrato)
    elif opcao == "x":
        break
    else:
        print("Opção inválida!")
