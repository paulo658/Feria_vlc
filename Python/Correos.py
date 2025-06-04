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

def crear_datos_prueba(conexion, cursor):
    try:
        # Verificar si ya existen las actividades
        print("Verificando actividades...")
        cursor.execute("SELECT COUNT(*) FROM actividad")
        if cursor.fetchone()[0] == 0:
            print("Creando actividades...")
            cursor.execute("""
                INSERT INTO actividad (Id_actividad, Nombre_Actividad, Fecha_Inicio, Fecha_Fin, Sponsor) VALUES
                (1, 'Salón del Cómic', '2025-10-01', '2025-10-03', 'Norma Editorial, Panini'),
                (2, '2Ruedas', '2025-11-10', '2025-11-12', 'Kawasaki, Ducati, Honda')
            """)
            print("✅ Actividades creadas")

        # Crear usuario de prueba si no existe
        print("Verificando usuario de prueba...")
        cursor.execute("SELECT Cod_User FROM usuarios WHERE Mail = %s", ("paulopgar2@alu.edu.gva.es",))
        resultado = cursor.fetchone()
        
        if resultado:
            cod_user = resultado[0]
            print(f"✅ Usuario existente encontrado con Cod_User: {cod_user}")
        else:
            print("Creando usuario de prueba...")
            cursor.execute(
                "INSERT INTO usuarios (Nombre, Mail, Edad, Idioma) VALUES (%s, %s, %s, %s)",
                ("Usuario Prueba", "paulopgar2@alu.edu.gva.es", 25, "ES")
            )
            cod_user = cursor.lastrowid
            print(f"✅ Usuario creado con Cod_User: {cod_user}")

        # Crear suscripciones si no existen
        print("Verificando suscripciones...")
        cursor.execute(
            "SELECT Id_actividad FROM Subscrito WHERE Cod_User = %s",
            (cod_user,)
        )
        suscripciones_existentes = [row[0] for row in cursor.fetchall()]

        for actividad_id in [1, 2]:  # Salón del Cómic y 2Ruedas
            if actividad_id not in suscripciones_existentes:
                print(f"Creando suscripción para actividad {actividad_id}...")
                cursor.execute(
                    "INSERT INTO Subscrito (Cod_User, Id_actividad) VALUES (%s, %s)",
                    (cod_user, actividad_id)
                )
                print(f"✅ Suscripción creada para actividad {actividad_id}")

        conexion.commit()
        print("✅ Datos de prueba creados/verificados correctamente")
        
        # Mostrar resumen de suscripciones
        cursor.execute("""
            SELECT a.Nombre_Actividad
            FROM Subscrito s
            JOIN actividad a ON s.Id_actividad = a.Id_actividad
            WHERE s.Cod_User = %s
        """, (cod_user,))
        
        print("\nSuscripciones actuales:")
        for (nombre_actividad,) in cursor.fetchall():
            print(f"- {nombre_actividad}")
            
        return True
    except mysql.connector.Error as err:
        print(f"❌ Error en la base de datos: {err}")
        conexion.rollback()
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        conexion.rollback()
        return False

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
        "1": ("Salón del Cómic", "supuesto1.html", "¡Tu entrada para el Salón del Cómic de Valencia!", 1),
        "2": ("2Ruedas", "supuesto2.html", "¡Tu entrada para 2Ruedas!", 2),
    }

    if len(sys.argv) < 2 or sys.argv[1] not in ["1", "2", "3", "4"]:
        print("Uso: python Correos.py [1|2|3|4]")
        print("1: Salón del Cómic (Id_actividad = 1)")
        print("2: 2Ruedas (Id_actividad = 2)")
        print("3: Añadir nuevo usuario")
        print("4: Crear datos de prueba")
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

            # Insertar el usuario
            cursor.execute(
                "INSERT INTO usuarios (Nombre, Mail, Edad, Idioma) VALUES (%s, %s, %s, %s)",
                (nombre, mail, edad, idioma)
            )
            cod_user = cursor.lastrowid

            # Mostrar actividades disponibles
            print("\nActividades disponibles:")
            cursor.execute("SELECT Id_actividad, Nombre_Actividad FROM actividad")
            actividades = cursor.fetchall()
            for id_act, nombre_act in actividades:
                print(f"{id_act}. {nombre_act}")

            # Solicitar selección de actividad
            while True:
                actividad = input("\nSelecciona el número de la actividad (0 para terminar): ").strip()
                if actividad == "0":
                    break
                
                try:
                    actividad_id = int(actividad)
                    if actividad_id in [act[0] for act in actividades]:
                        cursor.execute(
                            "INSERT INTO Subscrito (Cod_User, Id_actividad) VALUES (%s, %s)",
                            (cod_user, actividad_id)
                        )
                        print(f"✅ Usuario suscrito a la actividad {actividad_id}")
                    else:
                        print("❌ Actividad no válida")
                except ValueError:
                    print("❌ Por favor, introduce un número válido")

            conexion.commit()
            print("✅ Usuario añadido correctamente.")
            
            # Mostrar resumen de suscripciones
            cursor.execute("""
                SELECT a.Nombre_Actividad
                FROM Subscrito s
                JOIN actividad a ON s.Id_actividad = a.Id_actividad
                WHERE s.Cod_User = %s
            """, (cod_user,))
            
            print("\nSuscripciones realizadas:")
            suscripciones = cursor.fetchall()
            if suscripciones:
                for (nombre_actividad,) in suscripciones:
                    print(f"- {nombre_actividad}")
            else:
                print("No se realizaron suscripciones")

            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"Error añadiendo usuario: {e}")
            sys.exit(1)
        sys.exit(0)

    elif opcion == "4":
        try:
            print("Conectando a la base de datos...")
            conexion = mysql.connector.connect(**db_config)
            print("✅ Conexión a la base de datos exitosa")
            cursor = conexion.cursor()
            
            if crear_datos_prueba(conexion, cursor):
                print("✅ Datos de prueba creados exitosamente")
            else:
                print("❌ Error al crear datos de prueba")
            
            cursor.close()
            conexion.close()
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

    elif opcion == "1":
        # Envío de correos solo a usuarios suscritos a "Salón del Cómic"
        try:
            print("Conectando a la base de datos...")
            conexion = mysql.connector.connect(**db_config)
            print("✅ Conexión a la base de datos exitosa")
            
            cursor = conexion.cursor(dictionary=True)
            print("Ejecutando consulta para obtener usuarios del Salón del Cómic...")
            query = """
                SELECT u.Nombre, u.Mail
                FROM usuarios u
                JOIN Subscrito s ON u.Cod_User = s.Cod_User
                WHERE s.Id_actividad = %s
            """
            nombre_plantilla, archivo_html, asunto, id_actividad = plantillas[opcion]
            cursor.execute(query, (id_actividad,))
            resultados = cursor.fetchall()
            total_usuarios = len(resultados)
            
            if total_usuarios == 0:
                print("⚠️ No se encontraron usuarios suscritos al Salón del Cómic")
                cursor.close()
                conexion.close()
                sys.exit(1)
            
            print(f"✅ Se encontraron {total_usuarios} usuarios suscritos")
            
            html_final = os.path.join(ruta_script, '..', 'HTML', archivo_html)
            html_final = os.path.normpath(html_final)

            if not os.path.exists(html_final):
                print(f"❌ No se encontró el archivo HTML en: {html_final}")
                sys.exit(1)
            
            print(f"✅ Archivo HTML encontrado: {html_final}")

            with open(html_final, 'r', encoding='utf-8') as f:
                html_template = f.read()
                print("✅ Plantilla HTML cargada correctamente")

            # Configuración SMTP para Office 365
            smtp_server = "smtp.office365.com"
            smtp_port = 587

            try:
                print(f"Conectando al servidor SMTP {smtp_server}:{smtp_port}...")
                server = smtplib.SMTP(smtp_server, smtp_port)
                print("Iniciando TLS...")
                server.starttls()
                print(f"Intentando autenticar con la cuenta {EMAIL}...")
                server.login(EMAIL, APP_PASSWORD)
                print("✅ Conexión SMTP exitosa")
            except Exception as e:
                print(f"Error conectando o autenticando en el servidor SMTP: {e}")
                cursor.close()
                conexion.close()
                sys.exit(1)

            print(f"Se enviarán correos a {total_usuarios} usuarios...")

            enviados = 0
            errores = 0

            for row in resultados:
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
            print("Conectando a la base de datos...")
            conexion = mysql.connector.connect(**db_config)
            print("✅ Conexión a la base de datos exitosa")
            
            cursor = conexion.cursor(dictionary=True)
            print("Ejecutando consulta para obtener usuarios de 2Ruedas...")
            query = """
                SELECT u.Nombre, u.Mail
                FROM usuarios u
                JOIN Subscrito s ON u.Cod_User = s.Cod_User
                WHERE s.Id_actividad = %s
            """
            nombre_plantilla, archivo_html, asunto, id_actividad = plantillas[opcion]
            cursor.execute(query, (id_actividad,))
            resultados = cursor.fetchall()
            total_usuarios = len(resultados)
            
            if total_usuarios == 0:
                print("⚠️ No se encontraron usuarios suscritos a 2Ruedas")
                cursor.close()
                conexion.close()
                sys.exit(1)
            
            print(f"✅ Se encontraron {total_usuarios} usuarios suscritos")
            
            html_final = os.path.join(ruta_script, '..', 'HTML', archivo_html)
            html_final = os.path.normpath(html_final)

            if not os.path.exists(html_final):
                print(f"❌ No se encontró el archivo HTML en: {html_final}")
                sys.exit(1)
            
            print(f"✅ Archivo HTML encontrado: {html_final}")

            with open(html_final, 'r', encoding='utf-8') as f:
                html_template = f.read()
                print("✅ Plantilla HTML cargada correctamente")

            # Configuración SMTP para Office 365
            smtp_server = "smtp.office365.com"
            smtp_port = 587

            try:
                print(f"Conectando al servidor SMTP {smtp_server}:{smtp_port}...")
                server = smtplib.SMTP(smtp_server, smtp_port)
                print("Iniciando TLS...")
                server.starttls()
                print(f"Intentando autenticar con la cuenta {EMAIL}...")
                server.login(EMAIL, APP_PASSWORD)
                print("✅ Conexión SMTP exitosa")
            except Exception as e:
                print(f"Error conectando o autenticando en el servidor SMTP: {e}")
                cursor.close()
                conexion.close()
                sys.exit(1)

            print(f"Se enviarán correos a {total_usuarios} usuarios...")

            enviados = 0
            errores = 0

            for row in resultados:
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
