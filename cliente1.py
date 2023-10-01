import socket
import os
import platform
import json
import sys
import time
from tabuleiroClass import Tabuleiro
from jogadorClass import Jogador

class Client1:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = '127.0.0.1'  # Endereço IP do servidor
        self.server_port = 12345  # Porta do servidor

    def connect_to_server(self):
        self.client_socket.connect((self.server_host, self.server_port))
        print("Conectado ao servidor.")

    def play_game(self):
        sistema_operacional = platform.system()

        while True:
        # Verificando o sistema operacional para limpar o terminal
            if sistema_operacional == "Windows":
                os.system('cls')
            else:
                os.system('clear')

            print("Batalha de Submarinos - 2 Jogadores\n")
            # Recolhendo nome dos dois jogadores
            nome_jogador1 = input("Nome do Jogador 1: ")
            self.client_socket.send(nome_jogador1.encode())
            # Instanciando as classes de jogador e tabuleiro
            tabuleiro1 = Tabuleiro()
            jogador1 = Jogador(nome_jogador1)
            print(f"{nome_jogador1}, posicione seus 3 submarinos (linha e coluna de 0 a 4):")

            # Considerando que são 3 submarinos, estou fazendo um loop com range 3
            for _ in range(3):
                # O loop infinito é quebrado com break, portanto quando encontrada uma condição satisfatória, ele quebra o loop
                while True:
                    # Tratando o erro de validade de posição
                    try:
                        # Recebendo a linha e a coluna escolhida pelo jogador
                        linha = int(input(f"Posição do submarino {_ + 1} (linha): "))
                        coluna = int(input(f"Posição do submarino {_ + 1} (coluna): "))
                        # Se a linha e a coluna forem satisfatórias, ele dá um break e sai do while
                        if tabuleiro1.posicionar_submarino(linha, coluna):
                            break
                        else:
                            # Caso a condição do if não satisfaça, ele bate no else e pede para escolher uma linha e/ou coluna válidas
                            print("Posição inválida ou ocupada. Tente novamente.")
                    except ValueError:
                        print("Entrada inválida. Digite um número de 0 a 4.")

            tabuleiro1_serializado = json.dumps(tabuleiro1.to_dict())
            self.client_socket.send(tabuleiro1_serializado.encode())

            # Faz a mesma coisa do explicado acima
            if sistema_operacional == "Windows":
                os.system('cls')
            else:
                os.system('clear')

            tabuleiro_adversario_serializado = self.client_socket.recv(1024).decode()
            tabuleiro_adversario = json.loads(tabuleiro_adversario_serializado)
            tabuleiro2 = Tabuleiro.from_dict(tabuleiro_adversario)

            while True:
                # O jogador 1 escolhe o tiro que irá dar
                jogador1.atirar(tabuleiro2)

                # Caso acerte todos ele recebe a mensagem de que venceu
                if jogador1.submarinos_afundados == 3:
                    print(f"{nome_jogador1} venceu!")
                    self.client_socket.send("VITORIA1".encode())
                    time.sleep(5)
                    sys.exit()


if __name__ == "__main__":
    client1 = Client1()
    client1.connect_to_server()
    client1.play_game()
