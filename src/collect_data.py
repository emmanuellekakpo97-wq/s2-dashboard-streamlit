import requests
import pandas as pd
from pathlib import Path

BASE_URL = "https://api.worldbank.org/v2"

# Codes ISO2 des 54 pays africains
AFRICAN_COUNTRIES = [
    "DZ", "AO", "BJ", "BW", "BF", "BI", "CV", "CM", "CF",
    "TD", "KM", "CG", "CD", "CI", "DJ", "EG", "GQ", "ER",
    "SZ", "ET", "GA", "GM", "GH", "GN", "GW", "KE", "LS",
    "LR", "LY", "MG", "MW", "ML", "MR", "MU", "MA", "MZ",
    "NA", "NE", "NG", "RW", "ST", "SN", "SC", "SL", "SO",
    "ZA", "SS", "SD", "TZ", "TG", "TN", "UG", "ZM", "ZW"
]

INDICATORS = {
    "NY.GDP.MKTP.CD": "gdp",
    "NY.GDP.PCAP.CD": "gdp_per_capita",
    "SP.POP.TOTL": "population",
    "SP.DYN.LE00.IN": "life_expectancy",
    "SE.ADT.LITR.ZS": "literacy_rate",
    "IT.NET.USER.ZS": "internet_users",
    "EG.ELC.ACCS.ZS": "electricity_access",
    "SL.UEM.TOTL.ZS": "unemployment_rate",
    "EN.ATM.CO2E.PC": "co2_per_capita",
    "FP.CPI.TOTL.ZG": "inflation_rate",
}


def get_json(url, params, timeout=180):
    """Effectue une requête API robuste et retourne le contenu JSON."""
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def collect_data():
    # Récupérer les informations sur les pays
    countries_url = f"{BASE_URL}/country"
    countries_params = {"format": "json", "per_page": 400}

    countries_payload = get_json(countries_url, countries_params, timeout=60)

    if len(countries_payload) < 2 or countries_payload[1] is None:
        raise RuntimeError("Impossible de récupérer la liste des pays.")

    countries = {
        country["id"]: {
            "country": country["name"],
            "country_code": country["iso2Code"],
            "region": country["region"]["value"],
            "income_level": country["incomeLevel"]["value"],
        }
        for country in countries_payload[1]
        if country["iso2Code"] in AFRICAN_COUNTRIES
    }

    print(f"{len(countries)} pays africains identifiés.")

    if len(countries) != 54:
        print("Attention : certains pays africains n'ont pas été trouvés par l'API.")

    records = []

    # Une seule requête par indicateur avec tous les pays évite les URL trop longues.
    for indicator_code, indicator_name in INDICATORS.items():
        print(f"Téléchargement : {indicator_name}")

        indicator_url = f"{BASE_URL}/country/all/indicator/{indicator_code}"
        params = {
            "format": "json",
            "date": "2000:2024",
            "per_page": 20000,
        }

        try:
            payload = get_json(indicator_url, params)
        except requests.RequestException as exc:
            print(f"Erreur pour {indicator_name} : {exc}")
            continue

        if len(payload) < 2 or payload[1] is None:
            print(f"Aucune donnée pour {indicator_name}")
            continue

        for item in payload[1]:
            country_iso3 = item["countryiso3code"]
            country_info = countries.get(country_iso3)

            if country_info is None or item["value"] is None:
                continue

            records.append({
                "country": country_info["country"],
                "country_code": country_info["country_code"],
                "region": country_info["region"],
                "income_level": country_info["income_level"],
                "year": int(item["date"]),
                "indicator": indicator_name,
                "value": item["value"],
            })

    if not records:
        raise RuntimeError("Aucune donnée n'a été récupérée depuis l'API.")

    df = pd.DataFrame(records)

    # Transformer les indicateurs en colonnes
    df = df.pivot_table(
        index=[
            "country", "country_code", "region",
            "income_level", "year"
        ],
        columns="indicator",
        values="value",
        aggfunc="first",
    ).reset_index()

    df.columns.name = None

    return df


if __name__ == "__main__":
    print("Début de la collecte des données...")

    df = collect_data()

    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "african_development.csv"

    df.to_csv(output_path, index=False)

    print("\nCollecte terminée !")
    print("Nombre de lignes :", len(df))
    print("Nombre de colonnes :", len(df.columns))
    print("Fichier enregistré :", output_path)
    print(df.head())