import mysql.connector as mysql
from dotenv import load_dotenv
from os import getenv
from passlib.hash import pbkdf2_sha256 as sha256

#carrega as var de abiente no arquivo ".env"
load_dotenv()

def cria_user(nome,email,senha):
    try:
        #conexção com a db
        conn = mysql.connect(
            host=getenv("host"),
            port=getenv("port"),
            user=getenv("user"),
            password=getenv("password"),
            database=getenv("database")
           )
        
        #hash basico
        senha = sha256.hash(senha)

        #cria um objeto para poder executa comando 
        cursor = conn.cursor()
        #executa o coamndo em sql
        cursor.execute("INSERT INTO USERS (NOME, EMAIL, SENHA) VALUES (%s,%s,%s)", (nome,email, senha,))
        #evitiv o comando no servidor
        conn.commit()
    except Exception as e:
        print(f"Erro cria_user : {e}")
    finally:
        #apos a conexção ele mata o cursor e a conexção
        if conn.is_connected():
            cursor.close()
            conn.close()

def listar_usaurio():
    try:
        conn = mysql.connect(
            host=getenv("host"),
            port=getenv("port"),
            user=getenv("user"),
            password=getenv("password"),
            database=getenv("database")
        )

        cursor = conn.cursor()
        cursor.execute("SELECT NOME, EMAIL, SENHA FROM USERS")
        usuario = cursor.fetchall()

        #ver se retornou algo
        if usuario:
            #print as infos 
            print("Lista de user")
            for u in usuario:
                print(f"| {u}")
        else:
            print("user não existe")
    except Exception as e:
        print(f"erro listar_usaurio() : {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def excluir_user(id):
    try:
        conn = mysql.connect(
            host=getenv("host"),
            port=getenv("port"),
            user=getenv("user"),
            password=getenv("password"),
            database=getenv("database")
        )

        cursor = conn.cursor()
        cursor.execute("DELETE FROM USERS WHERE ID=%s", (id,))

        conn.commit()
        print("o user deletado com sucesso")
    except Exception as e:
        print(f"erro excluir_user() : {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def logar(email, senha):
    try:
        conn = mysql.connect(
            host=getenv("host"),
            port=getenv("port"),
            user=getenv("user"),
            password=getenv("password"),
            database=getenv("database")
        )

        cursor = conn.cursor()
        cursor.execute("SELECT SENHA FROM USERS WHERE EMAIL=%s", (email,))
        result = cursor.fetchall()

        #ver se o user existe
        if result:
            #pega só a string do resuldado
            result = tuple(result[0])
            result = str(result[0])
            #ver se o has da senha inserida é a mesma do has do banco
            if sha256.verify(senha,result):
                print("login liberado")
            else:
                print("senha invalida")
        else:
            print("user não encontrado")
    except Exception as e:
        print(f"erro logar() : {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

