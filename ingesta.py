import mysql.connector
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def leer_datos_mysql(host, user, password, database, tabla, archivo_csv):
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=8005
        )

        cursor = conexion.cursor()
        query = f"SELECT * FROM {tabla}"
        cursor.execute(query)
        columnas = [desc[0] for desc in cursor.description]
        registros = cursor.fetchall()

        df = pd.DataFrame(registros, columns=columnas)
        df.to_csv(archivo_csv, index=False, encoding='utf-8')

        print(f"Datos guardados en {archivo_csv}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def subir_a_s3(nombre_archivo_local, bucket_name, nombre_archivo_s3):
    try:
        s3 = boto3.client('s3')
        s3.upload_file(nombre_archivo_local, bucket_name, nombre_archivo_s3)
        print(f"Archivo '{nombre_archivo_local}' subido exitosamente al bucket '{bucket_name}' como '{nombre_archivo_s3}'")
    except FileNotFoundError:
        print(f"Error: El archivo {nombre_archivo_local} no existe.")
    except NoCredentialsError:
        print("Error: Credenciales AWS no encontradas.")
    except ClientError as e:
        print(f"Error al subir archivo: {e}")

if __name__ == "__main__":
    # Parámetros MySQL
    host_aws = "172.31.31.107"
    usuario = "root"
    contraseña = "utec"
    base_datos = "mysql_c"
    nombre_tabla = "employees"
    archivo_salida = "data.csv"

    # Parámetros AWS S3
    bucket_name = "semana6-s2-ejerciciopropuesto"  # <-- Cambia aquí por tu bucket real
    nombre_s3 = "data.csv"

    # Ejecutar la lectura y guardado
    leer_datos_mysql(host_aws, usuario, contraseña, base_datos, nombre_tabla, archivo_salida)

    # Subir el CSV generado a S3
    subir_a_s3(archivo_salida, bucket_name, nombre_s3)
