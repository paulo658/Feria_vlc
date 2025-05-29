#!/usr/bin/env python3

"""
@Name: Correos.py
@Author: Pau Lopez ft. Carlos Castañeda
"""



import mysql.connector
import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def leer_credenciales(ruta):
    credenciales = {}
    if not os.path.exists(ruta):
        print(f"No se ha encontrado el archivo de credenciales en: {ruta}")
        sys.exit(1)
    with open(ruta, 'r') as f:
        for linea in f:
            if '=' in linea:
                clave, valor = linea.strip().split('=', 1)
                credenciales[clave.strip()] = valor.strip()
    return credenciales

# ---------------------------------
# CONFIGURACIÓN DE RUTAS Y CREDENCIALES

ruta_script = os.path.dirname(__file__)
ruta_pass = os.path.join(ruta_script, 'pass.inf')
ruta_pass = os.path.normpath(ruta_pass)

# Leer credenciales SMTP y BD
datos = leer_credenciales(ruta_pass)

EMAIL = datos.get('mail')
APP_PASSWORD = datos.get('pass')

if not EMAIL or not APP_PASSWORD:
    print("No se encontraron las credenciales 'mail' o 'pass' en el archivo pass.inf")
    sys.exit(1)

# Conexión a la base de datos (ajusta si quieres usar las credenciales del archivo)
db_config = {
    'host': datos.get('db_host', '54.224.194.166'),
    'user': datos.get('db_user', 'usuario'),
    'password': datos.get('db_password', 'clave_usuario'),
    'database': datos.get('db_nombre', 'basededatos'),
    'port': int(datos.get('db_port', 3306))
}

try:
    conexion = mysql.connector.connect(**db_config)
except mysql.connector.Error as err:
    print(f"Error conectando a la base de datos: {err}")
    sys.exit(1)

cursor = conexion.cursor(dictionary=True)

# Consulta usuarios
query = "SELECT Nombre, Mail FROM usuarios"  # Ajusta la tabla y campos si es necesario
cursor.execute(query)

# Ruta archivo HTML base
html_final = os.path.join(ruta_script, '..', 'supuesto1.html')
html_final = os.path.normpath(html_final)

if not os.path.exists(html_final):
    print(f"No se encontró el archivo HTML en: {html_final}")
    sys.exit(1)

with open(html_final, 'r', encoding='utf-8') as f:
    html_template = f.read()

# ---------------- ENVÍO DE CORREOS ------------------

smtp_server = "smtp.office365.com"
smtp_port = 587

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(EMAIL, APP_PASSWORD)
except Exception as e:
    print(f"Error conectando o autenticando en el servidor SMTP: {e}")
    cursor.close()
    conexion.close()
    sys.exit(1)

print(f"Se enviarán correos a {cursor.rowcount} usuarios...")

enviados = 0
errores = 0

for row in cursor:
    nombre = row.get('nombre') or row.get('Nombre')  # por si acaso
    email = row.get('email') or row.get('Mail')
    if not nombre or not email:
        print(f"Datos incompletos para registro: {row}")
        continue

    html_personalizado = html_template.replace('{{nombre}}', nombre)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "¡Tu entrada para el Salón del Cómic de Valencia!"
    msg['From'] = EMAIL
    msg['To'] = email
    msg.attach(MIMEText(html_personalizado, 'html'))

    try:
        server.send_message(msg)
        print(f"Correo enviado a {nombre} <{email}>")
        enviados += 1
        # Aquí podrías añadir actualización para marcar correo enviado en BD, si quieres.
    except Exception as e:
        print(f"Error enviando correo a {email}: {e}")
        errores += 1

server.quit()
cursor.close()
conexion.close()

print(f"Proceso terminado. Correos enviados: {enviados}, errores: {errores}")
