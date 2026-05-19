-------------------------------------------
-- Create database, schema and stage
-------------------------------------------
CREATE DATABASE IF NOT EXISTS JUGADORES_FUTBOL_DB
    COMMENT = 'DB asociado al reto 2: Sistema analítico de datos de jugadores de fútbol';
USE DATABASE CONTRATOS_MENORES_DB;
CREATE SCHEMA IF NOT EXISTS RAW;
CREATE SCHEMA IF NOT EXISTS SILVER;
CREATE SCHEMA IF NOT EXISTS GOLD;
USE SCHEMA RAW;
CREATE STAGE IF NOT EXISTS raw_data;

-------------------------------------------
-- Create file format
-------------------------------------------
CREATE FILE FORMAT IF NOT EXISTS JUGADORES_FUTBOL_DB.PUBLIC.ff_jugadores_csv
    TYPE = CSV
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('', 'NULL')
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    TRIM_SPACE = TRUE;

