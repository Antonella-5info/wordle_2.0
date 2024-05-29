import mysql.connector as db
from constantes import DB_HOSTNAME,DB_DATABASE,DB_PASSWORD,DB_USERNAME
import random
from typing import List, Dict, Tuple, Any
RowType = Tuple, list, dict
import main
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


def test_verificar_letra(conn_fixture):
    assert main.verificar_letra("hola", "o") == [1]
    assert main.verificar_letra("casa", "a") == [1, 3]
    assert main.verificar_letra("python", "x") == []

def test_comparar_palabras(conn_fixture):
    assert main.comparar_palabras("hola", "casa") == ['X', 'X', 'X', 'O']
    assert main.comparar_palabras("python", "python") == ['O', 'O', 'O', 'O', 'O', 'O']
    assert main.comparar_palabras("abcd", "efgh") == ['X', 'X', 'X', 'X']

def test_obtener_nueva_palabra(conn_fixture):
    nueva_palabra = main.obtener_nueva_palabra(conn_fixture, "jugador1")
    assert nueva_palabra is not None
    assert len(nueva_palabra) == 2

def test_guardar_juego(conn_fixture):
    main.guardar_juego(conn_fixture, "jugador1", 1, 5)
    # Aquí podrías verificar que la jugada se guardó correctamente en la base de datos

def test_obtener_top10(conn_fixture):
    top10_jugadores = main.obtener_top10(conn_fixture)
    assert len(top10_jugadores) == 10
    for player in top10_jugadores:
        assert isinstance(player[0], str)
        assert isinstance(player[1], int)
        assert isinstance(player[2], int)
        assert isinstance(player[3], float)