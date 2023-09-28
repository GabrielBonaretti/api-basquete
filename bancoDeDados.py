import sqlite3
from models import League, Team
import json

def conectar():
    connection = sqlite3.connect('psqlite3.db')
    
    # Create the 'ligas_de_basquete' table if not exists
    connection.execute("""CREATE TABLE IF NOT EXISTS ligas_de_basquete (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(255) NOT NULL
    );"""
    )

    # Create the 'times_de_basquete' table if not exists
    connection.execute("""CREATE TABLE IF NOT EXISTS times_de_basquete (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        liga_id INT NOT NULL,
        nome VARCHAR(255) NOT NULL,
        FOREIGN KEY (liga_id) REFERENCES ligas_de_basquete(id)
    );"""
    )
    return connection

def desconectar(connection, cursor):
    cursor.close()
    connection.close()

# SELECT

def listar_times():
    '''
    Busca todas os times registrados no database 'times_de_basquete'
    '''
    # inicia a conexao e cursor
    connection = conectar()
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM times_de_basquete')
    times = cursor.fetchall()
    
    # fecha a conexao com o cursor
    desconectar(connection, cursor)
    return times

def buscar(table , id = None, nome = None):
    """
    Verifica se o a busca foi feita por id ou nome e a tabela no qual foi feito a busca
    """

    # inicia a conexao e cursor
    connection = conectar()
    cursor = connection.cursor()
    
    if id:
        cursor.execute(f'SELECT * FROM {table} WHERE id == {id}')
        search_time = cursor.fetchall()
        return search_time


    elif nome:
        cursor.execute(f"SELECT * FROM {table} WHERE nome LIKE '%{nome}%'")
        search_time = cursor.fetchall()
        return search_time

    # fecha a conexao com o cursor
    desconectar(connection, cursor)

def listar_ligas():
    '''
    Busca todas as ligas registradas na database 'ligas_de_basquete'
    '''

    # inicia a conexao e cursor
    connection = conectar()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM ligas_de_basquete')
    ligas = cursor.fetchall()

    # fecha a conexao com o cursor
    desconectar(connection, cursor)
    return ligas

def listar_times_liga(search, type_search):
    """
    Buscar todos os times que estao na liga pesquisada. 
    Alem de verificar o tipo de procura da busca e procurar a partir desse tipo  
    """

    # inicia a conexao e cursor
    connection = conectar()
    cursor = connection.cursor()

    if type_search == 'id':
        cursor.execute(f'SELECT * FROM times_de_basquete WHERE liga_id == {search}')
        times_liga = cursor.fetchall()
    elif type_search == 'name':
        cursor.execute(f"""
                       SELECT DISTINCT t.liga_id, t.nome 
                       FROM times_de_basquete as t 
                       INNER JOIN ligas_de_basquete as l
                       ON (t.liga_id == l.id)
                       WHERE l.nome LIKE '%{search}%'
                       """)
        times_liga = cursor.fetchall()

    # fecha a conexao com o cursor
    desconectar(connection, cursor)

    return times_liga

# INSERT

def inserir_time(team: Team):
    """
    Insere um time na tabela "times_de_basquete", a partir do model team. 
    """

    # inicia a conexao e cursor
    connection = conectar()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO times_de_basquete (liga_id, nome) VALUES ({team.liga_id}, '{team.nome}');")
    connection.commit()
    
    # verifica se foi criado
    if cursor.rowcount == 1:
        create = True
    else:
        create = False
    
    # fecha a conexao com o cursor
    desconectar(connection, cursor)
    
    return create

def inserir_liga(league: League):
    """
    Insere uma liga na tabela "ligas_de_basquete", a partir do model team. 
    """

    # inicia a conexao e cursor
    connection = conectar()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ligas_de_basquete (nome) VALUES ('{league.nome}');")
    connection.commit()

    # verifica se foi criado
    if cursor.rowcount == 1:
        create = True
    else:
        create = False
    
    # fecha a conexao com o cursor
    desconectar(connection, cursor)
    
    return create

# UPDATE

def upadate_times(team):

    connection = conectar()
    cursor = connection.cursor()

    cursor.execute(f"UPDATE times_de_basquete SET liga_id == {team.liga_id}, nome = '{team.nome}' WHERE id == {team.id}")
    connection.commit()

    if cursor.rowcount == 1:
        updated = True
    else:
        updated = False
    
    desconectar(connection, cursor)

    return updated

def upadate_ligas(league):
    connection = conectar()
    cursor = connection.cursor()

    cursor.execute(f"UPDATE ligas_de_basquete SET nome = '{league.nome}' WHERE id == {league.id}")
    connection.commit()

    if cursor.rowcount == 1:
        updated = True
    else:
        updated = False
    
    desconectar(connection, cursor)
    
    return updated

# DELETE

def delete(table, id):
    connection = conectar()
    cursor = connection.cursor()
    
    cursor.execute(f"DELETE FROM {table} WHERE id == {id}")

    connection.commit()

    if cursor.rowcount == 1:
        deleted = True
    else:
        deleted = False

    desconectar(connection, cursor)
    
    return deleted