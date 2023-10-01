"""
Class responsável pelas instâncias e métodos dos jogadores
bool atirar:
    tabuleiro - matriz contendo as posições do submarino
    @return - True para caso o tiro acerte, False caso o tiro erre
"""
class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.tiros = 0
        self.submarinos_afundados = 0

    def atirar(self, tabuleiro):
        while True:
            try:
                linha = int(input(f"{self.nome}, informe a linha para disparar o torpedo: "))
                coluna = int(input(f"{self.nome}, informe a coluna para disparar o torpedo: "))
                if tabuleiro.disparar_torpedo(linha, coluna):
                    print(f"{self.nome} acertou um submarino!")
                    self.tiros += 1
                    self.submarinos_afundados += 1
                    return True
                else:
                    print(f"{self.nome} errou o tiro.")
                    self.tiros += 1
                    return False
            except ValueError:
                print("Entrada inválida. Digite um número de 0 a 4.")