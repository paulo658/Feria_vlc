USE basededatos;

SELECT 
  a.Nombre_Actividad,i.Nombre_Invitado FROM TRAEN t
JOIN actividad a ON t.Id_actividad= a.Id_actividad
JOIN Invitado i ON t.Cod_Invitado = i.Cod_Invitado
WHERE a.ID_ACTIVIDAD = 1;


INSERT INTO usuarios (Nombre, Edad, Mail, Idioma) VALUES
('Pau',22,'paulopezgarcia5@gmail.com','Español'),
('Pau',20,'gradolipau@gmail.com','Valenciano'),
('Sara',22,'saretachust@gmail.com','Valenciano'),
('Carlos',22,'carloscodvcf@gmail.com','Ingles');

INSERT INTO actividad (Nombre_Actividad, Fecha_Inicio, Fecha_Fin, Sponsor) VALUES
('Salón del Cómic','2025-10-01', '2025-10-03', 'Norma Editorial, Panini'),
('DreamHack Valencia','2025-07-15', '2025-07-18', 'Intel, Logitech, Twitch'),
('2Ruedas','2025-11-10', '2025-11-12', 'Kawasaki, Ducati, Honda'),
('Fiesta y Boda','2025-11-25', '2025-11-27', 'Pronovias, El Corte Inglés'),
('EcoFira','2025-10-20', '2025-10-22', 'Ecoembes, Iberdrola'),
('Mediterránea Gastrónoma','2025-11-05', '2025-11-07', 'Mercadona, Dacsa, Hostelería Valencia');


-- Insertar invitados
INSERT INTO Invitado (Nombre_invitado,Pais,Descripcion) VALUES
('Ibai Llanos', 'España', 'Streamer y comunicador digital'),
('Paco Roca', 'España', 'Ilustrador y autor de cómics'),
('La Pija y la Quinqui', 'España', 'Podcast cultural con enfoque social'),
('Ferran Adrià', 'España', 'Chef reconocido internacionalmente'),
('Nuria Roca', 'España', 'Presentadora y comunicadora'),
('Verónica Blume', 'Alemania', 'Modelo y activista de vida saludable'),
('Álex Márquez', 'España', 'Piloto de motociclismo'),
('Jorge Cremades', 'España', 'Creador de contenido humorístico');

-- Relacionarlos con actividades
-- Supongamos que IDs de actividades: 
-- 1 = Salón del Cómic, 2 = DreamHack, 3 = 2Ruedas, 4 = Fiesta y Boda, 5 = EcoFira, 6 = Mediterránea Gastrónoma

INSERT INTO TRAEN (Id_actividad, Cod_Invitado) VALUES
(2, 1), -- Ibai → DreamHack
(1, 2), -- Paco Roca → Salón del Cómic
(6, 3), -- La Pija y la Quinqui → Gastrónoma
(6, 4), -- Ferran Adrià → Gastrónoma
(4, 5), -- Nuria Roca → Fiesta y Boda
(5, 6), -- Verónica Blume → EcoFira
(3, 7), -- Álex Márquez → 2Ruedas
(1, 8); -- Jorge Cremades → Salón del Cómic

INSERT INTO Encuesta(Nombre_Encuesta, Descripcion) VALUES
('Opinión sobre el Salón del Cómic', 'Encuesta para conocer la experiencia del público en el Salón del Cómic de Valencia'),
('Opinión sobre Actividades', 'Valoración de las actividades y eventos específicos'),
('Interés en futuros eventos', 'Preferencias sobre futuros temas y formatos de feria'),
('Accesibilidad y servicios', 'Opinión sobre accesos, limpieza y servicios del recinto'),
('Recomendación', '¿Recomendarías la feria a otras personas? ¿Por qué?');

INSERT INTO hacen (Cod_User, Id_encuesta) VALUES
(1, 1),  -- Pau (Español) → Encuesta sobre Salón del Cómic
(2, 1),  -- Pau (Valenciano) → Opinión sobre Actividades
(3, 1),  -- Sara → Interés en futuros eventos
(4, 1);  -- Carlos → Encuesta sobre Salón del Cómic
