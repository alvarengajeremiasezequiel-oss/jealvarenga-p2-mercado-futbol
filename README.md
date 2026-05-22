# pipeline-jugadores-de-futbol

## Arquitectura general del pipeline

### Extracción
Se emplea el módulo de kagglehub para python para descargar el dataset localmente. Se recupera el path con el dataset y se guarda en una variable local $DATASET_PATH.

### Capa raw
EL script `loadData.py` se encarga de subir a snowflake los archivos del dataset, siempre de forma idempotente. En este paso se imprimen el nuevo número de filas de cada tabla.

### Capa silver
Para la actualización de datos, dado el tamaño del dataset, se ha decidido simplificar el modelo reconstruyendo las tablas del dataset con cada actualización. Respecto al modelo de esta capa, `silver.fct_player_season` tiene como clave primaria player_id, season, club_id y competition_id, pero competition_id, en los datos de la capa raw, puede ser nulo, por lo que se parchea con un -1, indicador de que para esa fila no hay competiciones existentes.

### Capa gold
La tabla de hechos y dimensiones se mantienen iguales respecto a silver, excepto por la adición de `gold.dim_season`, que recoje datos agregados globales de cada temporada, y se identifica por la temporada (que al ser anual es el año).

## Tecnologías utilizadas
El proyecto emplea el módulo de kagglehub, el conector de snowflake para python, requiere una cuenta de snowflake con un warehouse existente, github actions y finalmente un cliente de powerBI para la visualización del informe.

## Pasos para ejecutar el proyecto
Se modifica el script `Generate-Snowflake-Keypair.py` para usar el usuario deseado. Se ejecuta el script, y se sube a snowflake el archivo generado llamado `register_public_key.sql` . Se ejecuta este último archivo en snowflake.

Al igual que en el proyecto anterior, se usa github actions para ejecución automática. Se deben añadir los siguientes secretos al repositorio:
- SNOWFLAKE_ACCOUNT
- SNOWFLAKE_USER
- SNOWFLAKE_PRIVATE_KEY
- SNOWFLAKE_WAREHOUSE
- SNOWFLAKE_DATABASE
- SNOWFLAKE_SCHEMA

En SNOWFLAKE_PRIVATE_KEY se debe añadir el contenido de `snowflake_key.pem`, generado por la ejecución de `generateSnowflakeKeypair.py`.