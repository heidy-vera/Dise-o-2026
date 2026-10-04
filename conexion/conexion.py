import mysql.connector


def conectar_bd():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dulces2026!",
        database="dulces_delicias"
    )

    return conexion