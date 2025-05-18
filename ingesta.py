import mysql.connector
import pandas as pd

def leer_datos_mysql(host, user, password, database, tabla, archivo_csv):
    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306  # Cambia si usas otro puerto
        )

        # Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()

        # Ejecutar la consulta para obtener todos los registros
        query = f"SELECT * FROM {tabla}"
        cursor.execute(query)

        # Obtener los nombres de columnas
        columnas = [desc[0] for desc in cursor.description]

        # Obtener todos los registros
        registros = cursor.fetchall()

        # Crear un DataFrame con los datos
        df = pd.DataFrame(registros, columns=columnas)

        # Guardar en archivo CSV
        df.to_csv(archivo_csv, index=False, encoding='utf-8')

        print(f"Datos guardados en {archivo_csv}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

if __name__ == "__main__":
    # Parámetros de conexión (modifica con tus datos)
    host_aws = "172.31.31.107"
    usuario = "root"
    contraseña = "utec"
    base_datos = "mysql_c"
    nombre_tabla = "employees"
    archivo_salida = "data.csv"

    leer_datos_mysql(host_aws, usuario, contraseña, base_datos, nombre_tabla, archivo_salida)
