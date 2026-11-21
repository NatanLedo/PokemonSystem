import sqlite3

conexao = sqlite3.connect("database/pokedex.db")
cursor = conexao.cursor()

cursor.execute("DELETE FROM pokemon")
cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'pokemon'")

conexao.commit()
conexao.close()

print("Todos os Pokémon foram apagados!")