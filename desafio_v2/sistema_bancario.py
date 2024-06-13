from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco  = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
               
class Conta:
    def __init__(self, numero, cliente):    
        
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico() 
        self.num_saques = 0
        self.data_ult_saque = ""
        
    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")
        elif valor > 0:
            saldo -= valor
            print(f"\nOperação realizada com sucesso!\nSaldo atual: R$ {self.saldo:.2f}")
            return True
        else:
            print("\nOperação falhou! Valor inválido.")
            return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\nOperação realizada com sucesso!\nSaldo atual: R$ {self._saldo:.2f}")
            return True
        else:
            print("\nOperação falhou! Valor inválido.")
            return False
        
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero=numero, cliente=cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        
    def sacar(self, valor):
        
        data_atual = datetime.now().strftime('%d/%m/%Y')
                
        if data_atual == self.data_ult_saque or self.data_ult_saque == "":
            self.num_saques += 1
            self.data_ult_saque = data_atual
        else:
            self.num_saques = 1
            self.data_ult_saque = data_atual
                                 
        excedeu_limite = valor > self._limite
        excedeu_saque = self.num_saques > self._limite_saques
        
        if excedeu_limite:
            print("\nOperação falhou! Você excedeu o valor limite.")
        elif excedeu_saque:
            print("\nOperação falhou! Você excedeu o limite de saques.")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\
        Agência:\t{self.agencia}
        C/C:\t\t{self.numero}
        Títular:\t{self.cliente.nome}
    """
    
class Historico:
        def __init__(self):
            self._transacoes = []
            
        @property
        def transacoes(self):
            return self._transacoes
        
        def adicionar_transacao(self, transacao):
            self._transacoes.append(
                {
                    "tipo": transacao.__class__.__name__,
                    "valor": transacao.valor,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }
            )          
     
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @property
    @abstractmethod
    def registrar(self, conta):
        pass
    
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
        
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def validar_data(data):
    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def nova_conta(contas, cliente):
    
    numero_conta = len(contas) + 1
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)


def listar_contas(cliente):
    for conta in cliente.contas:
        print("=" * 45)
        print(textwrap.dedent(str(conta)))

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta.")
        return
    
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def depositar(cliente):

    valor = float(input("Informe o valor a ser depositado: "))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(cliente):
    
    valor = float(input("Informe o valor a ser depositado: "))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(cliente):
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n==================== EXTRATO ====================")
    transacoes = conta.historico.transacoes
    
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            if transacao["tipo"] == "Deposito":
                extrato += f"\n{transacao['tipo']}\t+R$ {transacao['valor']:.2f}\t{transacao['data']}"
            elif transacao["tipo"] == "Saque":
                extrato += f"\n{transacao['tipo']}\t\t-R$ {transacao['valor']:.2f}\t{transacao['data']}"
                
            
    print(extrato)
    print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
    print("===================================================")

def limite_caracteres(prompt, limit):
    while True:
        text = input(prompt)
        if len(text) == limit:
            return text
        print(f"Campo inválido, utilize {limit} caracteres.")

def converter_e_validar_cpf():
    while True:
        chave_cpf = limite_caracteres("Informe o CPF (somente números): ", 11)
        break
    cpf = f"{chave_cpf[:3]}.{chave_cpf[3:6]}.{chave_cpf[6:9]}-{chave_cpf[9:11]}"
    return cpf

def entrar_conta(clientes, contas):
    cpf = converter_e_validar_cpf()
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado.")
        return
    
    while True:
        opcao = menu_conta(cliente.nome)
        if opcao == "nc":
            
            nova_conta(contas, cliente)
        
        elif opcao == "lc":
            listar_contas(cliente)
            
        elif opcao == "d":
            depositar(cliente)

        elif opcao == "s":
            sacar(cliente)

        elif opcao == "e":
            exibir_extrato(cliente)
        
        elif opcao == "x":
            print("\nSaindo...")
            break

def cadastrar_cliente(clientes):
    cpf = converter_e_validar_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return
    
    cliente_nome = input("Nome completo: ")
    
    while True:
        cliente_data_nasc = limite_caracteres("Data de nascimento (dd/mm/aaaa): ", 10)
        
        if validar_data(cliente_data_nasc):
            break
        else:
            print("Data de nascimento inválida.")
        
    logradouro = input("Logradouro (nome da rua): ")
    numero = input("Numero: ")
    # bairro = input("Bairro: ")
    # cidade = input("Cidade: ")
    # estado = limite_caracteres("Estado (sigla): ", 2)
    cliente_endereco = f"{logradouro}, {numero}"
    # cliente_endereco = f"{logradouro}, {numero} - {bairro}, {cidade}, {estado}"

    novo_cliente = PessoaFisica(cpf=cpf, nome=cliente_nome, data_nascimento=cliente_data_nasc, endereco=cliente_endereco)
    
    clientes.append(novo_cliente)
        
    print("\n=== Cliente criado com sucesso! ===")
        

def menu_inicial():
    menu = """\n
    ================ MENU ================
    [e]\tEntrar conta
    [c]\tCadastrar usuário
    [x]\tSair
    => """
    return input(textwrap.dedent(menu))

def menu_conta(usuario):
    menu = f"""\n
    ================ MENU ================
    Bem vindo, {usuario}!
    
    [nc]\tNova conta
    [lc]\tListar contas
    [d]\tDepositar
    [s]\tSacar
    [e]\tExibir extrato
    [x]\tSair
    => """
    return input(textwrap.dedent(menu))

def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu_inicial()
        
        if opcao == "e":
            
            entrar_conta(clientes, contas)
        elif opcao == "c":
            cadastrar_cliente(clientes)
        elif opcao == "x":
            break
        else:
            print("\nOpção inválida.")
main()