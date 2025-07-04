# diario_twin_db.py
import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def conectar():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def obter_ou_criar_usuario(nome, chave_api, provedor):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id FROM usuarios WHERE nome = %s", (nome,))
    resultado = cur.fetchone()

    if resultado:
        usuario_id = resultado[0]
    else:
        cur.execute(
            "INSERT INTO usuarios (nome, chave_api, provedor) VALUES (%s, %s, %s) RETURNING id",
            (nome, chave_api, provedor)
        )
        usuario_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return usuario_id

def salvar_interacao(usuario_id, entrada, resposta):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO interacoes (usuario_id, entrada, resposta) VALUES (%s, %s, %s)",
        (usuario_id, entrada, resposta)
    )
    conn.commit()
    cur.close()
    conn.close()

def buscar_historico(usuario_id, limite=10):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "SELECT entrada, resposta FROM interacoes WHERE usuario_id = %s ORDER BY id DESC LIMIT %s",
        (usuario_id, limite)
    )
    historico = cur.fetchall()
    cur.close()
    conn.close()
    return historico
