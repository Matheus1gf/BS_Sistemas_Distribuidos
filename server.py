# Importando bibliotecas necessárias
import socket  # Biblioteca para comunicação em rede
import os  # Biblioteca para funcionalidades do sistema operacional
import platform  # Biblioteca para informações sobre o sistema operacional
import time  # Biblioteca para pausas/temporizações
import json  # Biblioteca para serialização e desserialização de dados em JSON
import sys  # Biblioteca para funcionalidades do sistema
from jogadorClass import Jogador # Importando class Jogador que está em jogadorClass.py
from tabuleiroClass import Tabuleiro # Importando class Tabuleiro que está em tabuleiroClass.py

class Server:
    """
    Class responsável pela criação e tratativa do servidor com os clientes,
    aqui cria-se os clientes, suas conexões com o servidor e implementa toda execução e regra do jogo,
    tal como a criação dos tabuleiros
    """
    def __init__(self):
        """
        Inicialização do servidor.
        Criação do socket do servidor, definição do host e da porta,
        e aguardando conexões dos jogadores.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'  # Endereço IP do servidor (localhost)
        self.port = 12345  # Número da porta que o servidor usará
        self.server_socket.bind((self.host, self.port))  # Associa o socket do servidor ao endereço e porta
        self.server_socket.listen(2) # Inicia a escuta do servidor para até 2 conexões (jogadores)
        print("Aguardando conexões dos jogadores...")

    def accept_players(self):
        """
        accept_players:
        Aceita a conexão dos jogadores e retorna os sockets dos jogadores.

        Essa função cria dois sockets, um para cada jogador, e os aceita como jogadores.
        Em seguida, retorna os sockets dos jogadores.

        :return: Um par de sockets, representando o jogador 1 e o jogador 2.
        """
        player1_socket, player1_address = self.server_socket.accept()  # Aceita conexão do jogador 1
        player2_socket, player2_address = self.server_socket.accept()  # Aceita conexão do jogador 2
        print(f"Jogador 1 conectado: {player1_address}")  # Exibe informações de conexão do jogador 1
        print(f"Jogador 2 conectado: {player2_address}")  # Exibe informações de conexão do jogador 2
        return player1_socket, player2_socket  # Retorna os sockets dos jogadores

    def start_game(self):
        """
        Função principal que inicia o jogo e gerencia a lógica do servidor.

        Essa função é responsável por controlar a execução do jogo. Ela gerencia a troca de informações
        entre os jogadores, a atualização dos tabuleiros e a detecção do vencedor.

        """
        sistema_operacional = platform.system() # Obtém o sistema operacional em uso

       # Aqui é onde são impressos os tabuleiros
        nome_jogador1 = player1_socket.recv(1024).decode()  # Recebe o nome do jogador 1
        nome_jogador2 = player2_socket.recv(1024).decode()  # Recebe o nome do jogador 2

        tabuleiro1_serializado = player1_socket.recv(1024).decode()  # Recebe o tabuleiro serializado do jogador 1
        tabuleiro1_load = json.loads(tabuleiro1_serializado)  # Desserializa o tabuleiro
        tabuleiro1 = Tabuleiro.from_dict(tabuleiro1_load)  # Cria o objeto Tabuleiro do jogador 1 a partir do tabuleiro desserializado

        tabuleiro2_serializado = player2_socket.recv(1024).decode()  # Recebe o tabuleiro serializado do jogador 2
        tabuleiro2_load = json.loads(tabuleiro2_serializado)  # Desserializa o tabuleiro
        tabuleiro2 = Tabuleiro.from_dict(tabuleiro2_load)  # Cria o objeto Tabuleiro do jogador 2 a partir do tabuleiro desserializado

        while True:
            print(f"{nome_jogador1}'s Tabuleiro:")  # Exibe o tabuleiro do jogador 1
            tabuleiro1.imprimir()  # Imprime o tabuleiro do jogador 1
            print("\n")
            print(f"{nome_jogador2}'s Tabuleiro:")  # Exibe o tabuleiro do jogador 2
            tabuleiro2.imprimir()  # Imprime o tabuleiro do jogador 2

            # Irá esperar 5 segundos antes de limpar o terminal
            time.sleep(5)
            if sistema_operacional == "Windows":
                os.system('cls')  # Limpa a tela do console no Windows
            else:
                os.system('clear')  # Limpa a tela do console em sistemas UNIX

            tabuleiro2_serializado = json.dumps(tabuleiro2.to_dict())  # Serializa o tabuleiro do jogador 2
            player1_socket.send(tabuleiro2_serializado.encode())  # Envia o tabuleiro serializado para o jogador 1

            tabuleiro1_serializado = json.dumps(tabuleiro1.to_dict())  # Serializa o tabuleiro do jogador 1
            player2_socket.send(tabuleiro1_serializado.encode())  # Envia o tabuleiro serializado para o jogador 2

            print(f"{nome_jogador1}'s Tabuleiro:")  # Exibe o tabuleiro do jogador 1
            tabuleiro1.imprimir()  # Imprime o tabuleiro do jogador 1
            print("\n")
            print(f"{nome_jogador2}'s Tabuleiro:")  # Exibe o tabuleiro do jogador 2
            tabuleiro2.imprimir()  # Imprime o tabuleiro do jogador 2

            # Irá esperar 5 segundos antes de limpar o terminal
            time.sleep(5)
            if sistema_operacional == "Windows":
                os.system('cls')  # Limpa a tela do console no Windows
            else:
                os.system('clear')  # Limpa a tela do console em sistemas UNIX

            while True:
                vitoria1 = player1_socket.recv(1024).decode()
                vitoria1_tratada = vitoria1.split(":")
                vitoria2 = player2_socket.recv(1024).decode()
                vitoria2_tratada = vitoria2.split(":")
                print(vitoria1_tratada)
                print(vitoria2_tratada)

                if len(vitoria1_tratada) == 2 and len(vitoria2_tratada) == 2:
                    vitoria1_horario, vitoria1_acao = vitoria1_tratada[1], vitoria1_tratada[0]
                    vitoria2_horario, vitoria2_acao = vitoria2_tratada[1], vitoria2_tratada[0]
                    print(vitoria1_horario)
                    print(vitoria1_acao)
                    print(vitoria2_horario)
                    print(vitoria2_acao)
                    if vitoria1_acao == 'VITORIA1' and vitoria1_horario < vitoria2_horario:  # Verifica se o jogador 1 venceu
                        print(f"{nome_jogador1} venceu! {nome_jogador2}'s submarinos foram afundados.")
                        player2_socket.send('VITORIA_CLIENTE1'.encode())
                        player1_socket.send('VITORIA_CLIENTE1'.encode())
                        time.sleep(5)
                        player1_socket.close()  # Fecha a conexão do jogador 1
                        player2_socket.close()  # Fecha a conexão do jogador 2
                        sys.exit()  # Finaliza o programa
                    
                    if vitoria2_acao == 'VITORIA2' and vitoria1_horario > vitoria2_horario:  # Verifica se o jogador 2 venceu
                        print(f"{nome_jogador2} venceu! {nome_jogador1}'s submarinos foram afundados.")
                        player2_socket.send('VITORIA_CLIENTE2'.encode())
                        player1_socket.send('VITORIA_CLIENTE2'.encode())
                        time.sleep(5)
                        player2_socket.close()  # Fecha a conexão do jogador 2
                        player1_socket.close()  # Fecha a conexão do jogador 1
                        sys.exit()  # Finaliza o programa

                

# Bloco de código que é executado apenas se o script for executado como um programa principal
if __name__ == "__main__":
    # Cria uma instância da classe Server
    server = Server()

    # Aceita a conexão dos jogadores e obtém seus sockets
    player1_socket, player2_socket = server.accept_players()

    # Inicia o jogo
    server.start_game()