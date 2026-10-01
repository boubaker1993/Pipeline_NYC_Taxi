import os

import streamlit as st

DATABASE = "NYC_TAXI_DB_PARTIE_1"
SCHEMA = "FINAL"

st.set_page_config(page_title="NYC Taxi", layout="wide")

conn = st.connection("snowflake", ttl=os.getenv("SNOWFLAKE_CONNECTION_TTL"))
session = conn.session()


@st.cache_data(ttl=600)
def load_table(table_name):
    query = f"SELECT * FROM {DATABASE}.{SCHEMA}.{table_name}"
    return session.sql(query).to_pandas()


st.title("NYC Yellow Taxi :taxi:")
st.caption("Tables produites par le projet dbt (schéma FINAL)")

try:
    daily = load_table("DAILY_SUMMARY")
    hourly = load_table("HOURLY_PATTERNS")
    zones = load_table("ZONE_ANALYSIS")
except Exception as error:
    st.error("Impossible de lire les tables FINAL. Lance d'abord dbt build.")
    st.exception(error)
    st.stop()

try:
    quality = load_table("DATA_QUALITY_REPORT")
except Exception:
    quality = None

if daily.empty:
    st.warning("DAILY_SUMMARY est vide.")
    st.stop()

total_trips = int(daily["TOTAL_TRIPS"].sum())
total_revenue = float(daily["TOTAL_REVENUE"].sum())
total_passengers = int(daily["TOTAL_PASSENGERS"].sum())
avg_trip_amount = total_revenue / total_trips if total_trips else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Courses", f"{total_trips:,}")
col2.metric("Passagers", f"{total_passengers:,}")
col3.metric("Revenu total", f"{total_revenue:,.0f} $")
col4.metric("Montant moyen", f"{avg_trip_amount:,.2f} $")

tab_daily, tab_hourly, tab_zones, tab_quality = st.tabs(
    ["Par jour", "Par heure", "Par zone", "Qualité des données"]
)

with tab_daily:
    daily_sorted = daily.sort_values("TRIP_DATE")

    st.subheader("Courses par jour")
    st.line_chart(data=daily_sorted, x="TRIP_DATE", y="TOTAL_TRIPS")

    st.subheader("Revenu par jour")
    st.bar_chart(data=daily_sorted, x="TRIP_DATE", y="TOTAL_REVENUE")

    st.subheader("Données")
    st.dataframe(daily_sorted, use_container_width=True)

with tab_hourly:
    hourly_sorted = hourly.sort_values("PICKUP_HOUR")

    st.subheader("Courses par heure de prise en charge")
    st.bar_chart(data=hourly_sorted, x="PICKUP_HOUR", y="TOTAL_TRIPS")

    st.subheader("Vitesse moyenne par heure (mph)")
    st.line_chart(data=hourly_sorted, x="PICKUP_HOUR", y="AVG_SPEED_MPH")

    st.subheader("Répartition par période")
    by_period = hourly_sorted.groupby("TIME_PERIOD", as_index=False)["TOTAL_TRIPS"].sum()
    st.bar_chart(data=by_period, x="TIME_PERIOD", y="TOTAL_TRIPS")

    st.subheader("Données")
    st.dataframe(hourly_sorted, use_container_width=True)

with tab_zones:
    metric_labels = {
        "Nombre de courses": "TOTAL_TRIPS",
        "Revenu total": "TOTAL_REVENUE",
        "Pourboire moyen": "AVG_TIP_AMOUNT",
        "Distance moyenne": "AVG_DISTANCE_MILES",
    }

    left, right = st.columns(2)
    metric_label = left.selectbox("Classer par", list(metric_labels.keys()))
    top_n = right.slider("Nombre de zones", min_value=5, max_value=50, value=15)

    metric_column = metric_labels[metric_label]
    top_zones = zones.sort_values(metric_column, ascending=False).head(top_n).copy()
    top_zones["PICKUP_LOCATION_ID"] = top_zones["PICKUP_LOCATION_ID"].astype(str)

    st.subheader(f"Top {top_n} zones de départ : {metric_label.lower()}")
    st.bar_chart(data=top_zones, x="PICKUP_LOCATION_ID", y=metric_column)

    st.subheader("Données")
    st.dataframe(top_zones, use_container_width=True)

with tab_quality:
    st.subheader("Contrôles sur la table RAW")

    if quality is None:
        st.info(
            "La table DATA_QUALITY_REPORT n'existe pas encore. "
            "Ajoute models/quality/data_quality_report.sql au projet dbt puis relance dbt build."
        )
    elif quality.empty:
        st.warning("DATA_QUALITY_REPORT est vide.")
    else:
        report = quality.iloc[0]
        total_rows = int(report["TOTAL_ROWS"])

        q1, q2, q3 = st.columns(3)
        q1.metric("Lignes RAW", f"{total_rows:,}")
        q2.metric("Montants négatifs", f"{report['NEGATIVE_AMOUNT_PCT']} %")
        q3.metric("Distances à zéro", f"{report['ZERO_DISTANCE_PCT']} %")

        st.dataframe(
            quality.T.rename(columns={0: "valeur"}),
            use_container_width=True,
        )