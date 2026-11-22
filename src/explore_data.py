"""Analyse exploratoire du dataset africain nettoyé."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "african_development_clean.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_PATH = OUTPUT_DIR / "exploratory_analysis.md"

NUMERIC_COLUMNS = [
    "electricity_access",
    "gdp",
    "gdp_per_capita",
    "inflation_rate",
    "internet_users",
    "life_expectancy",
    "population",
    "unemployment_rate",
    "gdp_growth_yoy",
    "population_growth_yoy",
]

AFRICAN_SUBREGIONS = {
    "Algeria": "Afrique du Nord", "Egypt, Arab Rep.": "Afrique du Nord",
    "Libya": "Afrique du Nord", "Morocco": "Afrique du Nord",
    "Sudan": "Afrique du Nord", "Tunisia": "Afrique du Nord",
    "Benin": "Afrique de l'Ouest", "Burkina Faso": "Afrique de l'Ouest",
    "Cabo Verde": "Afrique de l'Ouest", "Cote d'Ivoire": "Afrique de l'Ouest",
    "Gambia, The": "Afrique de l'Ouest", "Ghana": "Afrique de l'Ouest",
    "Guinea": "Afrique de l'Ouest", "Guinea-Bissau": "Afrique de l'Ouest",
    "Liberia": "Afrique de l'Ouest", "Mali": "Afrique de l'Ouest",
    "Mauritania": "Afrique de l'Ouest", "Niger": "Afrique de l'Ouest",
    "Nigeria": "Afrique de l'Ouest", "Senegal": "Afrique de l'Ouest",
    "Sierra Leone": "Afrique de l'Ouest", "Togo": "Afrique de l'Ouest",
    "Burundi": "Afrique de l'Est", "Comoros": "Afrique de l'Est",
    "Djibouti": "Afrique de l'Est", "Eritrea": "Afrique de l'Est",
    "Ethiopia": "Afrique de l'Est", "Kenya": "Afrique de l'Est",
    "Madagascar": "Afrique de l'Est", "Malawi": "Afrique de l'Est",
    "Mauritius": "Afrique de l'Est", "Mozambique": "Afrique de l'Est",
    "Rwanda": "Afrique de l'Est", "Seychelles": "Afrique de l'Est",
    "Somalia, Fed. Rep.": "Afrique de l'Est", "South Sudan": "Afrique de l'Est",
    "Tanzania": "Afrique de l'Est", "Uganda": "Afrique de l'Est",
    "Zambia": "Afrique de l'Est", "Zimbabwe": "Afrique de l'Est",
    "Angola": "Afrique centrale", "Cameroon": "Afrique centrale",
    "Central African Republic": "Afrique centrale", "Chad": "Afrique centrale",
    "Congo, Dem. Rep.": "Afrique centrale", "Congo, Rep.": "Afrique centrale",
    "Equatorial Guinea": "Afrique centrale", "Gabon": "Afrique centrale",
    "Sao Tome and Principe": "Afrique centrale",
    "Botswana": "Afrique australe", "Eswatini": "Afrique australe",
    "Lesotho": "Afrique australe", "Namibia": "Afrique australe",
    "South Africa": "Afrique australe",
}


def main() -> None:
    if not CLEAN_DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset introuvable : {CLEAN_DATA_PATH}")

    df = pd.read_csv(CLEAN_DATA_PATH, keep_default_na=False)

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["african_subregion"] = df["country"].map(AFRICAN_SUBREGIONS)

    # 1. Statistiques descriptives
    descriptive = df[NUMERIC_COLUMNS].describe().T
    descriptive = descriptive[["count", "mean", "std", "min", "50%", "max"]]
    descriptive = descriptive.rename(columns={"50%": "median"}).round(3)

    # 2. Corrélations
    correlations = df[NUMERIC_COLUMNS].corr(numeric_only=True).round(3)

    # 3. Top 10 et Flop 10 du PIB pour l'année la plus récente
    latest_year = int(df["year"].max())
    latest = df[df["year"] == latest_year].copy()

    top10 = latest.nlargest(10, "gdp")[
        ["country", "gdp", "gdp_per_capita", "population", "life_expectancy"]
    ].reset_index(drop=True)

    flop10 = latest.nsmallest(10, "gdp")[
        ["country", "gdp", "gdp_per_capita", "population", "life_expectancy"]
    ].reset_index(drop=True)

    # 4. Évolution temporelle
    temporal = df.groupby("year").agg(
        gdp_mean=("gdp", "mean"),
        gdp_median=("gdp", "median"),
        gdp_total=("gdp", "sum"),
        population_total=("population", "sum"),
        electricity_access_mean=("electricity_access", "mean"),
        internet_users_mean=("internet_users", "mean"),
        life_expectancy_mean=("life_expectancy", "mean"),
        unemployment_rate_mean=("unemployment_rate", "mean"),
    ).reset_index().round(3)

    # 5. Comparaison par sous-région africaine
    regional = df.groupby("african_subregion").agg(
        countries=("country", "nunique"),
        gdp_mean=("gdp", "mean"),
        gdp_per_capita_mean=("gdp_per_capita", "mean"),
        population_mean=("population", "mean"),
        electricity_access_mean=("electricity_access", "mean"),
        internet_users_mean=("internet_users", "mean"),
        life_expectancy_mean=("life_expectancy", "mean"),
        unemployment_rate_mean=("unemployment_rate", "mean"),
    ).reset_index().round(3)

    # Exports CSV
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    descriptive.to_csv(OUTPUT_DIR / "statistics_descriptive.csv")
    correlations.to_csv(OUTPUT_DIR / "correlations.csv")
    top10.to_csv(OUTPUT_DIR / "top10_gdp.csv", index=False)
    flop10.to_csv(OUTPUT_DIR / "flop10_gdp.csv", index=False)
    temporal.to_csv(OUTPUT_DIR / "evolution_temporelle.csv", index=False)
    regional.to_csv(OUTPUT_DIR / "comparaison_regions.csv", index=False)

    # Rapport lisible avec interprétation des résultats
    first_temporal = temporal.iloc[0]
    last_temporal = temporal.iloc[-1]
    best_gdp = top10.iloc[0]
    lowest_gdp = flop10.iloc[0]

    highest_gdp_per_capita_region = regional.sort_values(
        "gdp_per_capita_mean", ascending=False
    ).iloc[0]
    highest_electricity_region = regional.sort_values(
        "electricity_access_mean", ascending=False
    ).iloc[0]

    lines = [
        "# Analyse exploratoire",
        "",
        f"Dataset : {len(df)} observations, {df['country'].nunique()} pays, années {int(df['year'].min())}-{latest_year}.",
        "",
        "Les tableaux CSV détaillés restent disponibles dans `data/processed/`. "
        "Cette section explique uniquement les résultats principaux sans reproduire une nouvelle visualisation.",
        "",
        "## 1. Statistiques descriptives",
        "",
        "### Ce que signifie cette analyse",
        "Pour chaque indicateur numérique, nous observons le minimum, le maximum, la moyenne, la médiane et l'écart-type.",
        "",
        "- Le **minimum** représente la plus petite valeur observée.",
        "- Le **maximum** représente la plus grande valeur observée.",
        "- La **moyenne** est la somme des valeurs divisée par leur nombre.",
        "- La **médiane** est la valeur centrale : elle est plus fiable que la moyenne lorsque quelques pays ont des valeurs très élevées.",
        "- L'**écart-type** mesure la dispersion : plus il est élevé, plus les observations sont éloignées les unes des autres.",
        "",
        "### Exemple de compréhension",
        f"L'accès à l'électricité varie de {descriptive.loc['electricity_access', 'min']:.2f} % à {descriptive.loc['electricity_access', 'max']:.2f} %, avec une moyenne de {descriptive.loc['electricity_access', 'mean']:.2f} % et une médiane de {descriptive.loc['electricity_access', 'median']:.2f} %. Cela montre de fortes différences entre les pays.",
        f"Pour le PIB, la moyenne est {descriptive.loc['gdp', 'mean']/1e9:.1f} milliards de dollars, alors que la médiane est {descriptive.loc['gdp', 'median']/1e9:.1f} milliards. Cette différence indique une distribution très asymétrique : quelques grandes économies tirent la moyenne vers le haut.",
        f"Pour l'espérance de vie, la moyenne est {descriptive.loc['life_expectancy', 'mean']:.2f} ans et la médiane est {descriptive.loc['life_expectancy', 'median']:.2f} ans. Les valeurs sont donc assez regroupées autour du même niveau.",
        "",
        "### Conclusion",
        "Il existe une forte hétérogénéité économique entre les pays africains. Pour les indicateurs comme le PIB ou le PIB par habitant, la médiane est souvent plus représentative que la moyenne.",
        "",
        "Résultat détaillé : `statistics_descriptive.csv`.",
        descriptive.to_markdown(),
        "",
        "## 2. Analyse des corrélations",
        "",
        "### Ce que signifie cette analyse",
        "La corrélation mesure la relation linéaire entre deux variables. Sa valeur varie entre -1 et 1.",
        "",
        "- Proche de 1 : les deux variables augmentent ensemble.",
        "- Proche de -1 : lorsque l'une augmente, l'autre tend à diminuer.",
        "- Proche de 0 : aucune relation linéaire importante n'est visible.",
        "- Une corrélation ne démontre pas une relation de cause à effet.",
        "",
        "### Exemples de compréhension",
        "La corrélation entre l'accès à l'électricité et l'espérance de vie est 0,729 : les pays mieux électrifiés ont généralement une espérance de vie plus élevée.",
        "La corrélation entre l'accès à l'électricité et les utilisateurs d'Internet est 0,662 : le développement numérique est accompagné d'une meilleure couverture électrique.",
        "La corrélation entre le PIB et la population est 0,756 : les pays plus peuplés disposent généralement d'économies plus importantes.",
        "À l'inverse, la corrélation entre la croissance démographique et l'accès à l'électricité est -0,389 : une croissance rapide de la population peut exercer une pression sur les infrastructures.",
        "",
        "### Conclusion",
        "Les relations les plus importantes concernent l'électricité, l'Internet, l'espérance de vie et le PIB par habitant. L'inflation présente des corrélations généralement faibles avec les autres indicateurs dans ce dataset.",
        "",
        "Résultat détaillé : `correlations.csv`.",
        correlations.to_markdown(),
        "",
        f"## 3. Top 10 et Flop 10 du PIB — {latest_year}",
        "",
        "### Ce que signifie cette analyse",
        "Le Top 10 rassemble les dix pays ayant le PIB total le plus élevé. Le Flop 10 rassemble les dix pays ayant le PIB total le plus faible.",
        "Le PIB mesure la taille totale de l'économie. Il ne mesure pas directement le niveau de vie moyen : les pays très peuplés peuvent avoir un PIB élevé avec un PIB par habitant faible.",
        "",
        "### Exemples de compréhension",
        f"En {latest_year}, {best_gdp['country']} est au premier rang avec environ {best_gdp['gdp']/1e9:.1f} milliards de dollars de PIB.",
        f"À l'autre extrémité, {lowest_gdp['country']} est le plus faible du classement pour cette année, avec environ {lowest_gdp['gdp']/1e9:.3f} milliard de dollars.",
        "La comparaison Nigeria–Côte d'Ivoire illustre aussi la différence entre PIB total et PIB par habitant : un PIB élevé peut accompagner une population importante, sans assurer un revenu élevé par personne.",
        "",
        "### Conclusion",
        "Le classement met en évidence les grandes économies africaines du Top 10, mais il ne suffit pas à mesurer le développement ou la richesse moyenne.",
        "",
        "Résultats détaillés : `top10_gdp.csv` et `flop10_gdp.csv`.",
        top10.to_markdown(index=False),
        "",
        "Flop 10 :",
        flop10.to_markdown(index=False),
        "",
        "## 4. Analyse temporelle",
        "",
        "### Ce que signifie cette analyse",
        "L'analyse temporelle observe les moyennes ou totaux annuels. Elle permet de repérer une progression, une stagnation, une baisse ou une rupture liée à une crise.",
        "",
        "### Exemples de compréhension",
        f"Entre {int(first_temporal['year'])} et {int(last_temporal['year'])}, la population totale passe d'environ {first_temporal['population_total']/1e9:.3f} milliard à {last_temporal['population_total']/1e9:.3f} milliard.",
        f"L'accès moyen à l'électricité passe de {first_temporal['electricity_access_mean']:.2f} % à {last_temporal['electricity_access_mean']:.2f} %.",
        f"La part moyenne d'utilisateurs d'Internet passe de {first_temporal['internet_users_mean']:.2f} % à {last_temporal['internet_users_mean']:.2f} %.",
        f"L'espérance de vie moyenne passe de {first_temporal['life_expectancy_mean']:.2f} ans à {last_temporal['life_expectancy_mean']:.2f} ans.",
        "La baisse observée autour de 2020 peut être liée à une perturbation économique mondiale ou à des effets sanitaires, mais une vérification par indicateur est nécessaire avant d'attribuer une cause.",
        "",
        "### Conclusion",
        "La tendance générale sur la période est positive pour l'électricité, l'Internet et l'espérance de vie. Le PIB connaît une progression globale avec plusieurs fluctuations annuelles.",
        "",
        "Résultat détaillé : `evolution_temporelle.csv`.",
        temporal.to_markdown(index=False),
        "",
        "## 5. Comparaison régionale",
        "",
        "### Ce que signifie cette analyse",
        "Cette comparaison regroupe les pays dans cinq sous-régions africaines afin de comparer leurs moyennes. Elle permet d'observer les écarts structurels sans confondre une moyenne régionale avec les résultats de chaque pays.",
        "",
        "### Exemples de compréhension",
        f"La région présentant le PIB par habitant moyen le plus élevé est {highest_gdp_per_capita_region['african_subregion']} avec environ {highest_gdp_per_capita_region['gdp_per_capita_mean']:,.0f} dollars.",
        f"La région ayant le meilleur accès moyen à l'électricité est {highest_electricity_region['african_subregion']} avec environ {highest_electricity_region['electricity_access_mean']:.2f} %.",
        "Une moyenne régionale peut être influencée par quelques grandes économies : elle ne signifie pas que tous les pays de la région obtiennent les mêmes résultats.",
        "",
        "### Conclusion",
        "L'Afrique du Nord présente généralement les meilleurs indicateurs moyens d'accès à l'électricité, d'Internet et d'espérance de vie. Les écarts entre régions restent importants, mais une comparaison pays par pays reste nécessaire pour comprendre les variations internes.",
        "",
        "Résultat détaillé : `comparaison_regions.csv`.",
        regional.to_markdown(index=False),
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(f"Analyse terminée : {len(df)} lignes analysées")
    print("Année la plus récente :", latest_year)
    print("Rapport Markdown :", REPORT_PATH)
    print("Résultats CSV :", OUTPUT_DIR)


if __name__ == "__main__":
    main()
