# 🚕 NYC Taxi Data Pipeline

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Snowflake](https://img.shields.io/badge/Snowflake-Data%20Warehouse-29B5E8?logo=snowflake)
![dbt](https://img.shields.io/badge/dbt-Transformations-FF694B?logo=dbt)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)
![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?logo=git)

## 📌 Présentation

**NYC Taxi Data Pipeline** est un projet de Data Engineering basé sur les données de trajets de taxis de New York.

L'objectif du projet est de construire une chaîne de traitement complète permettant de :

- charger et exploiter des données dans **Snowflake** ;
- transformer les données avec **dbt** ;
- contrôler leur qualité grâce aux tests dbt ;
- construire des modèles de données destinés à l'analyse ;
- présenter les résultats dans une application **Streamlit** ;
- versionner le code avec **Git / GitHub**.

Le projet met donc en pratique une architecture moderne de traitement de données allant de la donnée source jusqu'à sa visualisation.

---

## 🎯 Objectifs

Les principaux objectifs du projet sont :

1. Centraliser les données dans Snowflake.
2. Organiser les données selon différentes étapes de transformation.
3. Nettoyer et standardiser les données avec dbt.
4. Mettre en place des contrôles de qualité.
5. Construire des modèles analytiques réutilisables.
6. Exploiter les modèles finaux dans un dashboard Streamlit.
7. Structurer le projet selon de bonnes pratiques Data Engineering.
8. Versionner l'ensemble du code avec Git.

---

## 🏗️ Architecture du projet

```text
                         ┌─────────────────────┐
                         │    NYC Taxi Data    │
                         │       Sources       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Snowflake      │
                         │    Data Warehouse   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │        dbt          │
                         │      Staging        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Data Transformation│
                         │   & Data Quality    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Final Models     │
                         │    Data Analytics   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Streamlit      │
                         │      Dashboard      │
                         └─────────────────────┘
```

---

## 🧰 Technologies utilisées

| Technologie | Rôle |
|---|---|
| **Snowflake** | Stockage et traitement des données |
| **dbt** | Transformation SQL, modélisation et tests |
| **Python** | Développement et logique applicative |
| **Streamlit** | Création du dashboard interactif |
| **SQL** | Requêtes et transformations de données |
| **Git** | Gestion des versions |
| **GitHub** | Hébergement du code source |

---

## 📂 Structure du projet

```text
pipeline_nyc_taxi/
│
├── nyc_taxi_dbt/
│   │
│   ├── logs/
│   │   └── dbt.log
│   │
│   ├── macros/
│   │
│   ├── models/
│   │   ├── final/
│   │   ├── quality/
│   │   └── staging/
│   │       ├── schema.yml
│   │       └── stg_yellow_taxi.sql
│   │
│   ├── setup/
│   │
│   ├── target/
│   │
│   ├── tests/
│   │
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── sources.yml
│
├── src/
│
├── vis/
│   ├── .streamlit/
│   ├── pyproject.toml
│   ├── snowflake.yml
│   └── streamlit_app.py
│
├── main.py
│
└── README.md
```

> Certains dossiers générés automatiquement par dbt, comme `target/` et `logs/`, ne sont normalement pas nécessaires dans le dépôt Git final.

---

# 🔄 Pipeline de données

## 1. Source

Le projet travaille avec des données de trajets de taxis de New York, notamment les données **Yellow Taxi**.

Selon la source utilisée, les données peuvent contenir des informations telles que :

- date et heure de prise en charge ;
- date et heure de dépose ;
- identifiant du véhicule ;
- nombre de passagers ;
- distance du trajet ;
- zone de départ ;
- zone d'arrivée ;
- type de paiement ;
- tarif ;
- pourboire ;
- péages ;
- montant total.

---

## 2. Ingestion

Les données sont mises à disposition dans Snowflake afin de pouvoir être exploitées par les modèles dbt.

Cette étape constitue le point d'entrée du pipeline.

```text
Source
   ↓
Snowflake
```

---

## 3. Staging avec dbt

La couche **staging** permet de préparer les données brutes avant les transformations analytiques.

Le modèle :

```text
models/staging/stg_yellow_taxi.sql
```

sert notamment à :

- sélectionner les colonnes utiles ;
- renommer certaines colonnes ;
- convertir les types de données ;
- normaliser les valeurs ;
- préparer les données pour les modèles suivants.

Le principe est de conserver une couche de préparation claire et réutilisable.

---

## 4. Data Quality

La qualité des données est contrôlée avec **dbt**.

Les tests peuvent permettre de vérifier :

- les valeurs `NULL` ;
- l'unicité des identifiants ;
- les valeurs autorisées ;
- les relations entre différentes tables ;
- la cohérence générale des données.

Les fichiers de configuration des tests se trouvent notamment dans les fichiers `schema.yml`.

Exemple de logique de test :

```text
Données sources
      ↓
Staging
      ↓
Tests de qualité
      ↓
Modèles analytiques
```

---

## 5. Modèles finaux

Les modèles de la couche `final/` sont destinés à fournir des données directement exploitables pour l'analyse.

Cette couche peut servir à construire des indicateurs tels que :

- nombre de trajets ;
- chiffre d'affaires ;
- revenu moyen par trajet ;
- distance moyenne ;
- montant moyen des pourboires ;
- évolution de l'activité ;
- répartition des moyens de paiement ;
- analyse géographique.

---

# 📊 Dashboard Streamlit

L'application Streamlit se trouve dans :

```text
vis/streamlit_app.py
```

Elle permet de transformer les données préparées dans Snowflake en une interface interactive.

Le dashboard peut notamment présenter :

### 🚕 Activité

- nombre total de trajets ;
- évolution du nombre de trajets ;
- activité par période.

### 💰 Revenus

- revenus totaux ;
- revenu moyen par trajet ;
- montant moyen payé ;
- évolution des revenus.

### 📏 Trajets

- distance moyenne ;
- distribution des distances ;
- relation entre distance et prix.

### 💳 Paiements

- répartition des moyens de paiement ;
- montant moyen selon le type de paiement.

### 📍 Géographie

- zones de départ ;
- zones d'arrivée ;
- concentration des trajets.

---

# 🗃️ Modélisation des données

Le projet suit une organisation en différentes couches.

```text
                    SOURCE
                      │
                      ▼
                  STAGING
                      │
                      ▼
             DATA QUALITY
                      │
                      ▼
                   FINAL
                      │
                      ▼
                STREAMLIT
```

Cette séparation permet de distinguer :

- les données sources ;
- la préparation des données ;
- les contrôles qualité ;
- les données destinées à l'analyse ;
- la couche de présentation.

---

# 🔧 Installation

## Prérequis

Pour exécuter le projet localement, il est recommandé d'avoir :

- Python 3.x ;
- Git ;
- un compte Snowflake ;
- dbt ;
- Streamlit.

Vérifier Python :

```bash
python --version
```

Vérifier Git :

```bash
git --version
```

Vérifier dbt :

```bash
dbt --version
```

---

# 📥 Installation du projet

Cloner le dépôt :

```bash
git clone https://github.com/<USERNAME>/pipeline-nyc-taxi.git
```

Entrer dans le projet :

```bash
cd pipeline-nyc-taxi
```

---

# 🐍 Environnement Python

Il est recommandé d'utiliser un environnement virtuel.

Créer l'environnement :

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Si le projet utilise `pyproject.toml`, les dépendances peuvent également être installées avec :

```bash
pip install .
```

---

# ❄️ Configuration Snowflake

Le projet utilise Snowflake comme environnement de stockage et de traitement.

Les paramètres nécessaires dépendent de l'environnement Snowflake utilisé.

Exemple de paramètres :

```text
Account
User
Password / Authentication
Database
Schema
Warehouse
Role
```

## ⚠️ Sécurité

**Ne jamais placer de mot de passe, token, clé privée ou autre secret directement dans le dépôt GitHub.**

Les informations sensibles doivent être stockées dans :

- des variables d'environnement ;
- un gestionnaire de secrets ;
- les mécanismes de secrets de Snowflake / Streamlit lorsque cela est approprié.

---

# 🔧 Configuration dbt

Le projet dbt se trouve dans :

```text
nyc_taxi_dbt/
```

Se placer dans ce dossier :

```bash
cd nyc_taxi_dbt
```

Vérifier la configuration :

```bash
dbt debug
```

Installer les packages dbt éventuels :

```bash
dbt deps
```

---

# ▶️ Exécuter dbt

## Construire les modèles

```bash
dbt run
```

## Exécuter les tests

```bash
dbt test
```

## Exécuter modèles + tests

```bash
dbt build
```

## Générer la documentation

```bash
dbt docs generate
```

Puis :

```bash
dbt docs serve
```

---

# 🧪 Tests de qualité

Les tests dbt permettent de détecter les problèmes de qualité avant que les données soient utilisées par les modèles finaux ou le dashboard.

Exemples de contrôles :

```yaml
tests:
  - not_null
  - unique
```

Des tests supplémentaires peuvent être ajoutés pour contrôler :

- les valeurs acceptées ;
- les relations ;
- les règles métier ;
- les contraintes spécifiques aux données taxi.

---

# 📈 Lancer Streamlit

Se placer dans le dossier de l'application :

```bash
cd vis
```

Lancer Streamlit :

```bash
streamlit run streamlit_app.py
```

Streamlit démarre alors une application web permettant d'explorer les données.

---

# 🔁 Workflow recommandé

Le workflow de développement peut être résumé ainsi :

```text
1. Charger les données
        ↓
2. Vérifier Snowflake
        ↓
3. Transformer avec dbt
        ↓
4. Exécuter les tests
        ↓
5. Vérifier les modèles finaux
        ↓
6. Alimenter Streamlit
        ↓
7. Tester le dashboard
        ↓
8. Commit Git
        ↓
9. Push GitHub
```

---

# 🌿 Git & GitHub

Initialiser le dépôt :

```bash
git init
```

Ajouter les fichiers :

```bash
git add .
```

Créer un commit :

```bash
git commit -m "Initial commit"
```

Associer le dépôt GitHub :

```bash
git remote add origin https://github.com/<USERNAME>/pipeline-nyc-taxi.git
```

Utiliser la branche `main` :

```bash
git branch -M main
```

Envoyer le projet :

```bash
git push -u origin main
```

Pour les modifications suivantes :

```bash
git add .
git commit -m "Update pipeline"
git push
```

---

# 🚫 Fichiers à ne pas versionner

Créer un fichier `.gitignore` à la racine du projet.

Exemple :

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
venv/
env/

# Environment variables
.env
.env.*

# Streamlit secrets
.streamlit/secrets.toml
vis/.streamlit/secrets.toml

# dbt generated files
target/
logs/
dbt_packages/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Jupyter
.ipynb_checkpoints/
```

Avant chaque `git push`, vérifier :

```bash
git status
```

et s'assurer qu'aucun secret n'est présent.

---

# 📁 Organisation recommandée du dépôt

Une fois le projet nettoyé, la structure recommandée peut être :

```text
pipeline_nyc_taxi/
│
├── nyc_taxi_dbt/
│   ├── models/
│   │   ├── staging/
│   │   ├── quality/
│   │   └── final/
│   ├── macros/
│   ├── tests/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── sources.yml
│
├── src/
│
├── vis/
│   ├── .streamlit/
│   ├── pyproject.toml
│   ├── snowflake.yml
│   └── streamlit_app.py
│
├── main.py
├── .gitignore
└── README.md
```

---

# 📌 Bonnes pratiques

## SQL

Les transformations SQL doivent rester lisibles et organisées.

Il est recommandé de :

- utiliser des noms de modèles explicites ;
- éviter les transformations trop complexes dans un seul modèle ;
- séparer staging et final ;
- documenter les modèles importants.

## dbt

Il est recommandé de :

- utiliser les tests ;
- documenter les modèles ;
- utiliser des sources ;
- garder les modèles modulaires ;
- éviter de versionner les fichiers générés automatiquement.

## Python

Le code Python doit être organisé en fonctions ou modules lorsque cela améliore la lisibilité.

## Git

Utiliser des commits explicites :

```text
feat: add taxi staging model
fix: correct trip amount calculation
test: add data quality tests
docs: update README
refactor: clean pipeline structure
```

---

# 🔐 Sécurité

Avant de publier le projet sur GitHub, vérifier qu'il ne contient pas :

- mot de passe Snowflake ;
- clé API ;
- token ;
- clé privée ;
- identifiants personnels ;
- fichier `.env` ;
- secrets Streamlit ;
- credentials dbt.

En cas de secret publié accidentellement, il faut considérer le secret comme compromis et le révoquer/remplacer.

---

# 🚀 Améliorations futures

Plusieurs évolutions peuvent être ajoutées au projet :

- [ ] Automatiser l'ingestion des données.
- [ ] Ajouter davantage de modèles dbt.
- [ ] Ajouter des tests de qualité supplémentaires.
- [ ] Améliorer la documentation dbt.
- [ ] Ajouter une orchestration automatique.
- [ ] Ajouter une CI/CD avec GitHub Actions.
- [ ] Automatiser les déploiements.
- [ ] Ajouter davantage de visualisations Streamlit.
- [ ] Ajouter des filtres temporels au dashboard.
- [ ] Ajouter une analyse géographique plus détaillée.
- [ ] Ajouter des indicateurs de performance.
- [ ] Optimiser les requêtes Snowflake.
- [ ] Ajouter des tests automatisés Python.

---

# 📊 Compétences démontrées

Ce projet permet de démontrer des compétences dans les domaines suivants :

### Data Engineering

- conception d'un pipeline de données ;
- ingestion ;
- transformation ;
- modélisation ;
- contrôle qualité.

### Cloud Data

- utilisation de Snowflake ;
- organisation des données ;
- exécution de transformations SQL.

### Analytics Engineering

- dbt ;
- modèles staging ;
- modèles finaux ;
- tests ;
- documentation.

### Python

- développement d'une application ;
- manipulation de données ;
- intégration avec les outils data.

### Data Visualization

- création d'un dashboard Streamlit ;
- exploration interactive ;
- présentation d'indicateurs.

### Software Engineering

- Git ;
- GitHub ;
- organisation du code ;
- documentation ;
- gestion des versions.

---

# 📚 Ressources

- [Snowflake](https://www.snowflake.com/)
- [Snowflake Documentation](https://docs.snowflake.com/)
- [dbt Documentation](https://docs.getdbt.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Documentation](https://docs.github.com/)

---

# 👤 Auteur

**Nom :** `<TON NOM>`

**GitHub :** `https://github.com/<USERNAME>`

**Projet :** NYC Taxi Data Pipeline

---

# 📄 Licence

Ce projet est destiné à un usage d'apprentissage, de démonstration et de portfolio.

Une licence open source peut être ajoutée au dépôt selon les besoins du projet.

---

## ⭐ Conclusion

**NYC Taxi Data Pipeline** constitue un projet complet permettant de mettre en œuvre une chaîne moderne de Data Engineering :

```text
        DATA
         │
         ▼
    ┌─────────┐
    │Snowflake│
    └────┬────┘
         │
         ▼
      ┌─────┐
      │ dbt │
      └──┬──┘
         │
    ┌────┴────┐
    │         │
 Quality    Models
    │         │
    └────┬────┘
         │
         ▼
   ┌───────────┐
   │ Streamlit │
   └─────┬─────┘
         │
         ▼
     ANALYSES
```

Le projet illustre ainsi le parcours complet d'une donnée, depuis son stockage jusqu'à son exploitation dans une application de visualisation.
