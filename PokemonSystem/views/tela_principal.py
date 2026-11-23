import tkinter as tk
from tkinter import ttk, messagebox
from services.imagem_api import ImagemAPI
from PIL import Image, ImageTk
from io import BytesIO
from models.pokemon import Pokemon
from dao.pokemon_dao import PokemonDAO


class TelaPrincipal:

    def __init__(self, janela):

        self.janela = janela
        self.janela.title("Sistema Pokemon")
        self.janela.geometry("1000x750")
        self.janela.minsize(850, 650)

        self.imagem_tk = None
        self.dao = PokemonDAO()
        self.api = ImagemAPI()

        self.criar_interface()
        self.listar()

    
    def criar_interface(self):
        

        # Personalizacao da janela
        self.janela.configure(bg="#F1F4F8")

        estilo = ttk.Style(self.janela)
        estilo.theme_use("clam")

        estilo.configure(
            "Pokemon.Treeview",
            background="#FFFFFF",
            foreground="#263238",
            rowheight=30,
            fieldbackground="#FFFFFF",
            font=("Arial", 10)
        )

        estilo.configure(
            "Pokemon.Treeview.Heading",
            background="#263B5A",
            foreground="#FFFFFF",
            font=("Arial", 10, "bold"),
            padding=8
        )

        estilo.map(
            "Pokemon.Treeview",
            background=[("selected", "#B8D8F0")],
            foreground=[("selected", "#172B4D")]
        )

        frame_titulo = tk.Frame(
        self.janela,
        bg="#F1F4F8"
        )
        frame_titulo.pack(pady=15)

        tk.Label(
        frame_titulo,
        text="POKEMON SYSTEM",
        font=("Arial", 24, "bold"),
        bg="#F1F4F8",
        fg="#263B5A"
    ).pack()


        # Campos
        frame_campos = tk.Frame(
            self.janela,
            bg="#FFFFFF",
            padx=15,
            pady=10
        )
        frame_campos.pack(pady=10)

    
        
        campos = [
            ("ID:", 0),
            ("Nome:", 1),
            ("Tipo:", 2),
            ("Nivel:", 3),
            ("HP:", 4),
            ("Descricao:", 5)
        ]

        for texto, linha in campos:
            tk.Label(
                frame_campos,
                text=texto,
                bg="#FFFFFF",
                fg="#263B5A",
                font=("Arial", 10, "bold")
            ).grid(row=linha, column=0, padx=5, pady=6, sticky="e")

        self.id = tk.Entry(
            frame_campos,
            width=30,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )
        self.id.grid(row=0, column=1, padx=5, pady=6)

        self.nome = tk.Entry(
            frame_campos,
            width=30,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )
        self.nome.grid(row=1, column=1, padx=5, pady=6)

        self.tipo = tk.Entry(
            frame_campos,
            width=30,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )
        self.tipo.grid(row=2, column=1, padx=5, pady=6)

        self.nivel = tk.Entry(
            frame_campos,
            width=30,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )
        self.nivel.grid(row=3, column=1, padx=5, pady=6)

        self.hp = tk.Entry(
            frame_campos,
            width=30,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )
        self.hp.grid(row=4, column=1, padx=5, pady=6)

        self.descricao = tk.Entry(
            frame_campos,
            width=30,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )
        self.descricao.grid(row=5, column=1, padx=5, pady=6)

        # Botoes
        frame_botoes = tk.Frame(
            self.janela,
            bg="#F1F4F8"
        )
        frame_botoes.pack(pady=8)

        botoes = [
            ("Cadastrar", self.cadastrar, "#27864A"),
            ("Buscar", self.buscar, "#2878B5"),
            ("Atualizar", self.atualizar, "#D68A25"),
            ("Excluir", self.excluir, "#C44545"),
            ("Listar todos", self.listar, "#263B5A"),
            ("Limpar", self.limpar, "#687783")
        ]

        for coluna, (texto, comando, cor) in enumerate(botoes):
            tk.Button(
                frame_botoes,
                text=texto,
                width=12,
                command=comando,
                bg=cor,
                fg="#FFFFFF",
                activebackground="#40566F",
                activeforeground="#FFFFFF",
                font=("Arial", 9, "bold"),
                relief="flat",
                cursor="hand2",
                pady=7
            ).grid(row=0, column=coluna, padx=4)

        # Imagem
        self.label_imagem = tk.Label(
            self.janela,
            text="Imagem do Pokemon",
            bg="#F1F4F8",
            fg="#263B5A",
            font=("Arial", 11, "bold")
        )
        self.label_imagem.pack(pady=8)

        # Tabela
        frame_tabela = tk.Frame(
            self.janela,
            bg="#FFFFFF",
            padx=5,
            pady=5
        )
        frame_tabela.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        colunas = (
            "id",
            "nome",
            "tipo",
            "nivel",
            "hp",
            "descricao"
        )

        self.tabela = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show="headings",
            height=10,
            style="Pokemon.Treeview"
        )

        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("tipo", text="Tipo")
        self.tabela.heading("nivel", text="Nivel")
        self.tabela.heading("hp", text="HP")
        self.tabela.heading("descricao", text="Descricao")

        self.tabela.column("id", width=45, anchor="center")
        self.tabela.column("nome", width=130)
        self.tabela.column("tipo", width=100)
        self.tabela.column("nivel", width=70, anchor="center")
        self.tabela.column("hp", width=70, anchor="center")
        self.tabela.column("descricao", width=350)

        # Barras de rolagem
        barra_vertical = ttk.Scrollbar(
            frame_tabela,
            orient="vertical",
            command=self.tabela.yview
        )

        barra_horizontal = ttk.Scrollbar(
            frame_tabela,
            orient="horizontal",
            command=self.tabela.xview
        )

        self.tabela.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        self.tabela.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")

        frame_tabela.grid_rowconfigure(0, weight=1)
        frame_tabela.grid_columnconfigure(0, weight=1)

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar
        )


    def cadastrar(self):

        try:
            nome = self.nome.get().strip()
            tipo = self.tipo.get().strip()
            nivel = int(self.nivel.get())
            hp = int(self.hp.get())
            descricao = self.descricao.get().strip()

            if not nome or not tipo or not descricao:
                messagebox.showwarning(
                    "Aviso",
                    "Preencha todos os campos."
                )
                return

            if nivel <= 0 or hp <= 0:
                messagebox.showwarning(
                    "Aviso",
                    "Nivel e HP nao podem ser zero ou negativos."
                )
                return

            imagem = self.api.buscar_imagem(nome)

            if imagem is None:
                messagebox.showerror(
                    "Erro",
                    "Nao foi possivel encontrar a imagem desse Pokemon."
                )
                return

            pokemon = Pokemon(
                nome,
                tipo,
                nivel,
                hp,
                descricao,
                imagem
            )

            self.dao.cadastrar(pokemon)

            messagebox.showinfo(
                "Sucesso",
                "Pokemon cadastrado com sucesso!"
            )

            self.limpar()
            self.listar()

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Nivel e HP devem ser numeros."
            )

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def buscar(self):

        try:
            id_pokemon = int(self.id.get())

            pokemon = self.dao.buscar_por_id(id_pokemon)

            if pokemon:

                self.limpar_campos()

                self.id.insert(0, pokemon[0])
                self.nome.insert(0, pokemon[1])
                self.tipo.insert(0, pokemon[2])
                self.nivel.insert(0, pokemon[3])
                self.hp.insert(0, pokemon[4])
                self.descricao.insert(0, pokemon[5])

                self.exibir_imagem(pokemon[6])

            else:
                messagebox.showinfo(
                    "Aviso",
                    "Pokemon nao encontrado."
                )

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Digite um ID valido."
            )

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def atualizar(self):

        try:
            id_pokemon = int(self.id.get())

            nome = self.nome.get().strip()
            tipo = self.tipo.get().strip()
            nivel = int(self.nivel.get())
            hp = int(self.hp.get())
            descricao = self.descricao.get().strip()

            if not nome or not tipo or not descricao:
                messagebox.showwarning(
                    "Aviso",
                    "Preencha todos os campos."
                )
                return

            if nivel <= 0 or hp <= 0:
                messagebox.showwarning(
                    "Aviso",
                    "Nivel e HP nao podem ser zero ou negativos."
                )
                return
            
            imagem = self.api.buscar_imagem(nome)
            if imagem is None:
                messagebox.showerror(
                    "Erro",
                    "Nao foi possivel encontrar a imagem desse Pokemon."
                )
                return

            pokemon = Pokemon(
                nome,
                tipo,
                nivel,
                hp,
                descricao,
                imagem,
                id=id_pokemon
            )

            resultado = self.dao.atualizar(pokemon)

            if resultado > 0:

                messagebox.showinfo(
                    "Sucesso",
                    "Pokemon atualizado!"
                )

                self.limpar()
                self.listar()

            else:
                messagebox.showinfo(
                    "Aviso",
                    "Nenhuma alteracao realizada."
                )

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Verifique o ID, nivel e HP."
            )

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def excluir(self):

        try:
            id_pokemon = int(self.id.get())

            pokemon = self.dao.buscar_por_id(id_pokemon)

            if not pokemon:
                messagebox.showinfo(
                    "Aviso",
                    "Pokemon nao encontrado."
                )
                return

            confirmar = messagebox.askyesno(
                "Confirmar",
                "Deseja excluir " + pokemon[1] + "?"
            )

            if confirmar:

                resultado = self.dao.excluir(id_pokemon)

                if resultado > 0:

                    messagebox.showinfo(
                        "Sucesso",
                        "Pokemon excluido!"
                    )

                    self.limpar()
                    self.listar()

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Digite um ID valido."
            )

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def listar(self):

        try:
            # Limpa os registros anteriores da tabela
            for item in self.tabela.get_children():
                self.tabela.delete(item)

            # Busca todos os Pokemons no banco
            pokemons = self.dao.listar()

            # Insere todos os resultados na tabela
            for pokemon in pokemons:

                self.tabela.insert(
                    "",
                    tk.END,
                    values=(
                        pokemon[0],
                        pokemon[1],
                        pokemon[2],
                        pokemon[3],
                        pokemon[4],
                        pokemon[5]
                    )
                )

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def limpar_campos(self):

        self.id.delete(0, tk.END)
        self.nome.delete(0, tk.END)
        self.tipo.delete(0, tk.END)
        self.nivel.delete(0, tk.END)
        self.hp.delete(0, tk.END)
        self.descricao.delete(0, tk.END)

        self.label_imagem.config(
            image="",
            text="Imagem do Pokemon"
        )

        self.imagem_tk = None

    def limpar(self):

        self.limpar_campos()

        self.tabela.selection_remove(
            self.tabela.selection()
        )

    def selecionar(self, evento):

        selecionado = self.tabela.selection()

        if selecionado:

            valores = self.tabela.item(
                selecionado[0],
                "values"
            )

            self.limpar_campos()

            self.id.insert(0, valores[0])
            self.nome.insert(0, valores[1])
            self.tipo.insert(0, valores[2])
            self.nivel.insert(0, valores[3])
            self.hp.insert(0, valores[4])
            self.descricao.insert(0, valores[5])

            pokemon = self.dao.buscar_por_id(
                int(valores[0])
            )

            if pokemon:
                self.exibir_imagem(pokemon[6])

    def exibir_imagem(self, imagem):

        if imagem is None:

            self.label_imagem.config(
                image="",
                text="Imagem nao encontrada"
            )

            self.imagem_tk = None
            return

        try:
            arquivo = Image.open(BytesIO(imagem))
            arquivo = arquivo.resize((120, 120))

            self.imagem_tk = ImageTk.PhotoImage(arquivo)

            self.label_imagem.config(
                image=self.imagem_tk,
                text=""
            )

        except Exception as erro:
            self.label_imagem.config(
                image="",
                text="Erro ao carregar imagem"
            )

            self.imagem_tk = None
            print("Erro ao exibir imagem:", erro)
