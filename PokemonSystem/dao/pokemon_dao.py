from database.conexao import Conexao

class PokemonDAO:

    def cadastrar(self, pokemon):

        conexao = Conexao()
        banco = conexao.conectar()

        cursor = banco.cursor()

        comando = """
        INSERT INTO pokemon
        (nome, tipo, nivel, hp, descricao, imagem)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        valores = (
            pokemon.nome,
            pokemon.tipo,
            pokemon.nivel,
            pokemon.hp,
            pokemon.descricao,
            pokemon.imagem
        )

        cursor.execute(comando, valores)

        banco.commit()

        cursor.close()
        banco.close()

        print("Pokemon cadastrado com sucesso!")

    def listar(self):

        conexao = Conexao()
        banco = conexao.conectar()

        cursor = banco.cursor()

        comando = """
        SELECT id, nome, tipo, nivel, hp, descricao, imagem
        FROM pokemon
        """

        cursor.execute(comando)

        resultado = cursor.fetchall()

        cursor.close()
        banco.close()

        return resultado

    def buscar_por_id(self, id):

        conexao = Conexao()
        banco = conexao.conectar()

        cursor = banco.cursor()

        comando = """
        SELECT id, nome, tipo, nivel, hp, descricao, imagem
        FROM pokemon
        WHERE id = ?
        """

        valores = (id,)

        cursor.execute(comando, valores)

        resultado = cursor.fetchone()

        cursor.close()
        banco.close()

        return resultado

    def atualizar(self, pokemon):

        conexao = Conexao()
        banco = conexao.conectar()

        cursor = banco.cursor()

        comando = """
        UPDATE pokemon
        SET nome = ?,
            tipo = ?,
            nivel = ?,
            hp = ?,
            descricao = ?,
            imagem = ?
        WHERE id = ?
        """

        valores = (
            pokemon.nome,
            pokemon.tipo,
            pokemon.nivel,
            pokemon.hp,
            pokemon.descricao,
            pokemon.imagem,
            pokemon.id
        )

        cursor.execute(comando, valores)

        banco.commit()

        linhas = cursor.rowcount

        cursor.close()
        banco.close()

        return linhas

    def excluir(self, id):

        conexao = Conexao()
        banco = conexao.conectar()

        cursor = banco.cursor()

        comando = """
        DELETE FROM pokemon
        WHERE id = ?
        """

        valores = (id,)

        cursor.execute(comando, valores)

        banco.commit()

        linhas = cursor.rowcount

        cursor.close()
        banco.close()

        return linhas
