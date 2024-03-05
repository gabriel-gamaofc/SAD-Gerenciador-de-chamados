from flask import Flask, render_template, jsonify, request
from flask import Flask, render_template, jsonify, request, redirect, url_for

import mysql.connector

app = Flask(__name__)

# Configurar a conexão com o banco de dados MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='dba',
    password='Sad#Suporte',
    database='expresso_conectado'
)


# Função para verificar o login no banco de dados
def verificar_login(email, senha):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email=%s AND senha=%s", (email, senha))
    usuario = cursor.fetchone()
    cursor.close()
    print("Usuário encontrado:", usuario)
    if usuario:
        return True
    else:
        return False

@app.route('/verificar_login_Rota', methods=['POST'])
def verificar_login_route():
    if request.method == 'POST':
        email = request.form['username']
        senha = request.form['password']
        print("Email recebido:", email)
        print("Senha recebida:", senha)
        usuario = verificar_login(email, senha)
        print("Usuário autenticado:", usuario)
        if usuario:
            return jsonify({"message": "Login bem-sucedido"}), 200
        else:
            return jsonify({"message": "Login inválido"}), 401

    return jsonify({"message": "Método não permitido"}), 405

@app.route('/')
def login():
    return render_template('Login.html')

@app.route('/index')
def index_main():
    return render_template('index.html')


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Rota para servir o arquivo index.html
#@app.route('/')
#def index():
    #return render_template('index.html')

# Rota para abrir Cadastro de maquinas
@app.route('/Cadastro_Maquinas_Pina')
def Cadastro_Maquinas_Pina():
    return render_template('Cadastro_Maquinas_Pina.html')

# Rota para abrir Cadastro de maquinas
@app.route('/Chamados_TI_Pina')
def Chamados_TI_Pina():
    return render_template('Chamados_ti_pina.html')

# Rota para abrir Autenticação centralizada
@app.route('/Autenticacao_Centralizada_Pina')
def Autenticacao_Centralizada_Pina():
    return render_template('Autenticacao_Centralizada_Pina.html')


# Rota para abrir Manutenção Predial pina
@app.route('/Manutencao_Predial_Pina')
def Manutencao_Predial_Pina():
  return render_template('Manutencao_Predial_Pina.html')

# Rota para obter todas as máquinas
@app.route('/api/maquinas')
def get_maquinas():
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM maquinas')
    maquinas = cursor.fetchall()
    cursor.close()
    return jsonify(maquinas)

# Rota para adicionar uma nova máquina
@app.route('/api/maquinas', methods=['POST'])
def add_maquina():
    data = request.json
    orgao = data.get('orgao')
    ip = data.get('ip')
    tombamento = data.get('tombamento')
    guiche = data.get('guiche')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO maquinas (orgao, ip, tombamento, guiche) VALUES (%s, %s, %s, %s)', (orgao, ip, tombamento, guiche))
    connection.commit()
    cursor.close()
    return jsonify(message='Máquina adicionada com sucesso!', id=cursor.lastrowid)

# Rota para atualizar uma máquina existente
@app.route('/api/maquinas/<int:id>', methods=['PUT'])
def update_maquina(id):
    data = request.json
    orgao = data.get('orgao')
    ip = data.get('ip')
    tombamento = data.get('tombamento')
    guiche = data.get('guiche')
    cursor = connection.cursor()
    cursor.execute('UPDATE maquinas SET orgao=%s, ip=%s, tombamento=%s, guiche=%s WHERE id=%s', (orgao, ip, tombamento, guiche, id))
    connection.commit()
    cursor.close()
    return jsonify(message='Máquina atualizada com sucesso!', id=id)

# Rota para excluir uma máquina
@app.route('/api/maquinas/<int:id>', methods=['DELETE'])
def delete_maquina(id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM maquinas WHERE id=%s', (id,))
    connection.commit()
    cursor.close()
    return jsonify(message='Máquina excluída com sucesso!', id=id)


#-----------------------------------------------------------------------------------------------------------ROTAS DO CHAMADO DE TI PIA------------------------------------------------------------------------------------------------#


@app.route('/api/chamados')
def get_chamados():
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM chamados_ti')
    chamados = cursor.fetchall()
    cursor.close()
    return jsonify(chamados)

# Rota para adicionar um novo chamado de T.I.
@app.route('/api/chamados', methods=['POST'])
def add_chamado():
    data = request.json
    orgao = data.get('orgao')
    requerente = data.get('requerente')
    solicitacao = data.get('solicitacao')
    status = data.get('status')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO chamados_ti (orgao, requerente, solicitacao, status) VALUES (%s, %s, %s, %s)', (orgao, requerente, solicitacao, status))
    connection.commit()
    cursor.close()
    return jsonify(message='Chamado de T.I. adicionado com sucesso!', id=cursor.lastrowid)

# Rota para atualizar um chamado de T.I. existente
@app.route('/api/chamados/<int:id>', methods=['PUT'])
def update_chamado(id):
    data = request.json
    orgao = data.get('orgao')
    requerente = data.get('requerente')
    solicitacao = data.get('solicitacao')
    status = data.get('status')
    cursor = connection.cursor()
    cursor.execute('UPDATE chamados_ti SET orgao=%s, requerente=%s, solicitacao=%s, status=%s WHERE id=%s', (orgao, requerente, solicitacao, status, id))
    connection.commit()
    cursor.close()
    return jsonify(message='Chamado de T.I. atualizado com sucesso!', id=id)


# Rota para excluir um chamado de T.I.
@app.route('/api/chamados/<int:id>', methods=['DELETE'])
def delete_chamado(id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM chamados_ti WHERE id=%s', (id,))
    connection.commit()
    cursor.close()
    return jsonify(message='Chamado de T.I. excluído com sucesso!', id=id)




#----------------------------------------------------------------------------------------------------------------Rotas de autenticação centralizada do pina------------------------------------------------------------------------
@app.route('/api/centralizada_pina')
def get_centralizada_pina():
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Aut_cent_pina')
    chamados = cursor.fetchall()
    cursor.close()
    return jsonify(chamados)

# Rota para adicionar um novo login autenticado
@app.route('/api/centralizada_pina', methods=['POST'])
def add_centralizada_pina():
    data = request.json
    orgao = data.get('orgao')
    #print("Olha o orgao: ",data.get('orgao'))
    Login = data.get('Login')
    #print("Olha o Login: ",data.get('Login'))
    Matricula = data.get('Matricula')
    #print("Olha o Matricula: ",data.get('Matricula'))
    status = data.get('status')
    #print("Olha o status: ",data.get('status'))
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Aut_cent_pina (orgao, Login, Matricula, status) VALUES (%s, %s, %s, %s)', (orgao, Login, Matricula, status))
    connection.commit()
    cursor.close()
    return jsonify(message='Login de autenticação adicionado com sucesso!', id=cursor.lastrowid)

# Rota para atualizar um login autenticado existente
@app.route('/api/centralizada_pina/<int:id>', methods=['PUT'])
def update_centralizada_pina(id):
    data = request.json
    orgao = data.get('orgao')
    Login = data.get('Login')
    Matricula = data.get('Matricula')
    status = data.get('status')
    cursor = connection.cursor()
    cursor.execute('UPDATE Aut_cent_pina SET orgao=%s, Login=%s, Matricula=%s, status=%s WHERE id=%s', (orgao, Login, Matricula, status, id))
    connection.commit()
    cursor.close()
    return jsonify(message='Login autenticado e atualizado com sucesso!', id=id)


# Rota para excluir um login autenticado
@app.route('/api/centralizada_pina/<int:id>', methods=['DELETE'])
def delete_centralizada_pina(id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Aut_cent_pina WHERE id=%s', (id,))
    connection.commit()
    cursor.close()
    return jsonify(message='Login autenticado excluído com sucesso!', id=id)


#-------------------------------------------------------------------------------------------------Rotas para chamados prediais do pina ---------------------------------------------------------------------------------
@app.route('/api/chamadosPrediais')
def get_chamadosPrediaisPina():
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Chamado_Predial_Pina')
    chamados = cursor.fetchall()
    cursor.close()
    return jsonify(chamados)

# Rota para adicionar um novo chamado de T.I.
@app.route('/api/chamadosPrediais', methods=['POST'])
def add_chamadosPrediaisPina():
    data = request.json
    orgao = data.get('orgao')
    requerente = data.get('requerente')
    solicitacao = data.get('solicitacao')
    status = data.get('status')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Chamado_Predial_Pina (orgao, requerente, solicitacao, status) VALUES (%s, %s, %s, %s)', (orgao, requerente, solicitacao, status))
    connection.commit()
    cursor.close()
    return jsonify(message='Chamado predial adicionado com sucesso!', id=cursor.lastrowid)

# Rota para atualizar um chamado de T.I. existente
@app.route('/api/chamadosPrediais/<int:id>', methods=['PUT'])
def update_chamadosPrediaisPina(id):
    data = request.json
    orgao = data.get('orgao')
    requerente = data.get('requerente')
    solicitacao = data.get('solicitacao')
    status = data.get('status')
    cursor = connection.cursor()
    cursor.execute('UPDATE Chamado_Predial_Pina SET orgao=%s, requerente=%s, solicitacao=%s, status=%s WHERE id=%s', (orgao, requerente, solicitacao, status, id))
    connection.commit()
    cursor.close()
    return jsonify(message='Chamado prediais atualizado com sucesso!', id=id)


# Rota para excluir um chamado de T.I.
@app.route('/api/chamadosPrediais/<int:id>', methods=['DELETE'])
def delete_chamadosPrediaisPina(id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Chamado_Predial_Pina WHERE id=%s', (id,))
    connection.commit()
    cursor.close()
    return jsonify(message='Chamado prediais excluído com sucesso!', id=id)




if __name__ == '__main__':
    app.run(port=3001)
