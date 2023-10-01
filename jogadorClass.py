class Jogador:
    """
    Classe responsável pelas instâncias e métodos dos jogadores.
    bool atirar:
        :param tabuleiro - matriz contendo as posições do submarino
        :return - True para caso o tiro acerte, False caso o tiro erre
    """
    def __init__(self, nome):
        """
        Inicializa uma instância do jogador com um nome, contagem de tiros e submarinos afundados.
        """
        self.nome = nome  # Define o nome do jogador
        self.tiros = 0  # Inicializa a contagem de tiros do jogador
        self.submarinos_afundados = 0  # Inicializa a contagem de submarinos afundados pelo jogador

    def atirar(self, tabuleiro):
        """
        Realiza uma tentativa de tiro do jogador em um tabuleiro.
        :param tabuleiro - matriz contendo as posições do submarino
        :return - True se o tiro acertar um submarino, False se o tiro errar
        """
        while True:
            try:
                linha = int(input(f"{self.nome}, informe a linha para disparar o torpedo: "))  # Solicita a linha do tiro
                coluna = int(input(f"{self.nome}, informe a coluna para disparar o torpedo: "))  # Solicita a coluna do tiro
                if tabuleiro.disparar_torpedo(linha, coluna):
                    print(f"{self.nome} acertou um submarino!")  # Se o tiro acertar, exibe uma mensagem
                    self.tiros += 1  # Incrementa a contagem de tiros
                    self.submarinos_afundados += 1  # Incrementa a contagem de submarinos afundados
                    return True  # Retorna True para indicar que o tiro acertou
                else:
                    print(f"{self.nome} errou o tiro.")  # Se o tiro errar, exibe uma mensagem
                    self.tiros += 1  # Incrementa a contagem de tiros
                    return False  # Retorna False para indicar que o tiro errou
            except ValueError:
                print("Entrada inválida. Digite um número de 0 a 4.")  # Trata exceção de entrada inválida
