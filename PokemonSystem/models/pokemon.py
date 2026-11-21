class Pokemon:

    def __init__(self, nome, tipo, nivel, hp, descricao, imagem=None, id=None):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.nivel = nivel
        self.hp = hp
        self.descricao = descricao
        self.imagem = imagem