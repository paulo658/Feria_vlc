Create database IF NOT EXISTS basededatos;
USE basededatos;
-- Tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios(
Cod_User INT PRIMARY KEY AUTO_INCREMENT,
Nombre Varchar(45)NOT NULL,
Edad INT NOT NULL,
Mail VARCHAR(255) UNIQUE,
Idioma TEXT
);
-- Tabla actividad
CREATE TABLE IF NOT EXISTS actividad(
Id_actividad INT PRIMARY KEY AUTO_INCREMENT,
Nombre_Actividad VARCHAR(100) NOT NULL,
Fecha_Inicio DATE,
Fecha_Fin Date,
Sponsor VARCHAR(200)
);
-- Tabla encuesta
CREATE TABLE IF NOT EXISTS Encuesta(
Id_encuesta INT PRIMARY KEY auto_increment,
Nombre_Encuesta VARCHAR(75),
Descripcion text
);
-- Tabla invitado
CREATE TABLE IF NOT EXISTS Invitado(
Cod_Invitado INT PRIMARY KEY AUTO_INCREMENT,
Nombre_invitado VARCHAR(45),
Pais VARCHAR(75),
Descripcion TEXT
);
-- Tabla Subscrito (relacion Usuario-Actividad)
CREATE TABLE IF NOT EXISTS  Subscrito(
Cod_User INT,
Id_actividad INT,
PRIMARY KEY (Cod_User,Id_actividad),
FOREIGN KEY (Cod_User) REFERENCES usuarios(Cod_User),
FOREIGN KEY (Id_actividad) REFERENCES actividad(Id_actividad)
);
-- Tabla hacen (relacion usuarios-encuesta)
CREATE TABLE IF NOT EXISTS hacen(
Cod_User INT,
Id_encuesta INT,
PRIMARY KEY (Cod_User,Id_encuesta),
FOREIGN KEY (Cod_User) REFERENCES usuarios(Cod_User),
FOREIGN KEY (Id_encuesta) REFERENCES Encuesta(Id_encuesta)
);
-- Tabla Traen (relacion Actividad- Invitado)
CREATE TABLE IF NOT EXISTS  TRAEN(
Cod_invitado INT,
Id_actividad INT,
PRIMARY KEY (Cod_invitado,Id_actividad),
FOREIGN KEY (Cod_invitado) REFERENCES Invitado(Cod_invitado),
FOREIGN KEY (Id_actividad) REFERENCES actividad(Id_actividad)
);
