#!/usr/bin/env python3

"""
@Name: Correos.py
@Author: Pau Lopez
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
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                continue
            if '=' in linea:
                clave, valor = linea.split('=', 1)
                credenciales[clave.strip()] = valor.strip()
    return credenciales

def main():
    # ---------------------------------
    # CONFIGURACIÓN DE RUTAS Y CREDENCIALES

    ruta_script = os.path.dirname(__file__)
    ruta_pass = os.path.join(ruta_script, 'pass.inf')
    ruta_pass = os.path.normpath(ruta_pass)

    # Leer credenciales SMTP y BD
    datos = leer_credenciales(ruta_pass)

    # Comprobar claves obligatorias para SMTP
    for clave in ['mail', 'pass']:
        if clave not in datos:
            print(f"Falta la clave '{clave}' en el archivo pass.inf")
            sys.exit(1)

    EMAIL = datos['mail']
    APP_PASSWORD = datos['pass']

    # Comprobar claves obligatorias para BD
    for clave in ['db_host', 'db_user', 'db_password', 'db_nombre', 'db_port']:
        if clave not in datos:
            print(f"Falta la clave '{clave}' en el archivo pass.inf")
            sys.exit(1)

    db_config = {
        'host': datos['db_host'],
        'user': datos['db_user'],
        'password': datos['db_password'],
        'database': datos['db_nombre'],
        'port': int(datos['db_port'])
    }

    # -------- SELECCIÓN DE PLANTILLA POR ARGUMENTO O INTRODUCCIÓN DE USUARIOS --------
    plantillas = {
        "1": ("Salón del Cómic", "supuesto1.html", "¡Tu entrada para el Salón del Cómic de Valencia!"),
        "2": ("2Ruedas", "supuesto2.html", "¡Tu entrada para 2Ruedas!"),
    }

    if len(sys.argv) < 2 or sys.argv[1] not in ["1", "2", "3"]:
        print("Uso: python Correos.py [1|2|3]")
        print("1: Salón del Cómic")
        print("2: 2Ruedas")
        print("3: Añadir usuario a la base de datos")
        sys.exit(1)

    opcion = sys.argv[1]

    if opcion == "3":
        # Añadir usuario a la base de datos
        try:
            conexion = mysql.connector.connect(**db_config)
            cursor = conexion.cursor()
            nombre = input("Introduce el nombre del usuario: ").strip()
            mail = input("Introduce el correo del usuario: ").strip()
            edad = input("Introduce la edad del usuario: ").strip()
            idioma = input("Introduce el idioma del usuario: ").strip()
            if not nombre or not mail or not edad or not idioma:
                print("Nombre, correo, edad e idioma no pueden estar vacíos.")
                sys.exit(1)
            cursor.execute(
                "INSERT INTO usuarios (Nombre, Mail, Edad, Idioma) VALUES (%s, %s, %s, %s)",
                (nombre, mail, edad, idioma)
            )
            conexion.commit()
            print("Usuario añadido correctamente.")
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"Error añadiendo usuario: {e}")
            sys.exit(1)
        sys.exit(0)

    elif opcion == "1":
        # Envío de correos solo a usuarios suscritos a "Salón del Cómic"
        try:
            conexion = mysql.connector.connect(**db_config)
            cursor = conexion.cursor(dictionary=True)
            query = """
                SELECT u.Nombre, u.Mail
                FROM usuarios u
                JOIN Subscrito s ON u.Cod_User = s.Cod_User
                JOIN actividad a ON s.Id_actividad = a.Id_actividad
                WHERE a.Nombre_Actividad = 'Salón del Cómic'
            """
            cursor.execute(query)
            nombre_plantilla, archivo_html, asunto = plantillas[opcion]
            html_final = os.path.join(ruta_script, '..', 'HTML', archivo_html)
            html_final = os.path.normpath(html_final)

            if not os.path.exists(html_final):
                print(f"No se encontró el archivo HTML en: {html_final}")
                sys.exit(1)

            with open(html_final, 'r', encoding='utf-8') as f:
                html_template = f.read()

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
                nombre = row.get('nombre') or row.get('Nombre')
                email = row.get('email') or row.get('Mail')
                if not nombre or not email:
                    print(f"Datos incompletos para registro: {row}")
                    continue

                html_personalizado = html_template.replace('{{nombre}}', nombre)

                msg = MIMEMultipart('alternative')
                msg['Subject'] = asunto
                msg['From'] = EMAIL
                msg['To'] = email
                msg.attach(MIMEText(html_personalizado, 'html'))

                try:
                    server.send_message(msg)
                    print(f"Correo enviado a {nombre} <{email}>")
                    enviados += 1
                except Exception as e:
                    print(f"Error enviando correo a {email}: {e}")
                    errores += 1

            server.quit()
            cursor.close()
            conexion.close()

            print(f"Proceso terminado. Correos enviados: {enviados}, errores: {errores}")
        except Exception as e:
            print(f"Error en el envío de correos: {e}")
            sys.exit(1)

    elif opcion == "2":
        # Envío de correos solo a usuarios suscritos a "2Ruedas"
        try:
            conexion = mysql.connector.connect(**db_config)
            cursor = conexion.cursor(dictionary=True)
            query = """
                SELECT u.Nombre, u.Mail
                FROM usuarios u
                JOIN Subscrito s ON u.Cod_User = s.Cod_User
                JOIN actividad a ON s.Id_actividad = a.Id_actividad
                WHERE a.Nombre_Actividad = '2Ruedas'
            """
            cursor.execute(query)
            nombre_plantilla, archivo_html, asunto = plantillas[opcion]
            html_final = os.path.join(ruta_script, '..', 'HTML', archivo_html)
            html_final = os.path.normpath(html_final)

            if not os.path.exists(html_final):
                print(f"No se encontró el archivo HTML en: {html_final}")
                sys.exit(1)

            with open(html_final, 'r', encoding='utf-8') as f:
                html_template = f.read()

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
                nombre = row.get('nombre') or row.get('Nombre')
                email = row.get('email') or row.get('Mail')
                if not nombre or not email:
                    print(f"Datos incompletos para registro: {row}")
                    continue

                html_personalizado = html_template.replace('{{nombre}}', nombre)

                msg = MIMEMultipart('alternative')
                msg['Subject'] = asunto
                msg['From'] = EMAIL
                msg['To'] = email
                msg.attach(MIMEText(html_personalizado, 'html'))

                try:
                    server.send_message(msg)
                    print(f"Correo enviado a {nombre} <{email}>")
                    enviados += 1
                except Exception as e:
                    print(f"Error enviando correo a {email}: {e}")
                    errores += 1

            server.quit()
            cursor.close()
            conexion.close()

            print(f"Proceso terminado. Correos enviados: {enviados}, errores: {errores}")
        except Exception as e:
            print(f"Error en el envío de correos: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
