import sys
from pathlib import Path

from snowflake.snowpark.context import get_active_session

try:
    BASE_DIR = Path(__file__).resolve().parent
except NameError:
    BASE_DIR = Path.cwd()

sys.path.insert(0, str(BASE_DIR))

from src.loader import copy_into_raw, count_raw_rows, stage_has_files
from src.sql_runner import run_sql_file
from src.summary import print_summary

WAREHOUSE = "COMPUTE_WH"

SQL_FILES = {
    "infrastructure": "01_infrastructure.sql",
    "raw": "02_raw.sql",
    "quality": "03_quality.sql",
    "staging": "04_staging.sql",
    "final": [
        "05_final_daily_summary.sql",
        "06_final_hourly_patterns.sql",
        "07_final_zone_analysis.sql",
    ],
}


def title(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def main():
    session = get_active_session()

    title("1/5 - INFRASTRUCTURE")
    run_sql_file(session, SQL_FILES["infrastructure"])
    session.sql(f"USE WAREHOUSE {WAREHOUSE}").collect()

    title("2/5 - RAW")
    run_sql_file(session, SQL_FILES["raw"])

    title("3/5 - CHARGEMENT")
    if not stage_has_files(session):
        print("Le stage TLC_RAW_STAGE est vide.")
        print("Charge le fichier .parquet dans NYC_TAXI_DB_PARTIE_1 > RAW > Stages > TLC_RAW_STAGE,")
        print("puis relance ce script.")
        return "EN ATTENTE DU FICHIER PARQUET"
    copy_into_raw(session)
    print(f"Lignes RAW : {count_raw_rows(session):,}")

    title("4/5 - QUALITE")
    run_sql_file(session, SQL_FILES["quality"], show_results=True)

    title("5/5 - STAGING + FINAL")
    run_sql_file(session, SQL_FILES["staging"])
    for filename in SQL_FILES["final"]:
        run_sql_file(session, filename)

    title("RESUME")
    print_summary(session)

    return "PIPELINE TERMINE"


if __name__ == "__main__":
    print(main())
