import sqlite3
import os

class Conexao:
    def conectar(self):

        caminho = os.path.join(
            os.path.dirname(__file__),
            "pokedex.db"
        )

        conexao = sqlite3.connect(caminho)

        return conexao
