#!/usr/bin/env python3

import unittest
import mysql.connector
import os
import sys
from Correos import leer_credenciales

def run_specific_test(test_name=None):
    """Ejecuta un test específico o todos los tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCorreos)
    if test_name:
        # Filtrar los tests para ejecutar solo el especificado
        suite = unittest.TestSuite([test for test in suite if test.id().split('.')[-1] == test_name])
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)

class TestCorreos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para las pruebas"""
        print("\n🔧 Iniciando configuración de pruebas...")
        
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
        cls.actividades_prueba = []
        cls.encuestas_prueba = []
        
        try:
            # Crear conexión
            cls.conexion = mysql.connector.connect(**cls.db_config)
            cls.cursor = cls.conexion.cursor(dictionary=True)
            print("✅ Conexión a la base de datos establecida")
            
            # Verificar estructura de la tabla Encuesta
            cls.cursor.execute("DESCRIBE Encuesta")
            cls.estructura_encuesta = {row['Field']: row['Type'] for row in cls.cursor.fetchall()}
            print("\nEstructura de la tabla Encuesta:")
            for campo, tipo in cls.estructura_encuesta.items():
                print(f"- {campo}: {tipo}")
            
        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            sys.exit(1)

    def setUp(self):
        """Se ejecuta antes de cada prueba"""
        try:
            self.conexion.rollback()  # Asegurar que no hay transacciones pendientes
        except:
            pass
        self.conexion.start_transaction()
        print(f"\n🧪 Iniciando prueba: {self._testMethodName}")

    def tearDown(self):
        """Se ejecuta después de cada prueba"""
        try:
            self.conexion.rollback()
        except:
            pass
        print(f"✅ Finalizada prueba: {self._testMethodName}")

    @classmethod
    def tearDownClass(cls):
        """Limpieza final - Eliminar datos de prueba"""
        print("\n🧹 Limpiando datos de prueba...")
        try:
            # Asegurar que no hay transacciones pendientes
            try:
                cls.conexion.rollback()
            except:
                pass
                
            # Eliminar relaciones primero
            if cls.usuarios_prueba:
                cls.cursor.execute(
                    "DELETE FROM Subscrito WHERE Cod_User IN (%s)" % 
                    ','.join(['%s'] * len(cls.usuarios_prueba)),
                    cls.usuarios_prueba
                )
                cls.cursor.execute(
                    "DELETE FROM hacen WHERE Cod_User IN (%s)" % 
                    ','.join(['%s'] * len(cls.usuarios_prueba)),
                    cls.usuarios_prueba
                )
                cls.cursor.execute(
                    "DELETE FROM usuarios WHERE Cod_User IN (%s)" % 
                    ','.join(['%s'] * len(cls.usuarios_prueba)),
                    cls.usuarios_prueba
                )

            if cls.actividades_prueba:
                cls.cursor.execute(
                    "DELETE FROM actividad WHERE Id_actividad IN (%s)" % 
                    ','.join(['%s'] * len(cls.actividades_prueba)),
                    cls.actividades_prueba
                )

            if cls.encuestas_prueba:
                cls.cursor.execute(
                    "DELETE FROM Encuesta WHERE Id_encuesta IN (%s)" % 
                    ','.join(['%s'] * len(cls.encuestas_prueba)),
                    cls.encuestas_prueba
                )

            cls.conexion.commit()
            print("✅ Datos de prueba eliminados correctamente")
        except Exception as e:
            print(f"❌ Error limpiando datos de prueba: {e}")
        finally:
            cls.cursor.close()
            cls.conexion.close()
            print("✅ Conexión cerrada")

    def test_01_crear_usuario(self):
        """Prueba la creación de un usuario"""
        print("\n➡️ Probando creación de usuario")
        try:
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
            self.assertIsNotNone(usuario, "El usuario no fue creado")
            self.assertEqual(usuario['Nombre'], "Test User", "El nombre no coincide")
            self.assertEqual(usuario['Mail'], "test@example.com", "El email no coincide")
            print("✅ Usuario creado y verificado correctamente")
        except Exception as e:
            self.fail(f"Error en la prueba: {e}")

    def test_02_suscribir_usuario_actividad(self):
        """Prueba la suscripción de un usuario a una actividad"""
        print("\n➡️ Probando suscripción a actividad")
        try:
            # Crear usuario de prueba
            self.cursor.execute(
                "INSERT INTO usuarios (Nombre, Mail, Edad, Idioma) VALUES (%s, %s, %s, %s)",
                ("Test Sub User", "test_sub@example.com", 30, "Español")
            )
            usuario_id = self.cursor.lastrowid
            self.usuarios_prueba.append(usuario_id)
            
            # Crear actividad de prueba
            self.cursor.execute(
                "INSERT INTO actividad (Nombre_Actividad, Fecha_Inicio, Fecha_Fin) VALUES (%s, %s, %s)",
                ("Actividad Test", "2024-01-01", "2024-12-31")
            )
            actividad_id = self.cursor.lastrowid
            self.actividades_prueba.append(actividad_id)
            
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
            self.assertIsNotNone(subscripcion, "La suscripción no fue creada")
            print("✅ Suscripción creada y verificada correctamente")
        except Exception as e:
            self.fail(f"Error en la prueba: {e}")

    def test_03_crear_encuesta(self):
        """Prueba la creación de una encuesta y su relación con un usuario"""
        print("\n➡️ Probando creación de encuesta")
        try:
            # Crear usuario de prueba
            self.cursor.execute(
                "INSERT INTO usuarios (Nombre, Mail, Edad, Idioma) VALUES (%s, %s, %s, %s)",
                ("Test Survey User", "test_survey@example.com", 28, "English")
            )
            usuario_id = self.cursor.lastrowid
            self.usuarios_prueba.append(usuario_id)
            
            # Crear encuesta con los campos correctos
            self.cursor.execute(
                "INSERT INTO Encuesta (Nombre_Encuesta, Descripcion) VALUES (%s, %s)",
                ("Encuesta de Satisfacción", "Encuesta para evaluar la experiencia del usuario")
            )
            encuesta_id = self.cursor.lastrowid
            self.encuestas_prueba.append(encuesta_id)
            
            # Relacionar usuario con encuesta
            self.cursor.execute(
                "INSERT INTO hacen (Cod_User, Id_encuesta) VALUES (%s, %s)",
                (usuario_id, encuesta_id)
            )
            
            # Verificar la encuesta
            self.cursor.execute(
                "SELECT * FROM Encuesta WHERE Id_encuesta = %s",
                (encuesta_id,)
            )
            encuesta = self.cursor.fetchone()
            self.assertIsNotNone(encuesta, "La encuesta no fue creada")
            self.assertEqual(encuesta['Nombre_Encuesta'], "Encuesta de Satisfacción", "El nombre de la encuesta no coincide")
            self.assertEqual(encuesta['Descripcion'], "Encuesta para evaluar la experiencia del usuario", "La descripción no coincide")
            
            # Verificar la relación
            self.cursor.execute(
                "SELECT * FROM hacen WHERE Cod_User = %s AND Id_encuesta = %s",
                (usuario_id, encuesta_id)
            )
            relacion = self.cursor.fetchone()
            self.assertIsNotNone(relacion, "La relación usuario-encuesta no fue creada")
            print("✅ Encuesta creada y verificada correctamente")
        except Exception as e:
            self.fail(f"Error en la prueba: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Si se proporciona un argumento, ejecutar el test específico
        test_name = f"test_0{sys.argv[1]}_" + {
            "1": "crear_usuario",
            "2": "suscribir_usuario_actividad",
            "3": "crear_encuesta"
        }.get(sys.argv[1])
        if test_name:
            run_specific_test(test_name)
        else:
            print("Uso: python test_correos.py [1|2|3]")
            print("1: Probar creación de usuario")
            print("2: Probar suscripción a actividad")
            print("3: Probar creación de encuesta")
            print("Sin argumentos: Ejecutar todas las pruebas")
    else:
        # Sin argumentos, ejecutar todos los tests
        unittest.main(verbosity=2) 