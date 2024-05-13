import mysql.connector as db
from constantes import DB_HOSTNAME,DB_DATABASE,DB_PASSWORD,DB_USERNAME

def abrir_conexion() -> db.pooling.PooledMySQLConnection | db.MySQLConnection:

    return db.connect(host=DB_HOSTNAME,
                      user=DB_USERNAME,
                      password=DB_PASSWORD,
                      database=DB_DATABASE)
def consulta_generica(conn : db.MySQLConnection, consulta : str) -> List [db.connection.RowType]:
    cursor = conn.cursor(buffered=True)
    cursor.execute(consulta)
    return cursor.fetchall()
def jugador(conn) -> List[db.connection.RowType]:
    nombre = consulta_generica(conn, f'insert into jugadores (nombre) value ("nombre_del_jugador");')
    
def existe_jugador(conn) -> List[db.connection.RowType]:
    existe_nombre = consulta_generica(conn, f'select * from jugadores where nombre = "nombre_del_jugador";')
    
def palabras_jugadas(conn) -> List[db.connection.RowType]:
    existe_nombre = consulta_generica(conn, f'select id from palabras where  palabra =! "palabra_ya_jugada";')
    
def palabra_rand(conn:db.MySQLConnection):
    ultimo_id = consulta_generica(conn, f'select id, palabra from palabras order by id desc limit 1;')
    id_palabra = random.ranint(1, ultimo_id)
    palabras_jugadas = palabras_jugadas(conn, 1)
    for i in palabras_jugadas[0]:
        while id_palabra == i:
            id_palabra = random.randint(1, ultimo_id[0][0])
    return consulta_generica(conn, f'select palabra from palabras where id ={id_palabra}')



