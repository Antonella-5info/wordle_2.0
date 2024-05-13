from typing import List
import mysql.connector as db
from constantes import DB_HOSTNAME,DB_DATABASE,DB_PASSWORD,DB_USERNAME
import random
import mysql.connector as db

def abrir_conexion() -> db.pooling.PooledMySQLConnection | db.MySQLConnection:

    return db.connect(host=DB_HOSTNAME,
                      user=DB_USERNAME,
                      password=DB_PASSWORD,
                      database=DB_DATABASE)
def consulta_generica(conn : db.MySQLConnection, consulta : str) -> List[db.connection.RowType]:
    cursor = conn.cursor(buffered=True)
    cursor.execute(consulta)
    return cursor.fetchall()

