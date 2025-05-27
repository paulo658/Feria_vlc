import mysql.connector
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def leer_credenciales(ruta):
    credenciales = {}
    with open(ruta, 'r') as f:
        for linea in f:
            if '=' in linea:
                clave, valor = linea.strip().split('=', 1)
                credenciales[clave.strip()] = valor.strip()
    return credenciales

ruta_script = os.path.dirname(__file__) 

ruta_pass = os.path.join(ruta_script,'pass.inf')
ruta_pass = os.path.normpath(ruta_script)
data = leer_credenciales(ruta_pass)

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="TU_USUARIO",
    password="TU_CONTRASEÑA",
    database="TU_BASE_DE_DATOS"
)


cursor = conexion.cursor(dictionary=True)
cursor.execute("SELECT nombre, email FROM usuarios")  # Cambia 'usuarios' por tu tabla

# Leer el HTML base
with open('c:/Users/quebr/Desktop/PRACTICAS/Feria_vlc/supuesto1.html', 'r', encoding='utf-8') as f:
    html_template = f.read()

# Configura tu servidor SMTP (ejemplo con Gmail)
smtp_server = "smtp.office365.com"
smtp_port = 587
smtp_user = data.get("mail")
smtp_pass = data.get("pass")

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_user, smtp_pass)

for row in cursor:
    nombre = row['nombre']
    email = row['email']
    html_personalizado = html_template.replace('{{nombre}}', nombre)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "¡Tu entrada para el Salón del Cómic de Valencia!"
    msg['From'] = smtp_user
    msg['To'] = email

    part = MIMEText(html_personalizado, 'html')
    msg.attach(part)

    server.sendmail(smtp_user, email, msg.as_string())
    print(f'Correo enviado a {nombre} ({email})')

server.quit()
cursor.close()
conexion.close()