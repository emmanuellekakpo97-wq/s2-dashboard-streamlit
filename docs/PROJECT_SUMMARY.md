# Mini-projet S2 — Résumé du projet

## Objectif

Construire un tableau de bord analytique interactif avec Streamlit pour comparer les indicateurs de développement des pays africains sur la période 2000–2024.

## Indicateurs principaux

- Économie : PIB, PIB par habitant et inflation
- Démographie : population
- Santé : espérance de vie
- Éducation : taux d'alphabétisation
- Technologie : utilisateurs d'Internet
- Énergie : accès à l'électricité
- Emploi : taux de chômage
- Environnement : émissions de CO₂

## Source des données

Les données sont récupérées depuis l'API de la Banque mondiale. La collecte couvre les 54 pays africains identifiés par leurs codes ISO2. Le script produit `data/raw/african_development.csv`.

## Colonne cible du jeu de données

Le CSV doit être exploitable pour l'analyse interactive : `country`, `country_code`, `region`, `income_level`, `year`, puis une colonne par indicateur disponible.

## Livrables attendus

1. Script de collecte automatique des données
2. Jeu de données nettoyé avec au moins 1 000 lignes et 8 colonnes
3. Notebook d'analyse exploratoire
4. Dashboard Streamlit avec au moins 5 visualisations
5. README complet et documentation des conclusions
6. Démonstration publique déployée sur Streamlit Community Cloud

## Structure du dashboard

- Barre latérale : pays, région, année et indicateur
- Vue d'ensemble : indicateurs clés (`st.metric`)
- Analyse temporelle : graphique linéaire Plotly
- Comparaison géographique : carte ou bar chart
- Corrélations : heatmap ou scatter plot
- Distribution : histogramme ou box plot

## Contraintes de qualité

- Utiliser `pandas`, `plotly` et `streamlit`
- Expliquer les choix de nettoyage des valeurs manquantes
- Détecter les outliers avec IQR ou Z-score
- Normaliser les noms et les valeurs textuelles
- Créer des colonnes calculées utiles, par exemple le taux de croissance annuel
- Utiliser `st.cache_data` et viser un chargement inférieur à 5 secondes
- Citer la Banque mondiale comme source des données

## Étapes

| Étape | Travail | Statut |
|---|---|---|
| 1 | Initialisation du dépôt Git | Terminé |
| 2 | Collecte du dataset africain | En cours |
| 3 | Nettoyage avec Pandas | À faire |
| 4 | Analyse exploratoire | À faire |
| 5 | Visualisations | À faire |
| 6 | Dashboard Streamlit | À faire |
| 7 | Tests et optimisation | À faire |
| 8 | Déploiement public | À faire |
| 9 | Documentation et présentation | À faire |

## Convention GitLab

La branche personnelle doit suivre le format `prenom-nom`, sans accents ni majuscules. Les fonctionnalités passent par des sous-branches `prenom-nom/feature/nom-feature`, puis par une Merge Request vers la branche personnelle. Aucun développement direct ne doit être poussé vers `develop` ou `main`.


- Traitement des valeurs manquantes : supprimer, imputer par médiane ou mode (justifier le choix)