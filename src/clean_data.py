"""
Nettoyage du dataset africain de développement.

Source : data/raw/african_development.csv
Sortie : data/processed/african_development_clean.csv

Le fichier brut n'est jamais modifié.
"""

from pathlib import Path

import pandas as pd


# ============================================================
# 1. CHEMINS DU PROJET
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "african_development.csv"

PROCESSED_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "african_development_clean.csv"
)

OUTLIERS_REPORT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "outliers_report.csv"
)


# ============================================================
# 2. CONFIGURATION
# ============================================================

# Code ISO2 de la Namibie.
# Pandas peut interpréter "NA" comme une valeur manquante à la lecture du CSV.
COUNTRY_CODE_MAP = {
    "Namibia": "NA",
}

# Indicateurs numériques dont les valeurs manquantes peuvent être imputées.
NUMERIC_COLUMNS = [
    "electricity_access",
    "gdp",
    "gdp_per_capita",
    "inflation_rate",
    "internet_users",
    "life_expectancy",
    "population",
    "unemployment_rate",
]

# Indicateurs sur lesquels appliquer la règle IQR.
OUTLIER_COLUMNS = [
    "electricity_access",
    "gdp",
    "gdp_per_capita",
    "inflation_rate",
    "internet_users",
    "life_expectancy",
    "population",
    "unemployment_rate",
]


# ============================================================
# 3. NORMALISATION DES DONNÉES TEXTUELLES
# ============================================================

def normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise les noms de colonnes et les champs textuels."""

    df = df.copy()

    # Uniformisation des noms de colonnes.
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # Suppression des espaces inutiles dans les champs textuels.
    text_columns = [
        "country",
        "country_code",
        "region",
        "income_level",
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip()

    return df


# ============================================================
# 4. TRAITEMENT DES VALEURS MANQUANTES
# ============================================================

def impute_numeric_by_country_then_region(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Remplace les valeurs manquantes par :
    1. La médiane du pays.
    2. Si elle est indisponible, la médiane de la région.

    Une colonne indique les valeurs qui ont été imputées.
    """

    df = df.copy()

    for column in columns:

        if column not in df.columns:
            continue

        # Identification des valeurs manquantes avant traitement.
        df[f"{column}_was_imputed"] = df[column].isna()

        # Première étape : médiane du pays.
        df[column] = df[column].fillna(
            df.groupby("country", observed=True)[column].transform("median")
        )

        # Deuxième étape : médiane de la région.
        df[column] = df[column].fillna(
            df.groupby("region", observed=True)[column].transform("median")
        )

    return df


# ============================================================
# 5. DÉTECTION DES VALEURS EXTRÊMES AVEC LA RÈGLE IQR
# ============================================================

def detect_outliers(
    df: pd.DataFrame,
    columns: list[str],
) -> tuple[pd.DataFrame, dict[str, int]]:
    """
    Détecte les valeurs extrêmes avec la règle IQR.

    IQR = Q3 - Q1
    Borne inférieure = Q1 - 1.5 * IQR
    Borne supérieure = Q3 + 1.5 * IQR

    Les valeurs originales ne sont jamais modifiées. Seules les colonnes
    booléennes *_is_outlier et les bornes IQR sont conservées dans le fichier.
    """

    df = df.copy()
    outlier_counts: dict[str, int] = {}

    for column in columns:
        if column not in df.columns:
            continue

        series = df[column].dropna()
        if series.empty:
            outlier_counts[column] = 0
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        mask = df[column].notna() & (
            (df[column] < lower_bound)
            | (df[column] > upper_bound)
        )

        outlier_counts[column] = int(mask.sum())
        df[f"{column}_is_outlier"] = mask

    return df, outlier_counts


# ============================================================
# 6. CRÉATION DES INDICATEURS DE CROISSANCE
# ============================================================

def create_growth_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule les taux de croissance annuels du PIB et de la population."""

    df = df.copy()

    # Tri chronologique par pays.
    df = df.sort_values(
        ["country", "year"]
    ).reset_index(drop=True)

    for column, growth_column in [
        ("gdp", "gdp_growth_yoy"),
        ("population", "population_growth_yoy"),
    ]:

        if column not in df.columns:
            continue

        imputed_column = f"{column}_was_imputed"

        # Calcul de la variation annuelle en pourcentage.
        grouped = df.groupby("country", observed=True)

        previous_value = grouped[column].shift(1)
        previous_year = grouped["year"].shift(1)

        df[growth_column] = (
            (df[column] - previous_value)
            / previous_value
            * 100
        )

        # On évite de calculer une croissance si les années ne se suivent pas.
        consecutive_years = (df["year"] - previous_year) == 1

        # On évite d'utiliser une valeur imputée dans le calcul.
        current_imputed = df.get(
            imputed_column,
            pd.Series(False, index=df.index),
        ).fillna(False).astype(bool)

        previous_imputed = (
            grouped[imputed_column].shift(1)
            if imputed_column in df.columns
            else pd.Series(False, index=df.index)
        ).fillna(False).astype(bool)

        valid_values = (
            consecutive_years
            & ~current_imputed
            & ~previous_imputed
        )

        df.loc[~valid_values, growth_column] = pd.NA

    return df


# ============================================================
# 7. CRÉATION DU RAPPORT DES VALEURS EXTRÊMES
# ============================================================

def create_outliers_report(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Crée un rapport ligne par ligne des valeurs extrêmes détectées."""

    report_rows = []

    for column in columns:
        if column not in df.columns:
            continue

        series = df[column].dropna()
        if series.empty:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        mask = (
            (df[column] < lower_bound)
            | (df[column] > upper_bound)
        )

        for index in df.index[mask]:
            row = df.loc[index]
            report_rows.append(
                {
                    "indicator": column,
                    "country": row["country"],
                    "year": row["year"],
                    "region": row["region"],
                    "income_level": row["income_level"],
                    "value": row[column],
                    "lower_iqr_bound": lower_bound,
                    "upper_iqr_bound": upper_bound,
                    "direction": (
                        "below_lower_bound"
                        if row[column] < lower_bound
                        else "above_upper_bound"
                    ),
                    "was_imputed": bool(
                        row.get(f"{column}_was_imputed", False)
                    ),
                }
            )

    report = pd.DataFrame(report_rows)

    if not report.empty:
        report = report.sort_values(
            ["indicator", "year", "value"],
            ascending=[True, True, False],
        ).reset_index(drop=True)

    return report


# ============================================================
# 8. FONCTION PRINCIPALE DE NETTOYAGE
# ============================================================

def clean_data():

    """Charge, nettoie, enrichit et exporte le dataset."""

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Fichier source introuvable : {RAW_DATA_PATH}"
        )

    print("Lecture du dataset brut...")

    df = pd.read_csv(RAW_DATA_PATH)

    # Étape 1 : normalisation.
    df = normalize_text_columns(df)

    # Étape 2 : suppression des doublons pays/année.
    duplicate_count = df.duplicated(
        ["country", "year"]
    ).sum()

    if duplicate_count:
        df = df.drop_duplicates(
            ["country", "year"],
            keep="first",
        )

    # Étape 3 : correction du code ISO2 de la Namibie.
    for country, code in COUNTRY_CODE_MAP.items():
        df.loc[
            df["country"].eq(country),
            "country_code",
        ] = code

    # Vérification des codes pays encore absents.
    missing_country_codes = (
        df.loc[df["country_code"].isna(), "country"]
        .dropna()
        .unique()
        .tolist()
    )

    if missing_country_codes:
        print(
            "Codes pays non renseignés :",
            missing_country_codes,
        )

    # Étape 4 : détection IQR.
    # Elle est effectuée avant l'imputation pour calculer les bornes
    # à partir des valeurs réellement observées.
    df, outlier_counts = detect_outliers(
        df,
        OUTLIER_COLUMNS,
    )

    # Rapport des outliers calculé avant toute imputation.
    outliers_report = create_outliers_report(df, OUTLIER_COLUMNS)

    # Étape 5 : traitement des valeurs manquantes.
    df = impute_numeric_by_country_then_region(
        df,
        NUMERIC_COLUMNS,
    )

    # Étape 6 : suppression de literacy_rate.
    # Plus de 80 % des observations étaient manquantes.
    if "literacy_rate" in df.columns:
        df = df.drop(columns=["literacy_rate"])

    # Étape 7 : création des indicateurs de croissance.
    df = create_growth_indicators(df)

    # Étape 8 : export du rapport des valeurs extrêmes avant imputation.
    OUTLIERS_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not outliers_report.empty:
        outliers_report.to_csv(OUTLIERS_REPORT_PATH, index=False)

    return df, duplicate_count, outlier_counts


# ============================================================
# 9. EXPORT ET RAPPORT FINAL
# ============================================================

def main():

    df, duplicate_count, outlier_counts = clean_data()

    # Création du dossier de destination s'il n'existe pas.
    PROCESSED_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Export du dataset nettoyé.
    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False,
    )

    print("\n========== NETTOYAGE TERMINÉ ==========")

    print("Dimensions finales :", df.shape)

    print(
        "Doublons pays/année supprimés :",
        duplicate_count,
    )

    print("\nValeurs manquantes restantes :")
    print(df.isna().sum().to_string())

    print("\nNombre de valeurs extrêmes détectées avec IQR :")

    for column, count in outlier_counts.items():
        print(f"{column} : {count}")

    print("\nFichier exporté :")
    print(PROCESSED_DATA_PATH)

    print("\nRapport des outliers exporté :")
    print(OUTLIERS_REPORT_PATH)


if __name__ == "__main__":
    main()