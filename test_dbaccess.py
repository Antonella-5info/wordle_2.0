import mysql.connector as db
from constantes import DB_HOSTNAME,DB_DATABASE,DB_PASSWORD,DB_USERNAME
import random
from typing import List, Dict, Tuple, Any
RowType = Tuple, list, dict
import dbaccess
import pytest

@pytest.fixture
def conn_fixture():
    conn = db.connect(host=DB_HOSTNAME, 
                      user=DB_USERNAME,
                      password=DB_PASSWORD, 
                      database=DB_DATABASE)
    yield conn
    conn.close()

def consulta_generica(conn: db.MySQLConnection, consulta: str) -> list[db.connection.RowType]:
    cursor = conn.cursor(buffered=True)
    cursor.execute(consulta)
    return cursor.fetchall()

def modificacion_generica(conn: db.MySQLConnection, consulta: str) -> int:
    cursor = conn.cursor(buffered=True)
    cursor.execute(consulta)
    conn.commit()
    return cursor.rowcount

def test_jugador(conn_fixture):
    nombre_del_jugador = "Jugador de prueba"
    resultado = dbaccess.jugador(conn_fixture, nombre_del_jugador)
    assert resultado["nombre"] == nombre_del_jugador
    assert resultado["id"] > 0

def test_existe_jugador(conn_fixture):
    nombre_del_jugador = "Jugador Existente"
    dbaccess.jugador(conn_fixture, nombre_del_jugador)
    resultado = dbaccess.jugador(conn_fixture, nombre_del_jugador)
    assert resultado["nombre"] == nombre_del_jugador
    assert resultado["id"] > 0
'''
def test_jugador(conn_fixture):
    nombre_del_jugador = "Jugador de Prueba"
    resultado = dbaccess.jugador(conn_fixture, nombre_del_jugador)
    assert resultado["nombre"] == nombre_del_jugador
    assert resultado["id"] > 0

    with pytest.raises(ValueError):
        dbaccess.jugador(conn_fixture, nombre_del_jugador)

def test_existe_jugador(conn_fixture):
    nombre_del_jugador = "Jugador Existente"
    dbaccess.jugador(conn_fixture, nombre_del_jugador)
    assert dbaccess.existe_jugador(conn_fixture, nombre_del_jugador)
    assert not dbaccess.existe_jugador(conn_fixture, "Jugador No Existente")
'''
def test_palabras_jugadas(conn_fixture):
    nombre_del_jugador = "Jugador de Prueba"
    jugador_id = dbaccess.jugador(conn_fixture, nombre_del_jugador)["id"]
    dbaccess.cargar_partida(conn_fixture, 1, jugador_id, 3)
    dbaccess.cargar_partida(conn_fixture, 2, jugador_id, 5)
    dbaccess.cargar_partida(conn_fixture, 3, jugador_id, 2)
    palabras = dbaccess.palabras_jugadas(conn_fixture, nombre_del_jugador)
    assert len(palabras) == 3
    assert palabras[0]["palabra"] == 1
    assert palabras[0]["intentos"] == 3
    assert palabras[1]["palabra"] == 2
    assert palabras[1]["intentos"] == 5
    assert palabras[2]["palabra"] == 3
    assert palabras[2]["intentos"] == 2
    
def test_palabra_rand(conn_fixture):
    jugador_nombre = "Jugador de Prueba"
    jugador_id = dbaccess.jugador(conn_fixture, jugador_nombre)["id"]
    palabra = dbaccess.palabra_rand(conn_fixture, jugador_id)

    # Verificar que la palabra obtenida existe en la base de datos
    existe_palabra = dbaccess.consulta_generica(conn_fixture, f"select count(*) from palabras where palabra = '{palabra}'")
    assert existe_palabra[0][0] > 0

    # Verificar que la palabra no ha sido jugada anteriormente por este jugador
    palabras_jugadas = dbaccess.consulta_generica(conn_fixture, f"select palabra from jugadas where jugador = {jugador_id}")
    palabras_jugadas_set = set(row[0] for row in palabras_jugadas)
    assert palabra not in palabras_jugadas_set