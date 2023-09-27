import sqlite3
from models import League, Team

def conectar():
    connection = sqlite3.connect('psqlite3.db')
    
    # Create the 'ligas_de_basquete' table
    connection.execute("""CREATE TABLE IF NOT EXISTS ligas_de_basquete (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(255) NOT NULL
    );"""
    )

    # Create the 'times_de_basquete' table
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
    connection = conectar()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM times_de_basquete')
    times = cursor.fetchall()
    desconectar(connection, cursor)
    return times

def buscar(table , id = None, nome = None):
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

    desconectar(connection, cursor)

def listar_ligas():
    connection = conectar()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM ligas_de_basquete')
    ligas = cursor.fetchall()
    desconectar(connection, cursor)
    return ligas

def listar_times_liga(search, type_search):
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

    desconectar(connection, cursor)

    return times_liga

# INSERT

def inserir_time(team: Team):
    connection = conectar()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO times_de_basquete (liga_id, nome) VALUES ({team.liga_id}, '{team.nome}');")
    connection.commit()

    if cursor.rowcount == 1:
        create = True
    else:
        create = False
    
    desconectar(connection, cursor)
    
    return create

def inserir_liga(league: League):
    connection = conectar()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ligas_de_basquete (nome) VALUES ('{league.nome}');")
    connection.commit()

    if cursor.rowcount == 1:
        create = True
    else:
        create = False
    
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