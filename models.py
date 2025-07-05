import sqlite3

def bancoDeDados():
    conexao = sqlite3.connect('zanettiNotes.db')
    c = conexao.cursor()

    # TABELA DE USUARIO  
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
        id_user         INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_user       TEXT NOT NULL,
        email_user      TEXT NOT NULL UNIQUE,
        senha_user      TEXT NOT NULL)
    ''')

    # TABELA DE TAREFAS
    c.execute('''
        CREATE TABLE IF NOT EXISTS tarefa (
            id_taf          INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo_taf      TEXT NOT NULL,
            desc_taf        TEXT NOT NULL,
            data_taf        TEXT NOT NULL,
            status_taf      INTEGER NOT NULL,
            id_user         INTEGER NOT NULL,
            FOREIGN KEY (id_user) REFERENCES usuario(id_user))
    ''')

    # TABELA DE LISTAS
    c.execute('''
        CREATE TABLE IF NOT EXISTS lista (
            id_lista        INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo_lista    TEXT NOT NULL,
            id_user         INTEGER NOT NULL,
            id_taf          INTEGER NOT NULL,
            FOREIGN KEY (id_user)   REFERENCES usuario(id_user),
            FOREIGN KEY (id_taf)    REFERENCES tarefa(id_taf))
    ''')

    conexao.commit()
    conexao.close()