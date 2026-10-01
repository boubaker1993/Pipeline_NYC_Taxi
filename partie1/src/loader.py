DATABASE = "NYC_TAXI_DB_PARTIE_1"
SCHEMA = "RAW"
STAGE = "TLC_RAW_STAGE"
FILE_FORMAT = "TLC_PARQUET_FORMAT"
RAW_TABLE = "YELLOW_TAXI_RAW"


def stage_has_files(session):
    stage = f"@{DATABASE}.{SCHEMA}.{STAGE}"
    files = session.sql(f"LIST {stage}").collect()

    for file in files:
        print(f"Fichier sur le stage : {file['name']}")

    return len(files) > 0


def copy_into_raw(session):
    stage = f"@{DATABASE}.{SCHEMA}.{STAGE}"

    copy_sql = f"""
        COPY INTO {DATABASE}.{SCHEMA}.{RAW_TABLE}
        FROM {stage}
        FILE_FORMAT = (FORMAT_NAME = '{DATABASE}.{SCHEMA}.{FILE_FORMAT}')
        MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
        ON_ERROR = 'ABORT_STATEMENT'
    """

    for row in session.sql(copy_sql).collect():
        print(f"COPY : {row}")


def count_raw_rows(session):
    query = f"SELECT COUNT(*) FROM {DATABASE}.{SCHEMA}.{RAW_TABLE}"
    return session.sql(query).collect()[0][0]
