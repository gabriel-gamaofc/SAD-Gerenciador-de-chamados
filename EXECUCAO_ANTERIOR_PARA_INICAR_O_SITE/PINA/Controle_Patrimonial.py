import csv
import requests
import mysql.connector
from datetime import datetime

def get_responses_from_sheet(sheet_url):
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
           host='',#ip da maquina de conexão com o banco 
           user='',#usuario do banco de dados
           password='',#Senha do usuario
           database=''#Qual database
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
            data_solicitacao = datetime.strptime(response_data[0], '%m/%d/%Y %H:%M:%S')
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
            sql_check = "SELECT COUNT(*) FROM controle_Patrimonial_Pina WHERE orgao = %s AND requerente = %s AND monitor1_tombamento = %s AND gabiente_serie=%s  AND DATE(Data_Abertura) = DATE(%s)"
            values_check = (orgao, requerente, Tombamento,Serie,data_solicitacao)
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

# Exemplo de uso
sheet_url = "#Link da planilha"
get_responses_from_sheet(sheet_url)
