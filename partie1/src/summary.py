DATABASE = "NYC_TAXI_DB_PARTIE_1"

SUMMARY_TABLES = [
    "STAGING.YELLOW_TAXI",
    "FINAL.DAILY_SUMMARY",
    "FINAL.HOURLY_PATTERNS",
    "FINAL.ZONE_ANALYSIS",
]


def print_summary(session):
    for table in SUMMARY_TABLES:
        query = f"SELECT COUNT(*) FROM {DATABASE}.{table}"
        count = session.sql(query).collect()[0][0]
        print(f"{table:<25} {count:>12,} lignes")
