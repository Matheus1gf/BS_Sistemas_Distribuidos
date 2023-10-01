import socket
import os
import platform
import time
import json
import sys
from jogadorClass import Jogador
from tabuleiroClass import Tabuleiro

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 12345
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print("Aguardando conexões dos jogadores...")

    def accept_players(self):
        player1_socket, player1_address = self.server_socket.accept()
        player2_socket, player2_address = self.server_socket.accept()
        print(f"Jogador 1 conectado: {player1_address}")
        print(f"Jogador 2 conectado: {player2_address}")
        return player1_socket, player2_socket

    def start_game(self):
        sistema_operacional = platform.system()

        # Aqui é onde são impressos os tabuleiros
        nome_jogador1 = player1_socket.recv(1024).decode()
        nome_jogador2 = player2_socket.recv(1024).decode()
        
        tabuleiro1_serializado = player1_socket.recv(1024).decode()
        tabuleiro1_load = json.loads(tabuleiro1_serializado)
        tabuleiro1 = Tabuleiro.from_dict(tabuleiro1_load)
        
        tabuleiro2_serializado = player2_socket.recv(1024).decode()
        tabuleiro2_load = json.loads(tabuleiro2_serializado)
        tabuleiro2 = Tabuleiro.from_dict(tabuleiro2_load)

        jogador1 = Jogador(nome_jogador1)
        jogador2 = Jogador(nome_jogador2)

        while True:
            print(f"{nome_jogador1}'s Tabuleiro:")
            tabuleiro1.imprimir()
            print("\n")
            print(f"{nome_jogador2}'s Tabuleiro:")
            tabuleiro2.imprimir()

            # Irá esperar 5 segundos antes de limpar o terminal
            time.sleep(5)
            if sistema_operacional == "Windows":
                os.system('cls')
            else:
                os.system('clear')

            tabuleiro2_serializado = json.dumps(tabuleiro2.to_dict())
            player1_socket.send(tabuleiro2_serializado.encode())

            tabuleiro1_serializado = json.dumps(tabuleiro1.to_dict())
            player2_socket.send(tabuleiro1_serializado.encode())

            print(f"{nome_jogador1}'s Tabuleiro:")
            tabuleiro1.imprimir()
            print("\n")
            print(f"{nome_jogador2}'s Tabuleiro:")
            tabuleiro2.imprimir()

            # Irá esperar 5 segundos antes de limpar o terminal
            time.sleep(5)
            if sistema_operacional == "Windows":
                os.system('cls')
            else:
                os.system('clear')

            if player2_socket.recv(1024).decode() == 'VITORIA2':
                print(f"{nome_jogador2} venceu! {nome_jogador1}'s submarinos foram afundados.")
                time.sleep(5)
                sys.exit()

            if player1_socket.recv(1024).decode() == 'VITORIA1':
                print(f"{nome_jogador1} venceu! {nome_jogador2}'s submarinos foram afundados.")
                time.sleep(5)
                sys.exit()


if __name__ == "__main__":
    server = Server()
    player1_socket, player2_socket = server.accept_players()
    server.start_game()