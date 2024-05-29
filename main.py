import mysql.connector as db
from constantes import DB_HOSTNAME,DB_DATABASE,DB_PASSWORD,DB_USERNAME
import random
from typing import List, Dict, Tuple, Any
RowType = Tuple, list, dict

# Conexión a la base de datos
conn = db.connect(
        host=DB_HOSTNAME,
        database=DB_DATABASE,
        user=DB_USERNAME,
        password=DB_PASSWORD
)
cursor = conn.cursor()

# Función para verificar si una letra está dentro de una palabra
def verificar_letra(palabra, letra):
    posiciones = []
    for i, char in enumerate(palabra):
        if char == letra:
            posiciones.append(i)
    return posiciones

# Función para comparar dos palabras
def comparar_palabras(palabra1, palabra2):
    result = []
    for i, (char1, char2) in enumerate(zip(palabra1, palabra2)):
        if char1 == char2:
            result.append('O')
        elif char2 in palabra1:
            result.append('-')
        else:
            result.append('X')
    return result

# Función para obtener una palabra y su ID que no haya jugado un jugador
def obtener_nueva_palabra(jugador_name):
    # Obtener la lista de palabras que el jugador no ha jugado
    cursor.execute("SELECT p.id, p.palabra FROM palabras p LEFT JOIN jugadas j ON p.id = j.palabra_id AND j.jugador = %s WHERE j.jugador IS NULL", (jugador_name,))
    palabras = cursor.fetchone()
    return palabras

# Función para guardar la jugada de un jugador
def guardar_juego(jugador_name, palabra_id, intentos):
    cursor.execute("INSERT INTO jugadas (palabras, jugador, intentos) VALUES (%s, %s, %s)", (palabra_id, jugador_name, intentos))
    conn.commit()

# Función para obtener el top 10 de jugadores por promedio de intentos
def obtener_top10():
    cursor.execute("""
        SELECT 
            j.nombre,
            COUNT(DISTINCT g.palabras) AS palabras_adivinadas,
            COUNT(g.palabras) AS total_jugadas,
            AVG(g.intentos) AS promedio_intentos
        FROM jugadores j
        LEFT JOIN jugadas g ON j.id = g.jugador
        GROUP BY j.id
        ORDER BY promedio_intentos ASC
        LIMIT 10
    """)
    return cursor.fetchall()

# Pruebas
letras_encontradas = verificar_letra("hola", "o")
comparacion = comparar_palabras("hola", "casa")
nueva_palabra = obtener_nueva_palabra("jugador1")
guardar_juego("jugador1", 1, 5)
top10_jugadores = obtener_top10()

# Cierre de la conexión
conn.close()