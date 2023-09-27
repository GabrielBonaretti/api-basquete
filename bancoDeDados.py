# def inserir_dados():
#     connection = conectar()

#     with open('db.json') as db:
#         data = json.load(db)

#     connection.execute(f"INSERT INTO ligas_de_basquete (nome) VALUES ('NBA')")
#     connection.execute(f"INSERT INTO ligas_de_basquete (nome) VALUES ('NBB')")

#     for item in data:

#         if data[item]['legue'] == 'NBA':
#             legue_id = 1
#         else:
#             legue_id = 2
        
#         connection.execute(f"INSERT INTO times_de_basquete (liga_id, nome) VALUES ({legue_id}, '{data[item]['name']}')")
#     connection.commit()

#     desconectar(connection, cursor)

import sqlite3
import json
from models import League

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

def buscar_id(id, table):
    connection = conectar()
    cursor = connection.cursor()

    try:
        cursor.execute(f'SELECT * FROM {table} WHERE id == {id}')
        search_time = cursor.fetchall()
        return search_time
    
    except:
       print("error")

    finally:
        desconectar(connection, cursor)

def buscar_nome(nome, table):
    connection = conectar()
    cursor = connection.cursor()

    try:
        cursor.execute(f"SELECT * FROM {table} WHERE nome LIKE '%{nome}%'")
        search_time = cursor.fetchall()
        return search_time
    
    except:
       print("error")

    finally:
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

def inserir_time(league: League):
    connection = conectar()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ligas_de_basquete (nome) VALUES ('{league.nome}');")
    connection.commit()
    desconectar(connection, cursor)

# def inserir_liga():
#     connection = conectar()
#     cursor = connection.cursor()

#     nome = input("Informe o nome da liga: ")

#     cursor.execute(f"INSERT INTO ligas_de_basquete (nome) VALUES ('{nome}');")
#     connection.commit()

#     if cursor.rowcount == 1:
#         print("A liga foi inserida no banco de dados.")
#     else:
#         print("A liga não foi inserida no banco de dados.")

#     desconectar(connection, cursor)
