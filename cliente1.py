import socket  # Importa a biblioteca para comunicação em rede (sockets)
import os  # Importa a biblioteca para funcionalidades do sistema operacional
import platform  # Importa a biblioteca para obter informações sobre o sistema operacional
import json  # Importa a biblioteca para serialização e desserialização de dados em JSON
import sys  # Importa a biblioteca para funcionalidades do sistema (necessária para finalizar o programa)
import time  # Importa a biblioteca para pausas/temporizações
from tabuleiroClass import Tabuleiro  # Importa a classe Tabuleiro do arquivo tabuleiroClass.py
from jogadorClass import Jogador  # Importa a classe Jogador do arquivo jogadorClass.py

# Definição da classe Client1
class Client1:
    def __init__(self):
        """
        Inicializa a instância do cliente 1.
        Define o endereço IP e a porta do servidor a ser conectado.
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = '127.0.0.1'  # Endereço IP do servidor
        self.server_port = 12345  # Porta do servidor

    def connect_to_server(self):
        """
        Conecta o cliente 1 ao servidor.
        """
        self.client_socket.connect((self.server_host, self.server_port))  # Conecta ao servidor
        print("Conectado ao servidor.")

    def play_game(self):
        sistema_operacional = platform.system()  # Obtém o sistema operacional em uso

        while True:
            # Verificando o sistema operacional para limpar o terminal
            if sistema_operacional == "Windows":
                os.system('cls')  # Limpa a tela do console no Windows
            else:
                os.system('clear')  # Limpa a tela do console em sistemas UNIX

            print("Batalha de Submarinos - 2 Jogadores\n")

            # Recolhendo nome do jogador 1
            nome_jogador1 = input("Nome do Jogador 1: ")
            self.client_socket.send(nome_jogador1.encode())  # Envia o nome do jogador 1 para o servidor

            # Instanciando as classes de jogador e tabuleiro
            tabuleiro1 = Tabuleiro()  # Cria um objeto Tabuleiro para o jogador 1
            jogador1 = Jogador(nome_jogador1)  # Cria um objeto Jogador para o jogador 1

            print(f"{nome_jogador1}, posicione seus 3 submarinos (linha e coluna de 0 a 4):")

            # Considerando que são 3 submarinos, estou fazendo um loop com range 3
            for _ in range(3):
                # O loop infinito é quebrado com break, portanto quando encontrada uma condição satisfatória, ele quebra o loop
                while True:
                    try:
                        # Recebendo a linha e a coluna escolhida pelo jogador
                        linha = int(input(f"Posição do submarino {_ + 1} (linha): "))
                        coluna = int(input(f"Posição do submarino {_ + 1} (coluna): "))
                        verifica_vitoria = self.client_socket.recv(1024).decode()
                        
                        if verifica_vitoria == 'VITORIA2':
                            print("Jogador 2 afundou todos os seus submarinos.\n Jogo encerrado\n")
                            time.sleep(5)
                            sys.exit()
                        # Se a linha e a coluna forem satisfatórias, ele dá um break e sai do while
                        if tabuleiro1.posicionar_submarino(linha, coluna):
                            break
                        else:
                            # Caso a condição do if não satisfaça, ele bate no else e pede para escolher uma linha e/ou coluna válidas
                            print("Posição inválida ou ocupada. Tente novamente.")
                    except ValueError:
                        print("Entrada inválida. Digite um número de 0 a 4.")

            tabuleiro1_serializado = json.dumps(tabuleiro1.to_dict())  # Serializa o tabuleiro do jogador 1
            self.client_socket.send(tabuleiro1_serializado.encode())  # Envia o tabuleiro serializado para o servidor

            # Faz a mesma coisa do explicado acima
            if sistema_operacional == "Windows":
                os.system('cls')  # Limpa a tela do console no Windows
            else:
                os.system('clear')  # Limpa a tela do console em sistemas UNIX

            tabuleiro_adversario_serializado = self.client_socket.recv(1024).decode()  # Recebe o tabuleiro adversário serializado
            tabuleiro_adversario = json.loads(tabuleiro_adversario_serializado)  # Desserializa o tabuleiro adversário
            tabuleiro2 = Tabuleiro.from_dict(tabuleiro_adversario)  # Cria um objeto Tabuleiro para o tabuleiro adversário

            while True:
                # O jogador 1 escolhe o tiro que irá dar
                jogador1.atirar(tabuleiro2)

                # Caso acerte todos, ele recebe a mensagem de que venceu
                if jogador1.submarinos_afundados == 3:
                    print(f"{nome_jogador1} venceu!")
                    self.client_socket.send("VITORIA1".encode())  # Envia a mensagem de vitória para o servidor
                    time.sleep(5)  # Pausa por 5 segundos
                    sys.exit()  # Finaliza o programa

# Bloco de código que é executado apenas se o script for executado como um programa principal
if __name__ == "__main__":
    # Cria uma instância da classe Client1
    client1 = Client1()

    # Conecta o cliente 1 ao servidor
    client1.connect_to_server()

    # Inicia o jogo do cliente 1
    client1.play_game()
