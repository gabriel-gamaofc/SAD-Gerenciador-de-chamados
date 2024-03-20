import csv
import requests
import mysql.connector

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
            orgao = response_data[1]
            requerente = response_data[2]
            Tipo = response_data[3]
            solicitacao = response_data[4]
            print(f"Dados relevantes: orgao={orgao}, requerente={requerente},Tipo{Tipo},solicitacao={solicitacao}")

            # Verificar se a resposta já existe no banco de dados
            sql_check = "SELECT COUNT(*) FROM Chamado_Predial_Pina WHERE orgao = %s AND requerente = %s AND solicitacao = %s  AND  DATE(Data_Abertura) = CURDATE() "
            values_check = (orgao, requerente, solicitacao)
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

# Exemplo de uso
sheet_url = "https://docs.google.com/spreadsheets/d/1nGNg7bm_0Zhn5VQ0QMcGp5t55KZNhZqzQU_q4LPR--s/edit?usp=sharing"
get_responses_from_sheet(sheet_url)
