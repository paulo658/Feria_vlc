#!/usr/bin/env python3

import unittest
import mysql.connector
import os
from Correos import leer_credenciales

class TestCorreos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para las pruebas"""
        # Leer credenciales
        ruta_script = os.path.dirname(__file__)
        ruta_pass = os.path.join(ruta_script, 'pass.inf')
        cls.datos = leer_credenciales(ruta_pass)
        
        # Configurar conexión a la base de datos
        cls.db_config = {
            'host': cls.datos['db_host'],
            'user': cls.datos['db_user'],
            'password': cls.datos['db_password'],
            'database': cls.datos['db_nombre'],
            'port': int(cls.datos['db_port'])
        }
        
        # Lista para almacenar IDs de usuarios de prueba
        cls.usuarios_prueba = []
        
        # Crear conexión
        cls.conexion = mysql.connector.connect(**cls.db_config)
        cls.cursor = cls.conexion.cursor(dictionary=True)

    def setUp(self):
        """Se ejecuta antes de cada prueba"""
        self.conexion.start_transaction()

    def tearDown(self):
        """Se ejecuta después de cada prueba"""
        self.conexion.rollback()

    @classmethod
    def tearDownClass(cls):
        """Limpieza final - Eliminar usuarios de prueba"""
        try:
            if cls.usuarios_prueba:
                cls.cursor.execute(
                    "DELETE FROM usuarios WHERE Cod_User IN (%s)" % 
                    ','.join(['%s'] * len(cls.usuarios_prueba)),
                    cls.usuarios_prueba
                )
                cls.conexion.commit()
        finally:
            cls.cursor.close()
            cls.conexion.close()

    def test_crear_usuario(self):
        """Prueba la creación de un usuario"""
        # Insertar usuario de prueba
        self.cursor.execute(
            "INSERT INTO usuarios (Nombre, Mail, Edad, Idioma) VALUES (%s, %s, %s, %s)",
            ("Test User", "test@example.com", 25, "Español")
        )
        self.conexion.commit()
        
        # Obtener el ID del usuario insertado
        self.cursor.execute("SELECT LAST_INSERT_ID() as id")
        usuario_id = self.cursor.fetchone()['id']
        self.usuarios_prueba.append(usuario_id)
        
        # Verificar que el usuario existe
        self.cursor.execute("SELECT * FROM usuarios WHERE Cod_User = %s", (usuario_id,))
        usuario = self.cursor.fetchone()
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario['Nombre'], "Test User")

    def test_suscribir_usuario_actividad(self):
        """Prueba la suscripción de un usuario a una actividad"""
        # Crear usuario de prueba
        self.cursor.execute(
            "INSERT INTO usuarios (Nombre, Mail, Edad, Idioma) VALUES (%s, %s, %s, %s)",
            ("Test Sub User", "test_sub@example.com", 30, "Español")
        )
        usuario_id = self.cursor.fetchone()['id'] if self.cursor.lastrowid else None
        self.usuarios_prueba.append(usuario_id)
        
        # Crear actividad de prueba
        self.cursor.execute(
            "INSERT INTO actividad (Nombre_Actividad, Fecha_Inicio, Fecha_Fin) VALUES (%s, %s, %s)",
            ("Actividad Test", "2024-01-01", "2024-12-31")
        )
        actividad_id = self.cursor.fetchone()['id'] if self.cursor.lastrowid else None
        
        # Suscribir usuario a la actividad
        self.cursor.execute(
            "INSERT INTO Subscrito (Cod_User, Id_actividad) VALUES (%s, %s)",
            (usuario_id, actividad_id)
        )
        
        # Verificar la suscripción
        self.cursor.execute(
            "SELECT * FROM Subscrito WHERE Cod_User = %s AND Id_actividad = %s",
            (usuario_id, actividad_id)
        )
        subscripcion = self.cursor.fetchone()
        self.assertIsNotNone(subscripcion)

    def test_crear_encuesta(self):
        """Prueba la creación de una encuesta y su relación con un usuario"""
        # Crear usuario de prueba
        self.cursor.execute(
            "INSERT INTO usuarios (Nombre, Mail, Edad, Idioma) VALUES (%s, %s, %s, %s)",
            ("Test Survey User", "test_survey@example.com", 28, "English")
        )
        usuario_id = self.cursor.fetchone()['id'] if self.cursor.lastrowid else None
        self.usuarios_prueba.append(usuario_id)
        
        # Crear encuesta
        self.cursor.execute(
            "INSERT INTO Encuesta (Mail, Idioma) VALUES (%s, %s)",
            ("test_survey@example.com", "English")
        )
        encuesta_id = self.cursor.fetchone()['id'] if self.cursor.lastrowid else None
        
        # Relacionar usuario con encuesta
        self.cursor.execute(
            "INSERT INTO hacen (Cod_User, Id_encuesta) VALUES (%s, %s)",
            (usuario_id, encuesta_id)
        )
        
        # Verificar la relación
        self.cursor.execute(
            "SELECT * FROM hacen WHERE Cod_User = %s AND Id_encuesta = %s",
            (usuario_id, encuesta_id)
        )
        relacion = self.cursor.fetchone()
        self.assertIsNotNone(relacion)

if __name__ == '__main__':
    unittest.main() 