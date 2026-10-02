# Analyse réflexive — Projet NYC Yellow Taxi


## 1. Ce que nous avons fait

Nous avons construit un Data Warehouse Snowflake en trois couches (RAW, STAGING, FINAL) à partir de 12 mois de données NYC Taxi 2025, soit environ 48,7 millions de courses. Nous nous sommes réparti le travail : d'un côté le **nettoyage des données** et les contrôles qualité (mesurer les anomalies dans RAW, définir les règles de rejet, quantifier le taux de rejet et vérifier le résultat), de l'autre le projet dbt et le dashboard Streamlit. Chacun de nous a dû comprendre la partie de l'autre pour faire tourner l'ensemble sur les données complètes.

## 2. Difficultés rencontrées et solutions

**Choisir quoi faire des valeurs manquantes.** Le nombre de passagers est absent sur près de 30 % des lignes. Rejeter ces lignes aurait supprimé une part énorme du jeu de données ; imputer une valeur aurait fabriqué de l'information. Nous avons choisi de les garder en `NULL` : les agrégats les ignorent, et le choix est documenté dans le README.

**Distinguer une anomalie d'une erreur.** Les montants négatifs peuvent être des annulations ou des erreurs de saisie. Leur proportion diminuait au fil des mois et ils fausseraient les indicateurs de revenu, donc nous les avons rejetés, en gardant leur mesure dans le rapport qualité pour que la décision reste discutable.

**Un volume qui change les habitudes.** Passer de quelques mois à 12 mois (48,7 M de lignes) rend chaque requête et chaque `CREATE TABLE AS` beaucoup plus long. Nous avons dû vérifier à chaque étape que les tables étaient réellement construites, au lieu de supposer que le script avait fini.

**Des données hors périmètre.** En contrôlant le résultat, nous avons repéré 29 lignes datées hors de 2025. Elles passaient toutes les règles de nettoyage parce qu'aucun filtre sur la période n'était prévu. La solution est un filtre de dates explicite dans STAGING (SQL et dbt).La leçon : un contrôle « tout est à zéro » ne vaut que pour les règles que nous avons pensé à écrire.

**Faire tourner l'infrastructure.** Deux blocages ne venaient pas de notre code : l'application Streamlit refusait de démarrer faute de compute pool disponible, et la commande `EXECUTE DBT PROJECT` échouait parce que le projet dbt n'était pas déployé dans Snowflake sous le nom attendu. Nous avons appris à lire ces erreurs (`SHOW COMPUTE POOLS`, `SHOW DBT PROJECTS`) pour savoir si le problème venait du code, des droits ou de l'environnement.

## 3. Choix techniques et justifications

- **RAW intact, nettoyage dans STAGING.** Garder la donnée d'origine permet de rejouer toutes les transformations et de mesurer précisément ce qui a été rejeté. C'est aussi ce qui rend le taux de 3,12 % défendable.
- **Filtrer plutôt que corriger.** Pour les horodatages incohérents, les distances nulles ou aberrantes et les montants négatifs, nous n'avions aucune base fiable pour « réparer » la valeur. Rejeter et quantifier est plus honnête que corriger au hasard.
- **Pas d'imputation des passagers.** Une valeur inventée fausserait les totaux de passagers ; un `NULL` est neutre.
- **Un pipeline SQL puis dbt.** Le pipeline SQL pur nous a permis de comprendre chaque étape. dbt apporte ensuite le versionnement, les dépendances explicites avec `ref()` et les tests `not_null` / `unique`.
- **Un code volontairement simple**, avec un module par responsabilité (chargement, exécution SQL, résumé), pour que chaque membre du groupe puisse le relire et le modifier.

## 4. Compétences acquises

- Concevoir une architecture en couches sur Snowflake (base, schémas, stage, file format, `COPY INTO`).
- Profiler un jeu de données réel et transformer des constats en règles de qualité mesurables.
- Écrire des transformations SQL reproductibles (CTE, enrichissements, catégorisations) et les porter vers dbt.
- Lire et diagnostiquer des erreurs d'infrastructure cloud (droits, compute pool, objets non déployés).
- Travailler en groupe sur un même pipeline, avec des périmètres séparés.

## 5. Compétences à approfondir

- **Déploiement et industrialisation dbt** : déployer un projet dans Snowflake, gérer les profils, ajouter une couche `intermediate` et des tests de plages de valeurs.
- **Orchestration** : automatiser l'exécution mensuelle avec GitHub Actions et des secrets sécurisés (non réalisé dans ce projet).
- **Gestion des droits** : remplacer les `GRANT` accordés à `PUBLIC` par des rôles dédiés avec le principe du moindre privilège.
- **Performance et coûts Snowflake** : dimensionner le warehouse et estimer le coût d'un rechargement complet.
- **Qualité des données en continu** : passer d'un contrôle ponctuel à une surveillance automatique avec alertes.

## 6. Parallèle avec un contexte professionnel réel

Dans une entreprise, ce pipeline correspondrait à une chaîne d'alimentation d'un entrepôt de données pour le pilotage. Trois points se transposent directement :

- **La traçabilité.** Conserver la donnée brute et documenter chaque règle de rejet, c'est ce qu'attendrait un auditeur : on doit pouvoir expliquer pourquoi une ligne n'apparaît pas dans un indicateur.
- **La qualité comme sujet de gouvernance.** Un taux de rejet, des contrôles chiffrés et des tests automatisés sont des preuves de maîtrise. Ils relèvent autant de la gouvernance des données que de l'ingénierie.
- **La sécurité et les accès.** Les droits que nous avons utilisés (rôle `ACCOUNTADMIN`, `GRANT` à `PUBLIC`) seraient inacceptables en production : en environnement réglementé, chaque couche aurait ses rôles, et seuls les schémas d'analyse seraient exposés aux utilisateurs métier.

Ce projet nous a surtout montré que la valeur d'un Data Engineer tient autant à la fiabilité et à l'explicabilité des données qu'à la performance des requêtes.
