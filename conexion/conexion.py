import mysql.connector


def conectar_bd():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tu_contraseña-aqui",
        database="dulces_delicias"
    )

    return conexion