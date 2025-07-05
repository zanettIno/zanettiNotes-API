from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from models import bancoDeDados

app = Flask(__name__)
CORS(app)
bancoDeDados()

def conectar_bd():
    conexao = sqlite3.connect('zanettiNotes.db')
    conexao.row_factory = sqlite3.Row
    return conexao

@app.route('/')
def index():
    return 'API rodando daora!'

@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    conexao = conectar_bd()

    try:
        conexao.execute('''
            INSERT INTO usuario (nome_user, email_user, senha_user)
            VALUES (?, ?, ?)''', 
            (data['nome'], data['email'], data['senha']))
        conexao.commit()
        return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email já cadastrado!'}), 400
    
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    conexao = conectar_bd()

    usuario = conexao.execute('''
        SELECT * FROM usuario WHERE email_user = ? AND senha_user = ?''', 
        (data['email'], data['senha'])).fetchone()
    
    if usuario:
        return jsonify({'message': 'Login bem-sucedido!'}), 200
    else:
        return jsonify({'error': 'Email ou senha incorretos!'}), 401
    
@app.route('/tarefa', methods=['GET, POST'])
def tarefa():
    if request.method == 'POST':
        return criar_tarefa()
    else:
        return listar_tarefas()

# POST 
def criar_tarefa():
    data = request.get_json()
    conexao = conectar_bd()

    try:
        conexao.execute('''
            INSERT INTO tarefa (titulo_taf, desc_taf, data_taf, status_taf, id_user)
            VALUES (?, ?, ?, ?, ?)''', 
            (data['titulo'], data['descricao'], data['data'], data[1], data['id_user']))
        conexao.commit()
        return jsonify({'message': 'Tarefa criada com sucesso!'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400
    
# GET
def listar_tarefas():
    conexao = conectar_bd()
    tarefas = conexao.execute('SELECT * FROM tarefa').fetchall()
    conexao.close()
    
    return jsonify([dict(tarefa) for tarefa in tarefas]), 200

if __name__ == '__main__':
    app.run(debug=False, port=0000)