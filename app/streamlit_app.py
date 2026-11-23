import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Dashboard Afrique",
    page_icon="🌍",
    layout="wide",
)

INDICATORS = {
    "PIB (USD)": "gdp",
    "PIB par habitant (USD)": "gdp_per_capita",
    "Population": "population",
    "Accès à l'électricité (%)": "electricity_access",
    "Utilisateurs d'Internet (%)": "internet_users",
    "Espérance de vie (années)": "life_expectancy",
    "Inflation (%)": "inflation_rate",
    "Chômage (%)": "unemployment_rate",
}

SUBREGIONS = {
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


@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/processed/african_development_clean.csv",
        keep_default_na=False,
    )
    df["african_subregion"] = df["country"].map(SUBREGIONS)
    for column in INDICATORS.values():
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset nettoyé introuvable. Exécutez : python src/clean_data.py")
    st.stop()

st.title("🌍 Dashboard analytique africain")
st.caption("Indicateurs de développement économique et social — Banque mondiale — 2000 à 2024")

st.sidebar.header("Filtres")
regions = sorted(df["african_subregion"].dropna().unique())
selected_regions = st.sidebar.multiselect("Région africaine", regions, default=regions)

available = df[df["african_subregion"].isin(selected_regions)]
selected_countries = st.sidebar.multiselect(
    "Pays",
    sorted(available["country"].unique()),
    default=[],
)

selected_years = st.sidebar.slider(
    "Période",
    int(df["year"].min()),
    int(df["year"].max()),
    (2000, 2024),
)

indicator_label = st.sidebar.selectbox("Indicateur principal", list(INDICATORS))
indicator = INDICATORS[indicator_label]

filtered = available[available["year"].between(*selected_years)].copy()
if selected_countries:
    filtered = filtered[filtered["country"].isin(selected_countries)]

if filtered.empty:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
    st.stop()

# Vue d'ensemble
st.header("Vue d'ensemble")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Pays sélectionnés", filtered["country"].nunique())
col2.metric("Population totale", f"{filtered['population'].sum()/1e6:.1f} M")
col3.metric("PIB moyen", f"{filtered['gdp'].mean()/1e9:.1f} Md $")
col4.metric("Espérance de vie", f"{filtered['life_expectancy'].mean():.1f} ans")

st.caption("Les KPI représentent l'ensemble des observations sélectionnées par les filtres.")

# Visualisation 1 : courbe temporelle
st.subheader("Analyse temporelle")
st.markdown("Évolution de l'indicateur sélectionné selon les années.")
temporal = filtered.groupby(["year", "country"], as_index=False)[indicator].mean()
line_fig = px.line(
    temporal,
    x="year",
    y=indicator,
    color="country",
    markers=True,
    title=f"Évolution de : {indicator_label}",
)
line_fig.update_layout(height=430, hovermode="x unified")
st.plotly_chart(line_fig, use_container_width=True)

# Visualisation 2 : comparaison géographique
st.subheader("Comparaison géographique")
st.markdown("Classement des pays à la dernière année sélectionnée.")
latest_year = int(filtered["year"].max())
geographic = (
    filtered[filtered["year"] == latest_year]
    .sort_values(indicator, ascending=False)
)
bar_fig = px.bar(
    geographic,
    x=indicator,
    y="country",
    orientation="h",
    color="african_subregion",
    title=f"{indicator_label} — Top pays en {latest_year}",
)
bar_fig.update_layout(height=480, yaxis={"categoryorder": "total ascending"})
st.plotly_chart(bar_fig, use_container_width=True)

# Visualisation 3 : comparaison régionale
st.subheader("Comparaison régionale")
st.markdown("Moyenne de l'indicateur sélectionné dans chaque sous-région.")
regional = (
    filtered.groupby("african_subregion", as_index=False)[indicator]
    .mean()
    .sort_values(indicator, ascending=False)
)
regional_fig = px.bar(
    regional,
    x="african_subregion",
    y=indicator,
    color="african_subregion",
    text_auto=".2f",
    title=f"Moyenne régionale : {indicator_label}",
)
regional_fig.update_layout(height=420, showlegend=False)
st.plotly_chart(regional_fig, use_container_width=True)

# Visualisation 4 : corrélation
st.subheader("Corrélations")
st.markdown("Relation linéaire entre les principaux indicateurs numériques.")
columns = [column for column in INDICATORS.values() if column in filtered.columns]
corr = filtered[columns].corr(numeric_only=True)
labels = [label for label, column in INDICATORS.items() if column in columns]
corr.index = labels
corr.columns = labels
corr_fig = px.imshow(
    corr,
    text_auto=".2f",
    aspect="auto",
    zmin=-1,
    zmax=1,
    color_continuous_scale="RdBu_r",
    title="Matrice de corrélation",
)
corr_fig.update_layout(height=520)
st.plotly_chart(corr_fig, use_container_width=True)

# Visualisation 5 : distribution
st.subheader("Distribution")
st.markdown("Répartition des valeurs de l'indicateur sélectionné.")
dist_fig = px.histogram(
    filtered,
    x=indicator,
    color="african_subregion",
    marginal="box",
    nbins=30,
    barmode="overlay",
    title=f"Distribution : {indicator_label}",
)
dist_fig.update_layout(height=460)
st.plotly_chart(dist_fig, use_container_width=True)

st.divider()
st.caption(
    "Source : Banque mondiale / World Development Indicators, 2000–2024. "
    "Données nettoyées : data/processed/african_development_clean.csv."
)
