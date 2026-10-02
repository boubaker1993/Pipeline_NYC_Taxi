# NYC Yellow Taxi — Data Warehouse Snowflake (RAW → STAGING → FINAL)

Dans ce projet, Nous construisons le Data Warehouse analytique d'une société de transport à partir des données ouvertes de la NYC Taxi & Limousine Commission (taxis jaunes, format Parquet). J'ingère les données brutes, Nous les nettoyons, Nous les enrichissons, puis Nous produisons des tables d'analyse qui s'affiche dans un dashboard.

Projet réalisé en groupe (Boubaker et Asmaà). 

## Sommaire

- [NYC Yellow Taxi — Data Warehouse Snowflake (RAW → STAGING → FINAL)](#nyc-yellow-taxi--data-warehouse-snowflake-raw--staging--final)
  - [Sommaire](#sommaire)
  - [Périmètre](#périmètre)
  - [Architecture](#architecture)
  - [Structure du dépôt](#structure-du-dépôt)
  - [Prérequis](#prérequis)
  - [Exécution pas à pas](#exécution-pas-à-pas)
    - [Partie 1 — Pipeline SQL](#partie-1--pipeline-sql)
    - [Partie 2 — dbt](#partie-2--dbt)
    - [Dashboard](#dashboard)
  - [Nettoyage et qualité des données](#nettoyage-et-qualité-des-données)
    - [Règles appliquées en STAGING](#règles-appliquées-en-staging)
    - [Taux de rejet](#taux-de-rejet)
  - [Enrichissements](#enrichissements)
  - [Tables d'analyse (FINAL)](#tables-danalyse-final)
  - [dbt](#dbt)
  - [Dashboard Streamlit](#dashboard-streamlit)
  - [Choix techniques](#choix-techniques)
  - [Limites et pistes d'amélioration](#limites-et-pistes-damélioration)
  - [Analyse réflexive](#analyse-réflexive)

## Périmètre

- Source : fichiers Parquet mensuels des taxis jaunes NYC.
- Période analysée : **12 mois de 2025** (environ **48,7 millions** de courses).
- Technologies : Snowflake, SQL, Python (Snowpark), dbt, Streamlit.

## Architecture

```
Fichiers Parquet ──► Stage TLC_RAW_STAGE ──► RAW ──► STAGING ──► FINAL ──► Dashboard
                                              │          │           │
                                          brut, sans   nettoyé,    3 tables
                                         modification  enrichi    d'analyse
```

Base : `NYC_TAXI_DB_PARTIE_1`

| Schéma | Rôle | objet principal |
|---|---|---|
| `RAW` | Données brutes, importées sans aucune modification | `YELLOW_TAXI_RAW` |
| `STAGING` | Données nettoyées, filtrées et enrichies | `YELLOW_TAXI` |
| `FINAL` | Tables d'analyse métier | `DAILY_SUMMARY`, `HOURLY_PATTERNS`, `ZONE_ANALYSIS` (+ `DATA_QUALITY_REPORT`) |

Nous gardons RAW intact pour pouvoir rejouer toutes les transformations à partir de la donnée d'origine.

## Structure du dépôt


```
.
├── main.py                       # Orchestration du pipeline (partie 1, SQL pur)
├── src/
│   ├── loader.py                 # Vérification du stage + COPY INTO RAW
│   ├── sql_runner.py             # Exécution des fichiers .sql
│   ├── summary.py                # Comptage des lignes par table
│   └── sql/
│       ├── 01_infrastructure.sql # Base, schémas, warehouse
│       ├── 02_raw.sql            # File format, stage, table RAW
│       ├── 03_quality.sql        # Contrôles qualité sur RAW
│       ├── 04_staging.sql        # Nettoyage + enrichissement
│       ├── 05_final_daily_summary.sql
│       ├── 06_final_hourly_patterns.sql
│       └── 07_final_zone_analysis.sql
├── dbt/                          # Projet dbt (partie avancée)
│   ├── models/
│   │   ├── staging/stg_yellow_taxi.sql
│   │   ├── marts/                # daily_summary, hourly_patterns, zone_analysis
│   │   ├── quality/data_quality_report.sql
│   │   └── schema.yml            # Tests dbt
│   ├── 04_grants.sql             # Droits sur la base
│   └── 05_execute_dbt.sql        # Lancement de dbt dans Snowflake
└── streamlit_app.py              # Dashboard
```

## Prérequis

- Un compte Snowflake avec le rôle `ACCOUNTADMIN` (création de la base et du warehouse).
- Un notebook ou une feuille Python Snowflake (le script utilise `get_active_session()`).
- Le fichier Parquet des courses à charger.

## Exécution pas à pas

### Partie 1 — Pipeline SQL

1. Nous chargeons le dépôt dans l'environnement Snowflake.
2. Nous lançons `main.py` une première fois : il crée l'infrastructure (`01`), puis les objets RAW (`02`) et s'arrête si le stage est vide.
3. Nous dépose le fichier `.parquet` dans `NYC_TAXI_DB_PARTIE_1 > RAW > Stages > TLC_RAW_STAGE`.
4. Nous relançons `main.py` : il exécute dans l'ordre
   - le chargement `COPY INTO` vers RAW (`ON_ERROR = 'ABORT_STATEMENT'`),
   - les contrôles qualité (`03`),
   - le nettoyage et l'enrichissement vers STAGING (`04`),
   - les trois tables FINAL (`05`, `06`, `07`),
   - un récapitulatif du nombre de lignes par table.

### Partie 2 — dbt

1. J'exécute `04_grants.sql` pour donner les droits nécessaires.
2. Nous lançons le projet dbt avec `05_execute_dbt.sql` (`EXECUTE DBT PROJECT ... ARGS = 'build'`), qui construit les modèles et joue les tests.

### Dashboard

1. Nous configurons la connexion `snowflake` de Streamlit.
2. Nous lançons `streamlit run streamlit_app.py` (ou Nous déployons l'application dans Snowflake).

## Nettoyage et qualité des données

Le dataset présente des anomalies réelles. Nous les mesurons d'abord dans RAW (`03_quality.sql` / `DATA_QUALITY_REPORT`) : valeurs manquantes par colonne, montants négatifs, distances à zéro, distances extrêmes.

### Règles appliquées en STAGING

| Règle | Traitement |
|---|---|
| Horodatage de prise en charge ou de dépose manquant | Ligne rejetée |
| Dépose non strictement postérieure à la prise en charge | Ligne rejetée |
| Distance ≤ 0 | Ligne rejetée |
| Distance > 1 000 miles | Ligne rejetée (valeur aberrante) |
| Montant total négatif | Ligne rejetée |
| Nombre de passagers manquant | Ligne conservée, valeur laissée à `NULL` (pas d'imputation) |

Nous n'imputons pas le nombre de passagers : il est très souvent manquant, et inventer une valeur fausserait `total_passengers`. Les `NULL` sont simplement ignorés par les agrégats.

### Taux de rejet

Sur les 12 mois de 2025 : environ **48,7 M** de lignes en entrée, **1 522 287** lignes rejetées, soit **3,12 %**. Après nettoyage, tous nos contrôles finaux retournent zéro.

Nous notons aussi **29 lignes datées hors de 2025** dans les fichiers sources.

## Enrichissements

Calculés dans STAGING :

- `trip_duration_seconds` / `trip_duration_minutes` : durée de la course ;
- `trip_date`, `pickup_hour` : date et heure de prise en charge ;
- `avg_speed_mph` : vitesse moyenne (`NULL` si durée ou distance nulle) ;
- `distance_category` : `SHORT` (< 1), `MEDIUM` (< 5), `LONG` (< 15), `VERY_LONG` (≥ 15 miles) ;
- `duration_category` : `SHORT` (< 10 min), `MEDIUM` (< 30), `LONG` (< 60), `VERY_LONG` (≥ 60) ;
- `time_period` : `MORNING_RUSH` (6h–9h), `DAYTIME` (10h–15h), `EVENING_RUSH` (16h–19h), `NIGHT`.

## Tables d'analyse (FINAL)

| Table | Grain | Indicateurs |
|---|---|---|
| `DAILY_SUMMARY` | 1 ligne par jour | courses, passagers, distance / durée / vitesse moyennes, montant moyen, revenu total |
| `HOURLY_PATTERNS` | 1 ligne par heure de prise en charge | mêmes indicateurs + période de la journée |
| `ZONE_ANALYSIS` | 1 ligne par zone de départ | courses, zones d'arrivée distinctes, distance, durée, vitesse, montant, revenu, pourboire moyen |

## dbt

Les transformations SQL sont reprises dans un projet dbt pour les versionner et les tester :

- `stg_yellow_taxi` : même logique de nettoyage et d'enrichissement que `04_staging.sql`, lue depuis la source `raw.yellow_taxi_raw` ;
- `daily_summary`, `hourly_patterns`, `zone_analysis` : construits à partir de `ref('stg_yellow_taxi')` ;
- `data_quality_report` : une ligne de contrôles sur RAW, lue par le dashboard ;
- tests (`schema.yml`) : `not_null` et `unique` sur la clé de chaque table FINAL (`trip_date`, `pickup_hour`, `pickup_location_id`).

## Dashboard Streamlit

Le dashboard lit les tables du schéma `FINAL` et affiche des KPIs globaux (courses, passagers, revenu total, montant moyen) puis quatre onglets :

- **Par jour** : courses et revenu quotidiens ;
- **Par heure** : courses et vitesse moyenne par heure, répartition par période ;
- **Par zone** : classement des zones de départ selon la métrique choisie (top N réglable) ;
- **Qualité des données** : contrôles sur la table RAW.

Les lectures sont mises en cache 10 minutes.

## Choix techniques

- **Architecture en 3 couches** : séparer le brut, le nettoyé et l'analytique rend chaque étape rejouable et auditable.
- **Nettoyage par filtrage dans STAGING, jamais dans RAW** : la donnée d'origine reste intacte et le taux de rejet est mesurable.
- **Chargement par `COPY INTO` avec `MATCH_BY_COLUMN_NAME`** : le chargement ne dépend pas de l'ordre des colonnes du Parquet.
- **Tables FINAL recalculées en `CREATE OR REPLACE`** : plus simple et idempotent à cette échelle.
- **dbt** : transformations versionnées, dépendances explicites via `ref()`, tests automatiques.
- **Code volontairement simple** : un module par responsabilité, peu d'abstractions.

## Limites et pistes d'amélioration

- Filtrer explicitement les courses à la période étudiée (les 29 lignes hors 2025 passent aujourd'hui les règles de nettoyage).
- Ajouter une couche `intermediate` dbt et des tests de plages de valeurs (distance, montant, durée).
- Automatiser l'exécution mensuelle (GitHub Actions) avec des secrets sécurisés.
- Restreindre les droits : les grants actuels sont accordés au rôle `PUBLIC`, un rôle dédié serait plus propre en production.
- Ajouter des indicateurs : taux de pourboire, type de jour (semaine / week-end).

## Analyse réflexive

Notre analyse réflexive (difficultés et solutions, choix techniques, compétences acquises et à approfondir, parallèle professionnel) est dans [ANALYSE_REFLEXIVE.md](ANALYSE_REFLEXIVE.md).
