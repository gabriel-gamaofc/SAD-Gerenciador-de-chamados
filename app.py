from flask import Flask, render_template, jsonify, request
from flask import Flask, render_template, jsonify, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import csv
from datetime import datetime




import mysql.connector

app = Flask(__name__)

# Configurar a conexão com o banco de dados MySQL
connection = mysql.connector.connect(
    host='10.1.106.8',
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
    #print("Usuário encontrado: ",usuario)
    print("Usuário encontrado:", email)
    if usuario:
        return True
    else:
        return False

@app.route('/verificar_login_Rota', methods=['POST'])
def verificar_login_route():
    if request.method == 'POST':
        email = request.form['username']
        senha = request.form['password']
        #print("Email recebido:", email)
        #print("Senha recebida:", senha)
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


@app.route('/geral_pina')
def sit_geral_Pina():
    return render_template('principal_sit_geral_Ecpina.html')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
      # Extrair o ID da planilha do URL
    sheet_url = 'https://docs.google.com/spreadsheets/d/1kScU9vffzZh76fUDMukYZF35j6MTGZc6ebP66KPbCEI/edit?usp=sharing'
    
    sheet_id = sheet_url.split('/')[-2]

    # URL da API do Google Sheets
    api_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

    # Faça uma solicitação GET para a API do Google Sheets
    response = requests.get(api_url)

    # Verifique se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Obtenha as respostas da planilha em formato CSV
        responses = response.text.splitlines()

        # Inicializar a conexão com o banco de dados
        connection = mysql.connector.connect(
           host='localhost',
           user='dba',
           password='Sad#Suporte',
           database='expresso_conectado'
        )
        
        # Criar o cursor
        cursor = connection.cursor()

        print("Respostas obtidas com sucesso:")
        for index, response in enumerate(responses[1:], start=2):
            print(f"Resposta {index}: {response}")

            # Usar csv.reader para dividir os campos
            response_data = next(csv.reader([response], delimiter=',', quotechar='"'))

            # Se o comprimento for menor que 4, ignore esta resposta
            if len(response_data) < 4:
                print(f"Resposta {index} não contém dados relevantes. Ignorando...")
                continue

             # Obter os campos relevantes
            data_solicitacao = datetime.strptime(response_data[0], '%m/%d/%Y %H:%M:%S')
            orgao = response_data[1]
            requerente = response_data[2]
            solicitacao = response_data[3]
            tipo = response_data[4]
           
            print(f"Dados relevantes: orgao={orgao}, requerente={requerente},tipo={tipo}, solicitacao={solicitacao}")

            # Verificar se a resposta já existe no banco de dados
            sql_check = "SELECT COUNT(*) FROM chamados_ti WHERE orgao = %s AND requerente = %s AND solicitacao = %s AND DATE(Data_Abertura) = DATE(%s)"
            values_check = (orgao, requerente, solicitacao, data_solicitacao)
            cursor.execute(sql_check, values_check)
            result = cursor.fetchone()

            # Se não houver registros correspondentes, inserir a resposta
            if result[0] == 0:
                sql_insert = "INSERT INTO chamados_ti (orgao, requerente,tipo, solicitacao, status) VALUES (%s, %s,%s, %s, 'Não visto')"
                values_insert = (orgao, requerente, tipo, solicitacao)
                cursor.execute(sql_insert, values_insert)
                print(f"Resposta {index} inserida no banco de dados com sucesso.")

        # Commit das alterações
        connection.commit()

        # Fechar a conexão com o banco de dados
        connection.close()
        
    else:
        print("Falha ao obter respostas da planilha.")
        
    return render_template('Chamados_ti_pina.html')

# Rota para abrir Autenticação centralizada
@app.route('/Autenticacao_Centralizada_Pina')
def Autenticacao_Centralizada_Pina():
    return render_template('Autenticacao_Centralizada_Pina.html')


@app.route('/Controle_Patrimonial_Pina')
def Controle_Patrimonial_Pina():
    sheet_url = "https://docs.google.com/spreadsheets/d/1GChEXYjREHpozDMpH1jivxrSXgRRTyhbPf7LTzy3n8Y/edit?usp=sharing"

    # Extrair o ID da planilha do URL
    sheet_id = sheet_url.split('/')[-2]

    # URL da API do Google Sheets
    api_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

    # Faça uma solicitação GET para a API do Google Sheets
    response = requests.get(api_url)

    # Verifique se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Obtenha as respostas da planilha em formato CSV
        responses = response.text.splitlines()

        # Inicializar a conexão com o banco de dados
        connection = mysql.connector.connect(
           host='localhost',
           user='dba',
           password='Sad#Suporte',
           database='expresso_conectado'
        )
        
        # Criar o cursor
        cursor = connection.cursor()

        print("Respostas obtidas com sucesso:")
        for index, response in enumerate(responses[1:], start=2):
            print(f"Resposta {index}: {response}")

            # Usar csv.reader para dividir os campos
            response_data = next(csv.reader([response], delimiter=',', quotechar='"'))

            # Se o comprimento for menor que 4, ignore esta resposta
            if len(response_data) < 6:
                print(f"Resposta {index} não contém dados relevantes. Ignorando...")
                continue

            # Obter os campos relevantes
            
            orgao = response_data[1]
            requerente = response_data[2]
            Tombamento = response_data[3]
            serie1_mon = response_data[4]
            tomb2_mon = response_data[5]
            serie2_mon = response_data[6]
            tomb_gab = response_data[7]
            Serie = response_data[8]
            print(f"Dados relevantes: orgao={orgao}, requerente={requerente},Tombamento={Tombamento},Serie={Serie}")

            # Verificar se a resposta já existe no banco de dados
            sql_check = "SELECT COUNT(*) FROM controle_Patrimonial_Pina WHERE orgao = %s AND requerente = %s AND monitor1_tombamento = %s AND gabiente_serie=%s AND monitor2_tombamento=%s AND monitor2_serie=%s "
            values_check = (orgao, requerente, Tombamento,Serie,tomb2_mon,serie2_mon)
            cursor.execute(sql_check, values_check)
            result = cursor.fetchone()

            # Se não houver registros correspondentes, inserir a resposta
            if result[0] == 0:
                sql_insert = "INSERT INTO controle_Patrimonial_Pina (orgao, requerente, monitor1_tombamento, monitor1_serie, monitor2_tombamento, monitor2_serie, gabiente_tombamento, gabiente_serie, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Não visto')"
                values_insert = (orgao, requerente, Tombamento, serie1_mon, tomb2_mon, serie2_mon, tomb_gab, Serie)
                cursor.execute(sql_insert, values_insert)
                print(f"Resposta {index} inserida no banco de dados com sucesso.")
        
        # Commit das alterações
        connection.commit()

        # Fechar a conexão com o banco de dados
        connection.close()
        
    else:
        print("Falha ao obter respostas da planilha.")
    return render_template('Controle_Patrimonial_Pina.html')

# Rota para abrir Manutenção Predial pina
@app.route('/Manutencao_Predial_Pina')
def Manutencao_Predial_Pina():
    sheet_url = "https://docs.google.com/spreadsheets/d/1nGNg7bm_0Zhn5VQ0QMcGp5t55KZNhZqzQU_q4LPR--s/edit?usp=sharing"

    # Extrair o ID da planilha do URL
    sheet_id = sheet_url.split('/')[-2]

    # URL da API do Google Sheets
    api_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

    # Faça uma solicitação GET para a API do Google Sheets
    response = requests.get(api_url)

    # Verifique se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Obtenha as respostas da planilha em formato CSV
        responses = response.text.splitlines()

        # Inicializar a conexão com o banco de dados
        connection = mysql.connector.connect(
           host='localhost',
           user='dba',
           password='Sad#Suporte',
           database='expresso_conectado'
        )
        
        # Criar o cursor
        cursor = connection.cursor()

        print("Respostas obtidas com sucesso:")
        for index, response in enumerate(responses[1:], start=2):
            print(f"Resposta {index}: {response}")

            # Usar csv.reader para dividir os campos
            response_data = next(csv.reader([response], delimiter=',', quotechar='"'))

            # Se o comprimento for menor que 4, ignore esta resposta
            if len(response_data) < 4:
                print(f"Resposta {index} não contém dados relevantes. Ignorando...")
                continue

            # Obter os campos relevantes
            data_solicitacao = datetime.strptime(response_data[0], '%m/%d/%Y %H:%M:%S')
            orgao = response_data[1]
            requerente = response_data[2]
            Tipo = response_data[3]
            solicitacao = response_data[4]
            print(f"Dados relevantes: orgao={orgao}, requerente={requerente},Tipo{Tipo},solicitacao={solicitacao}")

            # Verificar se a resposta já existe no banco de dados
            sql_check = "SELECT COUNT(*) FROM Chamado_Predial_Pina WHERE orgao = %s AND requerente = %s AND solicitacao = %s AND DATE(Data_Abertura) = DATE(%s)"
            values_check = (orgao, requerente, solicitacao,data_solicitacao)
            cursor.execute(sql_check, values_check)
            result = cursor.fetchone()

            # Se não houver registros correspondentes, inserir a resposta
            if result[0] == 0:
                sql_insert = "INSERT INTO Chamado_Predial_Pina (orgao, requerente, Tipo,solicitacao, status) VALUES (%s, %s, %s,%s, 'Não visto')"
                values_insert = (orgao, requerente,Tipo, solicitacao)
                cursor.execute(sql_insert, values_insert)
                print(f"Resposta {index} inserida no banco de dados com sucesso.")
        
        # Commit das alterações
        connection.commit()

        # Fechar a conexão com o banco de dados
        connection.close()
        
    else:
        print("Falha ao obter respostas da planilha.")

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


#-----------------------------------------------------------------------------------------------------------ROTAS DO CHAMADO DE TI PINA------------------------------------------------------------------------------------------------#
#//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input
@app.route('/api/preencher-formulario', methods=['POST'])
def preencher_formulario():
    # Obter os dados do formulário enviados pela requisição POST
    data = request.json
    orgao = data.get('orgao')
    requerente = data.get('requerente')
    tipo = data.get('tipo')
    solicitacao = data.get('solicitacao')
    driver = webdriver.Chrome()
   
    # Navegar até a URL do formulário
    driver.get('https://docs.google.com/forms/d/e/1FAIpQLScoG84h7UBbDJ4KCY8R7Ygd5iWZWqo6av5_CjTVAvHEbQT_4g/viewform')

   
    time.sleep(5)
    # Esperar até que o campo de input esteja visível
   # Esperar até que o campo de input esteja visível
    orgao_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))
    
    )
    orgao_input.send_keys(orgao)
    
    requerente_input=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'))
     )
    requerente_input.send_keys(requerente)
    
    Tipoch_input=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'))
     )
    Tipoch_input.send_keys(tipo)
    
    
    solicitacao_input=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div[2]/textarea'))
     )
    solicitacao_input.send_keys(solicitacao)

    # Enviar o formulário
    send_button=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div'))
    )
    
    send_button.click()
    

    return jsonify({'message': 'Formulário preenchido com sucesso.'})


#### o de cima foi novidade
@app.route('/api/chamados')
def get_chamados():
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM chamados_ti ORDER BY Data_Abertura DESC')
    chamados = cursor.fetchall()
    cursor.close()
    return jsonify(chamados)

# Rota para adicionar um novo chamado de T.I.
@app.route('/api/chamados', methods=['POST'])
def add_chamado():
    data = request.json
    orgao = data.get('orgao')
    requerente = data.get('requerente')
    tipo = data.get('tipo')
    solicitacao = data.get('solicitacao')
    status = data.get('status')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO chamados_ti (orgao, requerente,tipo, solicitacao, status) VALUES (%s, %s, %s, %s,%s)', (orgao, requerente, tipo,solicitacao, status))
    connection.commit()
    cursor.close()
    return jsonify(message='Chamado de T.I. adicionado com sucesso!', id=cursor.lastrowid)

# Rota para atualizar um chamado de T.I. existente
@app.route('/api/chamados/<int:id>', methods=['PUT'])
def update_chamado(id):
    data = request.json
    
    orgao = data.get('orgao')
    requerente = data.get('requerente')
    tipo = data.get('Tipo')
    solicitacao = data.get('solicitacao')
    status = data.get('status')
    Tipo_ac = data.get('Tipo_ac')
    Andamento = data.get('Andamento')
    Situacao = data.get('Situacao')
    OBS =  data.get('OBS')
    cursor = connection.cursor()
    cursor.execute('UPDATE chamados_ti SET orgao=%s, requerente=%s,tipo=%s, solicitacao=%s, status=%s, Tipo_ac=%s,Andamento=%s,Situacao=%s,OBS=%s WHERE id=%s', (orgao, requerente, tipo,solicitacao, status, Tipo_ac,Andamento,Situacao,OBS,id))
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



@app.route('/api/preencher-formulario-predial', methods=['POST'])
def preencher_formulario_predial():
    # Obter os dados do formulário enviados pela requisição POST
    data = request.json
    orgao = data.get('orgao')
    requerente = data.get('requerente')
    Tipo = data.get('Tipo')
    solicitacao = data.get('solicitacao')
    driver = webdriver.Chrome()

    # Navegar até a URL do formulário
    driver.get('https://docs.google.com/forms/d/e/1FAIpQLSdXsHjKVzzBp7OKs7xo6-NuwHUkUgQLYZ1UZPWYa2rg1Yv2gA/viewform?usp=sf_link')

   
    time.sleep(5)
    # Esperar até que o campo de input esteja visível
   # Esperar até que o campo de input esteja visível
    orgao_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))
    
    )
    orgao_input.send_keys(orgao)
    
    requerente_input=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'))
     )
    requerente_input.send_keys(requerente)
    
    
    Tipo_input=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'))
     )
    Tipo_input.send_keys(Tipo)
    
    solicitacao_input=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div[2]/textarea'))
     )
    solicitacao_input.send_keys(solicitacao)

    # Enviar o formulário
    send_button=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div'))
    )
    
    send_button.click()
    

    return jsonify({'message': 'Formulário preenchido com sucesso.'})



#############################
@app.route('/api/chamadosPrediais')
def get_chamadosPrediaisPina():
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Chamado_Predial_Pina ORDER BY Data_Abertura DESC')
    chamados = cursor.fetchall()
    cursor.close()
    return jsonify(chamados)

# Rota para adicionar um novo chamado de T.I.
@app.route('/api/chamadosPrediais', methods=['POST'])
def add_chamadosPrediaisPina():
    data = request.json
    orgao = data.get('orgao')
    requerente = data.get('requerente')
    Tipo = data.get('Tipo')
    solicitacao = data.get('solicitacao')
    status = data.get('status')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Chamado_Predial_Pina (orgao, requerente,Tipo,solicitacao, status) VALUES (%s, %s, %s, %s, %s)', (orgao, requerente,Tipo, solicitacao, status))
    connection.commit()
    cursor.close()
    return jsonify(message='Chamado predial adicionado com sucesso!', id=cursor.lastrowid)

# Rota para atualizar um chamado de T.I. existente
@app.route('/api/chamadosPrediais/<int:id>', methods=['PUT'])
def update_chamadosPrediaisPina(id):
    data = request.json
    #print (data)
    orgao = data.get('orgao')
    requerente = data.get('requerente')
    Tipo = data.get('Tipo')
    solicitacao = data.get('solicitacao')
    status = data.get('status')
    Tipo_ac = data.get('Tipo_ac')
    Andamento = data.get('Andamento')
    Situacao = data.get('Situacao')
    OBS =  data.get('OBS')
    cursor = connection.cursor()
    #print(orgao,requerente,Tipo,solicitacao,status,Tipo_ac,Andamento,Situacao,OBS)
    cursor.execute('UPDATE Chamado_Predial_Pina SET orgao=%s, requerente=%s,Tipo=%s, solicitacao=%s, status=%s,Tipo_ac=%s,Andamento=%s,Situacao=%s,OBS=%s WHERE id=%s', (orgao, requerente,Tipo, solicitacao, status,Tipo_ac,Andamento,Situacao,OBS,id))
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



#--------------------------------------------------------------------------------------------------------------controle patrimonial---------------------------------------------------------------
  
@app.route('/api/preencher-formulario-controle-patrimonial', methods=['POST'])
def preencher_formulario_controle_patrimonial():
    # Obter os dados do formulário enviados pela requisição POST
    data = request.json
    orgao = data.get('orgao')
    requerente = data.get('requerente')
    monitor1_tomb = data.get('monitor1_tomb')
    monitor1_serie = data.get('monitor1_serie')
    monitor2_tomb = data.get('monitor2_tomb')
    monitor2_serie = data.get('monitor2_serie')
    gabiente_Tom = data.get('gabiente_Tom')
    gabiente_serie = data.get('gabiente_serie')
    driver = webdriver.Chrome()

    # Navegar até a URL do formulário
    driver.get('https://docs.google.com/forms/d/e/1FAIpQLSdqTH_L-1izXy1pn0lNtSiWkvEOw3lI5iSERfAWqNBDaEBI2w/viewform?usp=sf_link')

   
    time.sleep(5)
    # Esperar até que o campo de input esteja visível
   # Esperar até que o campo de input esteja visível
    orgao_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))
    
    )
    orgao_input.send_keys(orgao)
    
    requerente_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'))
    
    )
    requerente_input.send_keys(requerente)
    
    Mon1_Tomb_input=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'))
     )
    Mon1_Tomb_input.send_keys(monitor1_tomb)
    
    
    Mon1_serie_input=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input'))
     )
    Mon1_serie_input.send_keys(monitor1_serie)
    
    Mon2_Tomb_input=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input'))
     )
    Mon2_Tomb_input.send_keys(monitor2_serie)
    
    
    Mon2_serie_input=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input'))
     )
    Mon2_serie_input.send_keys(monitor2_tomb)
    
    gab_tomb_input=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input'))
     )
    gab_tomb_input.send_keys(gabiente_Tom)
    
    gab_serie_input=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input'))
     )
    gab_serie_input.send_keys(gabiente_serie)
    
    

    # Enviar o formulário
    send_button=WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div'))
    )
    
    send_button.click()
    

    return jsonify({'message': 'Formulário preenchido com sucesso.'})



#############################
@app.route('/api/controlepatrimonialpina')
def get_controle_patrimonial_Pina():
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM controle_Patrimonial_Pina ORDER BY Data_Abertura DESC')
    chamados = cursor.fetchall()
    cursor.close()
    return jsonify(chamados)

# Rota para adicionar um novo equipamento patrimonial.
@app.route('/api/controlepatrimonialpina', methods=['POST'])
def add_controlepatrimonialPina():
    data = request.json
    #print(data)
    orgao = data.get('orgao')
    requerente = data.get('requerente')
    monitor1_tomb = data.get('monitor1_tomb')
    monitor1_serie = data.get('monitor1_serie')
    monitor2_tomb = data.get('monitor2_tomb')
    monitor2_serie = data.get('monitor2_serie')
    gabiente_Tom = data.get('gabiente_Tom')
    gabiente_serie = data.get('gabiente_serie')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO controle_Patrimonial_Pina (orgao, requerente,monitor1_tombamento,monitor1_serie, monitor2_tombamento,monitor2_serie,gabiente_tombamento,gabiente_serie,status) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,"Não visto")', (orgao, requerente,monitor1_tomb, monitor1_serie, monitor2_tomb,monitor2_serie,gabiente_Tom,gabiente_serie))
    connection.commit()
    cursor.close()
    return jsonify(message='Chamado predial adicionado com sucesso!', id=cursor.lastrowid)

# Rota para atualizar um equipamento patrimonial existente
@app.route('/api/controlepatrimonialpina/<int:id>', methods=['PUT'])
def update_controle_patrimonial_Pina(id):
    data = request.json
    #print (data)
    orgao = data.get('orgao')
    requerente = data.get('requerente')
    monitor1_tomb = data.get('monitor1_tomb')
    monitor1_serie = data.get('monitor1_serie')
    monitor2_tomb = data.get('monitor2_tomb')
    monitor2_serie = data.get('monitor2_serie')
    gabiente_Tom = data.get('gabiente_Tom')
    gabiente_serie = data.get('gabiente_serie')
    status = data.get('status')
    cursor = connection.cursor()
    #print(orgao,requerente,Tipo,solicitacao,status,Tipo_ac,Andamento,Situacao,OBS)
    cursor.execute('UPDATE controle_Patrimonial_Pina SET orgao=%s, requerente=%s,monitor1_tombamento=%s,monitor1_serie=%s, monitor2_tombamento=%s,monitor2_serie=%s,gabiente_tombamento=%s,gabiente_serie=%s,status=%s WHERE id=%s', (orgao, requerente,monitor1_tomb, monitor1_serie, monitor2_tomb,monitor2_serie,gabiente_Tom,gabiente_serie,status,id))
    connection.commit()
    cursor.close()
    return jsonify(message='Equipamento predial atualizado com sucesso!', id=id)


# Rota para excluir um equipamento patrimonial.
@app.route('/api/controlepatrimonialpina/<int:id>', methods=['DELETE'])
def update_controlepatrimonialPina(id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM controle_Patrimonial_Pina WHERE id=%s', (id,))
    connection.commit()
    cursor.close()
    return jsonify(message='Equipamento predial excluído com sucesso!', id=id)


#--------------------------------------------------------------------------------------------------------------Situação geral do Pina----------------------------------------------------------------------------------------
# Rota para Conseguir a quantidade de atendimentos totais feitos.
# Inicializar a conexão com o banco de dados
conexao = mysql.connector.connect(
    host='localhost',
    user='dba',
    password='Sad#Suporte',
    database='ec_pina'
)
        
# Criar o cursor
exe = conexao.cursor()
@app.route('/api/sitgeralpina')
def get_contagem():
    exe = conexao.cursor(dictionary=True)
    exe.execute('SELECT count(id) FROM recepcao where sit_atendimento="Atendido"')
    chamados = exe.fetchall()
    exe.close()
    return jsonify(chamados)


exe = conexao.cursor()
@app.route('/api/sitprioritarios')
def get_contagem_pri():
    exe = conexao.cursor(dictionary=True)
    exe.execute('SELECT count(id) FROM recepcao where sit_atendimento="Atendido" and tipo="Prioritario"')
    chamados = exe.fetchall()
    exe.close()
    return jsonify(chamados)


@app.route('/api/tma')
def get_contagem_tma():
    exe = conexao.cursor(dictionary=True)
    exe.execute('SELECT AVG(TIMESTAMPDIFF(MINUTE, hora_inicio_atendimento, hora_fim_atedimento)) AS media_atendimento FROM atendente; ')
    result = exe.fetchone()  # Fetchone para obter apenas uma linha
    media_atendimento = result['media_atendimento']  # Acessa a coluna corretamente
    formatted_media_atendimento = str(media_atendimento)  # Converta para uma string
    exe.close()
    
    # Adicionando logs de depuração
    print("Resultado da consulta:", result)
    print("Tempo médio formatado:", formatted_media_atendimento)
    
    return jsonify({'media_atendimento': formatted_media_atendimento})

@app.route('/api/grafico_atendimento')
def get_contagem_atendimentos():
    exe = conexao.cursor(dictionary=True)
    exe.execute('''
        SELECT
            SUM(CASE WHEN MONTH(hora_fim_atedimento) = 1 THEN 1 ELSE 0 END) AS total_atendidas_janeiro,
            SUM(CASE WHEN MONTH(hora_fim_atedimento) = 2 THEN 1 ELSE 0 END) AS total_atendidas_fevereiro,
            SUM(CASE WHEN MONTH(hora_fim_atedimento) = 3 THEN 1 ELSE 0 END) AS total_atendidas_marco
        FROM
            atendente
        WHERE
            sit_atendimento = "Atendido";
    ''')
    result = exe.fetchall()  # Fetchall para obter todos os resultados
    
    exe.close()
    
    return jsonify(result)


@app.route('/api/graf_pizza')
def get_contagem_atendimentos_pizza():
    exe = conexao.cursor(dictionary=True)
    exe.execute('''
        SELECT
        SUM(CASE WHEN cod LIKE 'rg%' THEN 1 ELSE 0 END) AS primeiravia,
        SUM(CASE WHEN cod LIKE '2rg%' THEN 1 ELSE 0 END) AS segundavia,
        SUM(CASE WHEN cod NOT LIKE 'rg%' AND cod NOT LIKE '2rg%' THEN 1 ELSE 0 END) AS outros
        FROM
       recepcao
       WHERE
       sit_atendimento = 'Atendido';
    ''')
    result = exe.fetchall()  # Fetchall para obter todos os resultados
    
    exe.close()
    
    return jsonify(result)




if __name__ == '__main__':
   app.run(debug=False, host='10.1.106.8', port=3001)

