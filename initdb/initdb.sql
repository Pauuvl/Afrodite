-- 1) Crear/asegurar el rol de la app (en DO porque aquí sí se permite IF)
DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'afrodite_usr') THEN
      -- Puedes usar CREATE USER también; CREATE ROLE + LOGIN es equivalente
      CREATE ROLE afrodite_usr LOGIN PASSWORD 'afrodite_pwd';
   ELSE
      -- Si ya existe, asegurar login y actualizar contraseña
      ALTER ROLE afrodite_usr WITH LOGIN PASSWORD 'afrodite_pwd';
   END IF;
END
$$;

-- 2) Crear la base si no existe (OJO: NO dentro de DO; CREATE DATABASE no admite transacción)
-- Este patrón usa psql y \gexec para ejecutar la sentencia devuelta por SELECT.
-- Los scripts en /docker-entrypoint-initdb.d/ se ejecutan con psql, así que funciona.
SELECT 'CREATE DATABASE afrodite OWNER afrodite_usr'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'afrodite')\gexec

-- 3) Ajustar privilegios en la base (conéctate primero a esa base)
\connect afrodite

-- Asegurar propietario del esquema público para que la app pueda crear objetos
ALTER SCHEMA public OWNER TO afrodite_usr;

-- (Opcional) Conceder privilegios por defecto para objetos futuros creados por el superusuario
-- Esto afecta solo objetos creados por el rol que ejecuta estas sentencias.
-- ALTER DEFAULT PRIVILEGES GRANT ALL ON TABLES TO p2usr;
-- ALTER DEFAULT PRIVILEGES GRANT ALL ON SEQUENCES TO p2usr;
-- ALTER DEFAULT PRIVILEGES GRANT ALL ON FUNCTIONS TO p2usr;