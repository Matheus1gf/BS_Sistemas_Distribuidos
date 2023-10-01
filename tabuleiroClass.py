class Tabuleiro:
    """
    Classe responsável pela aplicabilidade das funções do tabuleiro.
    """
    def __init__(self):
        # Criando o range do tabuleiro
        self.tabuleiro = [[' ' for _ in range(5)] for _ in range(5)]

    def imprimir(self):
        """
        Imprime o tabuleiro na saída padrão.
        """
        print("  0 1 2 3 4")
        for i, linha in enumerate(self.tabuleiro):
            print(i, ' '.join(linha))

    def posicionar_submarino(self, linha, coluna):
        """
        Posiciona um submarino na posição especificada do tabuleiro.
        :param linha - linha na qual o jogador posicionará seu submarino
        :param coluna - coluna na qual o jogador posicionará seu submarino
        :return - True para caso a posição seja válida, False para caso a posição seja inválida
        """
        if 0 <= linha < 5 and 0 <= coluna < 5 and self.tabuleiro[linha][coluna] == ' ':
            self.tabuleiro[linha][coluna] = 'S'
            return True
        else:
            return False

    def disparar_torpedo(self, linha, coluna):
        """
        Realiza um disparo de torpedo na posição especificada do tabuleiro.
        :param linha - linha na qual o jogador está disparando o torpedo
        :param coluna - coluna na qual o jogador está disparando o torpedo
        :return - True para caso o tiro seja válido, False para caso o tiro seja inválido
        """
        if 0 <= linha < 5 and 0 <= coluna < 5:
            if self.tabuleiro[linha][coluna] == 'S':
                self.tabuleiro[linha][coluna] = 'X'
                return True
            elif self.tabuleiro[linha][coluna] == ' ':
                self.tabuleiro[linha][coluna] = 'O'
                return False
        return False
    
    def to_dict(self):
        # Converte o tabuleiro em um dicionário serializável
        return {'tabuleiro': self.tabuleiro}

    @classmethod
    def from_dict(cls, data):
        # Cria um objeto Tabuleiro a partir de um dicionário
        tabuleiro = cls()
        tabuleiro.tabuleiro = data['tabuleiro']
        return tabuleiro
