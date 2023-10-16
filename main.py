from fastapi import FastAPI, Request
import hefesto
import mysql.connector
from mysql.connector import Error
#imports para gerar um ID randomico
import random
import string
from typing import Optional
from pydantic import BaseModel
import requests

"""data = {
    "latitude": 'Test',
    "longitude": 'Test',
    "nav_user": 'Test',
    "hour_login": 'Test',
    "sys_user": 'Test',
    "IP_user": 'Test',
    "seguro": 'Test'
}

def env_solit():
    response = requests.post("http://127.0.0.1:8000/solicitacao/", data=data)
    print(response.content)"""


class dataAnltc(BaseModel):
    #modelo/SCHEMA do Json para o DADOS
    latitude: str
    longitude: str
    nav_user: int
    hour_login: str
    sys_user: int
    IP_user: str
    seguro: Optional[int] = None


def insert_database(latitude,longitude,nav_user,hour_login,sys_user,user_ip,seguro):
    #essa função insere no DB a linha de dados
    connection = create_server_connection( )

    cursor = connection.cursor()
    #random_id = generate_random_id(10)
    try:
        comando_createtable = f"INSERT INTO data_hefestos (latitude, longitude, nav_user, hour_login, sys_user, user_ip, seguro) VALUES ('"+latitude+"','"+longitude+"','"+str(nav_user)+"','"+hour_login+"','"+str(sys_user)+"','"+user_ip+"','"+str(seguro)+"');"
        print(comando_createtable)
        cursor.execute(comando_createtable)
        connection.commit()
        resp = "Inserido no BD"
    except Error as err:
        print(f"Error: '{err}'")
        resp = "Deu Bosta!"
    return  resp



def create_server_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
           host='localhost',
    user='root',
    passwd='',
    database='hefestapibd'
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection



app = FastAPI()#Cria a API

#Função para gerar um ID randomico 
def generate_random_id(length):
  """Gera um ID aleatório de um determinado comprimento."""
  # Gera uma lista de caracteres aleatórios.
  characters = list(string.ascii_letters + string.digits)
  random.shuffle(characters)
  # Seleciona os primeiros `length` caracteres da lista.
  random_id = ''.join(characters[:length])
  # Retorna o ID aleatório.
  return random_id

@app.get("/")
def home():
    return{'message': 'Olá, essa é a URL principal'}

@app.post("/insert/")
#nessa solicitação eu passo os parametros que serão analisados
async def criar_solicitacao(request: dataAnltc):
    insert = insert_database(request.latitude, request.longitude, request.nav_user, request.hour_login, request.sys_user, request.IP_user, request.seguro)
    if(insert == 'Inserido no BD'):
        http = True
    if(insert == 'Deu Bosta!'):
        http = False
    return{'message': http}    

@app.post("/push")
async def root(request: dataAnltc):
    test = hefesto.rest_trainTest(request.latitude, request.longitude, request.nav_user, request.hour_login, request.sys_user, request.IP_user)
    if(test == 'Não é seguro'):
        esc = 'not'
        seg = 1
        print(esc)
    if(test == 'Seguro'):
        esc = 'yes'
        seg = 0
        print(esc)
    insert = insert_database(request.latitude, request.longitude, request.nav_user, request.hour_login, request.sys_user, request.IP_user,seg)
    print(insert)
    return{"resposta": esc}


@app.get("/mysql")
#nessa função eu recebo o id da applicação que é o nome que darei na tabela   
def cadastra_db():
    connection = create_server_connection( )

    cursor = connection.cursor()
    random_id = generate_random_id(10)
    try:
        comando_createtable = f"CREATE TABLE `data_hefestos`(\nlatitude VARCHAR(100),\nlongitude VARCHAR(100),\nnav_user INT(6),\nhour_login VARCHAR(50),\nsys_user INT(6),\nuser_ip VARCHAR(100));"
        print(comando_createtable)
        cursor.execute(comando_createtable)
        connection.commit()
        resp = "Banco de dados criado!"
    except Error as err:
        print(f"Error: '{err}'")
        resp = "Deu Bosta!"
    return {'message': resp}
