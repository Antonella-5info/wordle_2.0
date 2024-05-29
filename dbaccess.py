import mysql.connector as db
from constantes import DB_HOSTNAME,DB_DATABASE,DB_PASSWORD,DB_USERNAME
import random
from typing import List, Dict, Tuple, Any
RowType = Tuple, list, dict

def abrir_conexion() -> db.pooling.PooledMySQLConnection | db.MySQLConnection:
    return db.connect(host=DB_HOSTNAME,
                      user=DB_USERNAME,
                      password=DB_PASSWORD,
                      database=DB_DATABASE)

def consulta_generica(conn: db.MySQLConnection, consulta: str, parametros: tuple = ()) -> list[db.connection.RowType]:
    cursor = conn.cursor(buffered=True)
    cursor.execute(consulta, parametros)
    return cursor.fetchall()

def modificacion_generica(conn: db.MySQLConnection, consulta: str, parametros: tuple = ()) -> int:
    cursor = conn.cursor(buffered=True)
    cursor.execute(consulta, parametros)
    conn.commit()
    return cursor.rowcount

def jugador(conn: db.MySQLConnection, nombre_del_jugador: str) -> dict:
    nv = consulta_generica(conn, f'select * from jugadores where nombre = "{nombre_del_jugador}"')
    if len(nv) == 0:
        modificacion_generica(conn, f'insert into jugadores (nombre) value ("{nombre_del_jugador}")')
        resultado = consulta_generica(conn, 'select * from jugadores order by id desc limit 1')
        return {
            "id": resultado[0][0],
            "nombre": resultado[0][1]
        }
    else:
        return {
            "id": nv[0][0],
            "nombre": nv[0][1]
        }

def existe_jugador(conn: db.MySQLConnection, nombre_del_jugador: str) -> bool:
    resultado = consulta_generica(conn, f'select nombre from jugadores where nombre = "{nombre_del_jugador}"')
    return len(resultado) > 0


def palabras_jugadas(conn: db.MySQLConnection, nombre_del_jugador: str) -> list[dict]:
    jugador_id = jugador(conn, nombre_del_jugador)["id"]
    resultado = consulta_generica(conn, f'select palabra, intentos from jugadas where jugador = {jugador_id}')
    palabras = []
    for row in resultado:
        palabras.append({
            "palabra": row[0],
            "intentos": row[1]
        })
    return palabras

def palabra_rand(conn: db.MySQLConnection, jugador_id: int) -> str:
    ultimo_id = consulta_generica(conn, f'select id from palabras order by id desc limit 1')
    ultimo_id = ultimo_id[0][0] 
    id_palabra = random.randint(1, ultimo_id)
    palabras_jugadas = consulta_generica(conn, f'select id from jugadores where id = {jugador_id}')
    palabras_jugadas_ids = [row[0] for row in palabras_jugadas]
    while id_palabra in palabras_jugadas_ids:
        id_palabra = random.randint(1, ultimo_id)

    # Obtener la palabra a partir del id
    palabra = consulta_generica(conn, f'select palabra from palabras where id ={id_palabra}')
    return palabra[0][0]

def cargar_partida(conn: db.MySQLConnection, id_palabra_jugada: int, id_jugador: int, cant_intentos: int):
    # Verificar si la combinación de palabra, jugador e intentos ya existe
    existe_jugada = consulta_generica(conn, "select count(*) from jugadas where palabra = %s and jugador = %s and intentos = %s", (id_palabra_jugada, id_jugador, cant_intentos))
    if existe_jugada[0][0] > 0:
        return  # La jugada ya existe, no es necesario insertarla de nuevo

    cargar = modificacion_generica(conn, "insert into jugadas (palabra, jugador, intentos) values (%s, %s, %s)", (id_palabra_jugada, id_jugador, cant_intentos))