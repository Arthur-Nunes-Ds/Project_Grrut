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
        cursor.execute("INSERT INTO user (NOME, EMAIL, SENHA) VALUES (%s,%s,%s)", (nome,email, senha,))
        #evitiv o comando no servidor
        conn.commit()
    except Exception as e:
        print(f"Erro cria_user : {e}")
        return
    finally:
        #apos a conexção ele mata o cursor e a conexção
        if conn.is_connected():
            cursor.close()
            conn.close()
            return

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
        cursor.execute("SELECT NOME, EMAIL, SENHA FROM user")
        usuario = cursor.fetchall()

        #ver se retornou algo
        if usuario:
            #print as infos 
            print("Lista de user: ")
            print("user | email | senha |")
            for u in usuario:
                for d in u:
                    print(d, end=" | ")
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
        cursor.execute("DELETE FROM user WHERE ID=%s", (id,))

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
        cursor.execute("SELECT ID,SENHA FROM user WHERE EMAIL=%s", (email,))
        result = cursor.fetchall()

        #ver se o user existe
        if result:
            #pega só a string do resuldado
            _senha = tuple(result[1])
            _senha = str(_senha[1])
            id = tuple(result[0])
            id = int(id[0])  # pyright: ignore[reportArgumentType]
            #ver se o has da senha inserida é a mesma do has do banco
            if sha256.verify(senha,_senha):
                print("login liberado")
                return [True, id]
            else:
                print("senha invalida")
        else:
            print("user não encontrado")
    except Exception as e:
        print(f"erro logar() : {e}")
        return
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

#produtos:
def cadastrar_produtos(Nome, Desc, Pr, Qn):
    try:
        Pr = str(Pr)
        if Pr.isdigit:
            Pr = float(Pr.replace(",","."))
            if Pr >= 0.00:
                print("preço abaixo do zero")
        else:
            print("insira um numero valido")

        #conexção com a db
        conn = mysql.connect(
            host=getenv("host"),
            port=getenv("port"),
            user=getenv("user"),
            password=getenv("password"),
            database=getenv("database")
           )

        #cria um objeto para poder executa comando 
        cursor = conn.cursor()

        #executa o coamndo em sql
        cursor.execute("INSERT INTO produtos (DESCRECAO,PR,QNT,NOME) VALUES (%s,%s,%s,%s)", (Desc, Pr, Qn, Nome))
        #evitiv o comando no servidor
        conn.commit()

        print("produto cadastrado com suceso")
    except Exception as e:
        print(f"Erro cadastarar_produtos : {e}")
        return
    finally:
        #apos a conexção ele mata o cursor e a conexção
        if conn.is_connected():
            cursor.close()
            conn.close()
            return

def listar_produtos():
    try:
        #conexção com a db
        conn = mysql.connect(
            host=getenv("host"),
            port=getenv("port"),
            user=getenv("user"),
            password=getenv("password"),
            database=getenv("database")
           )

        #cria um objeto para poder executa comando 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        usuario = cursor.fetchall()

        #ver se retornou algo
        if usuario:
            #print as infos 
            print("Lista de produtos: ")
            print("id | descreção | R$ | QNT | NOME")
            for u in usuario:
                print()
                for d in u:
                    print(d, end=" | ")
        else:
            print("produtos não existe")
    except Exception as e:
        print(f"Erro cadastarar_produtos : {e}")
        return
    finally:
        #apos a conexção ele mata o cursor e a conexção
        if conn.is_connected():
            cursor.close()
            conn.close()
            return
        
def vender(id, qauntidade=1):
    try:
        #conexção com a db
        conn = mysql.connect(
            host=getenv("host"),
            port=getenv("port"),
            user=getenv("user"),
            password=getenv("password"),
            database=getenv("database")
           )

        #cria um objeto para poder executa comando 
        cursor = conn.cursor()
        cursor.execute("SELECT QNT FROM produtos WHERE id=%s",(id,))
        dados = cursor.fetchall()
        dados = tuple(dados[0]); dados = dados[0]

        qnt = dados - qauntidade # pyright: ignore[reportOperatorIssue]

        if qnt > 0:
            cursor.execute("UPDATE produtos SET QNT = %s WHERE id=%s",(int(qnt),int(id)))
        else:
            cursor.execute("DELETE FROM produtos WHERE id=%s ",(int(id),))

        conn.commit()

    except Exception as e:
        print(f"Erro cadastarar_produtos : {e}")
        return
    finally:
        #apos a conexção ele mata o cursor e a conexção
        if conn.is_connected():
            cursor.close()
            conn.close()
            return

def editar_produtos(id, Nome, Desc, Pr, Qn):
    try:
        conn = mysql.connect(
            host=getenv("host"),
            port=getenv("port"),
            user=getenv("user"),
            password=getenv("password"),
            database=getenv("database")
           )
        
        cursor = conn.cursor()

        Pr = str(Pr)
        if Pr.isdigit:
            Pr = float(Pr.replace(",","."))
            if Pr <= 0.00:
                print("preço abaixo do zero")
        else:
            print("insira um numero valido")

        #conexção com a db
        conn = mysql.connect(
            host=getenv("host"),
            port=getenv("port"),
            user=getenv("user"),
            password=getenv("password"),
            database=getenv("database")
           )

        #cria um objeto para poder executa comando 
        cursor = conn.cursor()

        #executa o coamndo em sql
        cursor.execute("UPDATE produtos SET DESCRECAO = %s,PR= %s,QNT= %s ,NOME = %s WHERE id = %s", (Desc, Pr, Qn, Nome, id))
        #evitiv o comando no servidor
        conn.commit()

        print("produto cadastrado com suceso")
    except Exception as e:
        print(f"Erro cadastarar_produtos : {e}")
        return
    finally:
        #apos a conexção ele mata o cursor e a conexção
        if conn.is_connected():
            cursor.close()
            conn.close()
            return

