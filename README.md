# pipeline-jugadores-de-futbol

## Arquitectura general del pipeline

### Extracción
Se emplea el módulo de kagglehub para python para descargar el dataset localmente. Se recupera el path con el dataset y se guarda en una variable local $DATASET_PATH.

### Capa raw
EL script loadData.py se encarga de subir a snowflake los archivos del dataset, siempre de forma idempotente. En este paso se imprimen el nuevo número de filas de cada tabla.

### Capa silver
Para la actualización de datos, dado el tamaño del dataset, se ha decidido simplificar el modelo reconstruyendo las tablas del dataset con cada actualización.


## Tecnologías utilizadas

## Pasos para ejecutar el proyecto
Se modifica el script Generate-Snowflake-Keypair.py para usar el usuario deseado. Se ejecuta el script, y se sube a snowflake el archivo generado llamado register_public_key.sql . Se ejecuta este último archivo en snowflake.

Al igual que en el proyecto anterior, se usa github actions para ejecución automática. Se deben añadir los siguientes secretos al repositorio:
- SNOWFLAKE_ACCOUNT
- SNOWFLAKE_USER
- SNOWFLAKE_PRIVATE_KEY
- SNOWFLAKE_WAREHOUSE
- SNOWFLAKE_DATABASE
- SNOWFLAKE_SCHEMA

En SNOWFLAKE_PRIVATE_KEY se debe añadir el contenido de snowflake_key.pem, generado por la ejecución de Generate-Snowflake-Keypair.