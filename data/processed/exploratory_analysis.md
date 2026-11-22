# Analyse exploratoire

Dataset : 1350 observations, 54 pays, années 2000-2024.

Les tableaux CSV détaillés restent disponibles dans `data/processed/`. Cette section explique uniquement les résultats principaux sans reproduire une nouvelle visualisation.

## 1. Statistiques descriptives

### Ce que signifie cette analyse
Pour chaque indicateur numérique, nous observons le minimum, le maximum, la moyenne, la médiane et l'écart-type.

- Le **minimum** représente la plus petite valeur observée.
- Le **maximum** représente la plus grande valeur observée.
- La **moyenne** est la somme des valeurs divisée par leur nombre.
- La **médiane** est la valeur centrale : elle est plus fiable que la moyenne lorsque quelques pays ont des valeurs très élevées.
- L'**écart-type** mesure la dispersion : plus il est élevé, plus les observations sont éloignées les unes des autres.

### Exemple de compréhension
L'accès à l'électricité varie de 0.80 % à 100.00 %, avec une moyenne de 45.70 % et une médiane de 42.95 %. Cela montre de fortes différences entre les pays.
Pour le PIB, la moyenne est 37.8 milliards de dollars, alors que la médiane est 11.5 milliards. Cette différence indique une distribution très asymétrique : quelques grandes économies tirent la moyenne vers le haut.
Pour l'espérance de vie, la moyenne est 60.45 ans et la médiane est 60.41 ans. Les valeurs sont donc assez regroupées autour du même niveau.

### Conclusion
Il existe une forte hétérogénéité économique entre les pays africains. Pour les indicateurs comme le PIB ou le PIB par habitant, la médiane est souvent plus représentative que la moyenne.

Résultat détaillé : `statistics_descriptive.csv`.
|                       |   count |           mean |            std |             min |         median |             max |
|:----------------------|--------:|---------------:|---------------:|----------------:|---------------:|----------------:|
| electricity_access    |    1350 |   45.699       |   29.595       |     0.8         |   42.95        |   100           |
| gdp                   |    1350 |    3.78308e+10 |    8.20296e+10 |     7.59511e+07 |    1.14656e+10 |     6.6822e+11  |
| gdp_per_capita        |    1350 | 2278.81        | 2944.3         |   109.594       | 1081.96        | 19141.5         |
| inflation_rate        |    1350 |   10.116       |   31.435       |   -16.86        |    5.418       |   557.202       |
| internet_users        |    1350 |   16.516       |   20.503       |     0.006       |    7           |    91.2         |
| life_expectancy       |    1350 |   60.453       |    7.664       |    14.665       |   60.414       |    77.237       |
| population            |    1350 |    2.11741e+07 |    3.1363e+07  | 81131           |    1.13304e+07 |     2.32679e+08 |
| unemployment_rate     |    1350 |    9.106       |    7.337       |     0.316       |    5.783       |    36.472       |
| gdp_growth_yoy        |    1266 |    8.279       |   16.668       |   -61.032       |    7.473       |   164.438       |
| population_growth_yoy |    1296 |    2.385       |    1.205       |    -5.272       |    2.495       |    20.774       |

## 2. Analyse des corrélations

### Ce que signifie cette analyse
La corrélation mesure la relation linéaire entre deux variables. Sa valeur varie entre -1 et 1.

- Proche de 1 : les deux variables augmentent ensemble.
- Proche de -1 : lorsque l'une augmente, l'autre tend à diminuer.
- Proche de 0 : aucune relation linéaire importante n'est visible.
- Une corrélation ne démontre pas une relation de cause à effet.

### Exemples de compréhension
La corrélation entre l'accès à l'électricité et l'espérance de vie est 0,729 : les pays mieux électrifiés ont généralement une espérance de vie plus élevée.
La corrélation entre l'accès à l'électricité et les utilisateurs d'Internet est 0,662 : le développement numérique est accompagné d'une meilleure couverture électrique.
La corrélation entre le PIB et la population est 0,756 : les pays plus peuplés disposent généralement d'économies plus importantes.
À l'inverse, la corrélation entre la croissance démographique et l'accès à l'électricité est -0,389 : une croissance rapide de la population peut exercer une pression sur les infrastructures.

### Conclusion
Les relations les plus importantes concernent l'électricité, l'Internet, l'espérance de vie et le PIB par habitant. L'inflation présente des corrélations généralement faibles avec les autres indicateurs dans ce dataset.

Résultat détaillé : `correlations.csv`.
|                       |   electricity_access |    gdp |   gdp_per_capita |   inflation_rate |   internet_users |   life_expectancy |   population |   unemployment_rate |   gdp_growth_yoy |   population_growth_yoy |
|:----------------------|---------------------:|-------:|-----------------:|-----------------:|-----------------:|------------------:|-------------:|--------------------:|-----------------:|------------------------:|
| electricity_access    |                1     |  0.352 |            0.629 |           -0.091 |            0.662 |             0.729 |        0.079 |               0.368 |           -0.088 |                  -0.389 |
| gdp                   |                0.352 |  1     |            0.181 |            0.01  |            0.308 |             0.139 |        0.756 |               0.133 |           -0.027 |                  -0.093 |
| gdp_per_capita        |                0.629 |  0.181 |            1     |           -0.07  |            0.518 |             0.466 |       -0.114 |               0.331 |           -0.017 |                  -0.205 |
| inflation_rate        |               -0.091 |  0.01  |           -0.07  |            1     |           -0.055 |            -0.103 |        0.079 |               0.003 |           -0.036 |                  -0.037 |
| internet_users        |                0.662 |  0.308 |            0.518 |           -0.055 |            1     |             0.587 |        0.058 |               0.248 |           -0.164 |                  -0.306 |
| life_expectancy       |                0.729 |  0.139 |            0.466 |           -0.103 |            0.587 |             1     |       -0.012 |               0.124 |           -0.122 |                  -0.196 |
| population            |                0.079 |  0.756 |           -0.114 |            0.079 |            0.058 |            -0.012 |        1     |              -0.176 |           -0.012 |                   0.081 |
| unemployment_rate     |                0.368 |  0.133 |            0.331 |            0.003 |            0.248 |             0.124 |       -0.176 |               1     |           -0.043 |                  -0.286 |
| gdp_growth_yoy        |               -0.088 | -0.027 |           -0.017 |           -0.036 |           -0.164 |            -0.122 |       -0.012 |              -0.043 |            1     |                   0.152 |
| population_growth_yoy |               -0.389 | -0.093 |           -0.205 |           -0.037 |           -0.306 |            -0.196 |        0.081 |              -0.286 |            0.152 |                   1     |

## 3. Top 10 et Flop 10 du PIB — 2024

### Ce que signifie cette analyse
Le Top 10 rassemble les dix pays ayant le PIB total le plus élevé. Le Flop 10 rassemble les dix pays ayant le PIB total le plus faible.
Le PIB mesure la taille totale de l'économie. Il ne mesure pas directement le niveau de vie moyen : les pays très peuplés peuvent avoir un PIB élevé avec un PIB par habitant faible.

### Exemples de compréhension
En 2024, South Africa est au premier rang avec environ 401.1 milliards de dollars de PIB.
À l'autre extrémité, Sao Tome and Principe est le plus faible du classement pour cette année, avec environ 0.825 milliard de dollars.
La comparaison Nigeria–Côte d'Ivoire illustre aussi la différence entre PIB total et PIB par habitant : un PIB élevé peut accompagner une population importante, sans assurer un revenu élevé par personne.

### Conclusion
Le classement met en évidence les grandes économies africaines du Top 10, mais il ne suffit pas à mesurer le développement ou la richesse moyenne.

Résultats détaillés : `top10_gdp.csv` et `flop10_gdp.csv`.
| country          |         gdp |   gdp_per_capita |   population |   life_expectancy |
|:-----------------|------------:|-----------------:|-------------:|------------------:|
| South Africa     | 4.01145e+11 |          6267.19 |  6.40072e+07 |            66.312 |
| Egypt, Arab Rep. | 3.8906e+11  |          3338.47 |  1.16538e+08 |            71.806 |
| Algeria          | 2.69322e+11 |          5752.99 |  4.68143e+07 |            76.475 |
| Nigeria          | 2.52262e+11 |          1084.16 |  2.32679e+08 |            54.635 |
| Morocco          | 1.60611e+11 |          4153.19 |  3.80812e+07 |            75.493 |
| Ethiopia         | 1.4974e+11  |          1133.88 |  1.3206e+08  |            67.603 |
| Kenya            | 1.20398e+11 |          2133.46 |  5.64329e+07 |            63.834 |
| Angola           | 1.03081e+11 |          2720.82 |  3.78858e+07 |            64.805 |
| Cote d'Ivoire    | 8.71132e+10 |          2727.89 |  3.19342e+07 |            62.11  |
| Ghana            | 8.32886e+10 |          2419.25 |  3.44274e+07 |            65.695 |

Flop 10 :
| country                  |         gdp |   gdp_per_capita |       population |   life_expectancy |
|:-------------------------|------------:|-----------------:|-----------------:|------------------:|
| Sao Tome and Principe    | 8.24993e+08 |         3502.62  | 235536           |           69.905  |
| Eritrea                  | 1.16011e+09 |          437.419 |      3.5356e+06  |           68.893  |
| Comoros                  | 1.61008e+09 |         1857.87  | 866628           |           67.023  |
| Guinea-Bissau            | 2.19778e+09 |          998.376 |      2.20135e+06 |           64.254  |
| Seychelles               | 2.22861e+09 |        18364.5   | 121354           |           76.2951 |
| Lesotho                  | 2.39128e+09 |         1023.04  |      2.33742e+06 |           57.798  |
| Gambia, The              | 2.40489e+09 |          871.34  |      2.75999e+06 |           66.057  |
| Cabo Verde               | 2.71372e+09 |         5170.21  | 524877           |           76.224  |
| Central African Republic | 2.75149e+09 |          516.161 |      5.33069e+06 |           57.671  |
| Burundi                  | 3.03758e+09 |          216.232 |      1.40478e+07 |           63.818  |

## 4. Analyse temporelle

### Ce que signifie cette analyse
L'analyse temporelle observe les moyennes ou totaux annuels. Elle permet de repérer une progression, une stagnation, une baisse ou une rupture liée à une crise.

### Exemples de compréhension
Entre 2000 et 2024, la population totale passe d'environ 0.829 milliard à 1.512 milliard.
L'accès moyen à l'électricité passe de 33.36 % à 61.88 %.
La part moyenne d'utilisateurs d'Internet passe de 0.89 % à 42.49 %.
L'espérance de vie moyenne passe de 55.05 ans à 65.69 ans.
La baisse observée autour de 2020 peut être liée à une perturbation économique mondiale ou à des effets sanitaires, mais une vérification par indicateur est nécessaire avant d'attribuer une cause.

### Conclusion
La tendance générale sur la période est positive pour l'électricité, l'Internet et l'espérance de vie. Le PIB connaît une progression globale avec plusieurs fluctuations annuelles.

Résultat détaillé : `evolution_temporelle.csv`.
|   year |    gdp_mean |   gdp_median |   gdp_total |   population_total |   electricity_access_mean |   internet_users_mean |   life_expectancy_mean |   unemployment_rate_mean |
|-------:|------------:|-------------:|------------:|-------------------:|--------------------------:|----------------------:|-----------------------:|-------------------------:|
|   2000 | 1.28925e+10 |  3.76143e+09 | 6.96198e+11 |        8.28997e+08 |                    33.363 |                 0.892 |                 55.053 |                    9.571 |
|   2001 | 1.25423e+10 |  4.10936e+09 | 6.77283e+11 |        8.50058e+08 |                    34.048 |                 1.207 |                 55.413 |                    9.572 |
|   2002 | 1.29017e+10 |  4.47442e+09 | 6.9669e+11  |        8.7174e+08  |                    34.461 |                 1.618 |                 55.779 |                    9.614 |
|   2003 | 1.55554e+10 |  5.18721e+09 | 8.39991e+11 |        8.94023e+08 |                    35.767 |                 2.049 |                 56.211 |                    9.612 |
|   2004 | 1.87226e+10 |  5.99939e+09 | 1.01102e+12 |        9.17026e+08 |                    36.7   |                 2.99  |                 56.742 |                    9.366 |
|   2005 | 2.19955e+10 |  6.94919e+09 | 1.18776e+12 |        9.40755e+08 |                    37.043 |                 3.416 |                 57.23  |                    9.269 |
|   2006 | 2.58083e+10 |  8.03704e+09 | 1.39365e+12 |        9.65106e+08 |                    38.97  |                 4.253 |                 57.82  |                    9.06  |
|   2007 | 2.98942e+10 |  8.81112e+09 | 1.61429e+12 |        9.90198e+08 |                    39.496 |                 4.941 |                 58.396 |                    8.969 |
|   2008 | 3.47882e+10 |  1.0728e+10  | 1.87857e+12 |        1.01618e+09 |                    39.996 |                 5.932 |                 58.932 |                    8.837 |
|   2009 | 3.31078e+10 |  9.73096e+09 | 1.78782e+12 |        1.04288e+09 |                    40.522 |                 7.084 |                 58.835 |                    8.915 |
|   2010 | 3.87017e+10 |  1.17396e+10 | 2.08989e+12 |        1.07031e+09 |                    42.428 |                 8.651 |                 59.91  |                    8.997 |
|   2011 | 4.28298e+10 |  1.43641e+10 | 2.31281e+12 |        1.0982e+09  |                    43.933 |                 9.98  |                 60.112 |                    9.066 |
|   2012 | 4.57423e+10 |  1.34748e+10 | 2.47008e+12 |        1.12684e+09 |                    44.73  |                11.613 |                 61.02  |                    8.911 |
|   2013 | 4.7844e+10  |  1.50095e+10 | 2.58358e+12 |        1.15671e+09 |                    45.772 |                13.643 |                 61.502 |                    8.757 |
|   2014 | 4.95365e+10 |  1.47162e+10 | 2.67497e+12 |        1.18707e+09 |                    46.965 |                15.953 |                 61.51  |                    8.702 |
|   2015 | 4.46281e+10 |  1.22985e+10 | 2.40992e+12 |        1.21784e+09 |                    47.852 |                19.206 |                 62.079 |                    8.824 |
|   2016 | 4.19143e+10 |  1.24134e+10 | 2.26337e+12 |        1.24888e+09 |                    50.007 |                21.904 |                 62.469 |                    8.78  |
|   2017 | 4.3546e+10  |  1.33068e+10 | 2.35148e+12 |        1.28048e+09 |                    51.113 |                25.094 |                 62.703 |                    8.799 |
|   2018 | 4.65929e+10 |  1.48657e+10 | 2.51602e+12 |        1.31291e+09 |                    53.337 |                27.273 |                 63.55  |                    8.706 |
|   2019 | 5.20251e+10 |  1.45185e+10 | 2.80935e+12 |        1.34545e+09 |                    54.189 |                30.972 |                 63.668 |                    8.794 |
|   2020 | 4.9495e+10  |  1.42548e+10 | 2.67273e+12 |        1.3782e+09  |                    55.389 |                34.818 |                 63.904 |                    9.617 |
|   2021 | 5.52961e+10 |  1.652e+10   | 2.98599e+12 |        1.41105e+09 |                    56.819 |                37.33  |                 63.164 |                    9.745 |
|   2022 | 5.96781e+10 |  1.7627e+10  | 3.22262e+12 |        1.44409e+09 |                    57.826 |                39.664 |                 64.186 |                    9.112 |
|   2023 | 5.57108e+10 |  1.88707e+10 | 3.00838e+12 |        1.47788e+09 |                    59.87  |                39.917 |                 65.441 |                    9.02  |
|   2024 | 5.40208e+10 |  1.98182e+10 | 2.91712e+12 |        1.5122e+09  |                    61.885 |                42.49  |                 65.688 |                    9.028 |

## 5. Comparaison régionale

### Ce que signifie cette analyse
Cette comparaison regroupe les pays dans cinq sous-régions africaines afin de comparer leurs moyennes. Elle permet d'observer les écarts structurels sans confondre une moyenne régionale avec les résultats de chaque pays.

### Exemples de compréhension
La région présentant le PIB par habitant moyen le plus élevé est Afrique australe avec environ 4,113 dollars.
La région ayant le meilleur accès moyen à l'électricité est Afrique du Nord avec environ 85.32 %.
Une moyenne régionale peut être influencée par quelques grandes économies : elle ne signifie pas que tous les pays de la région obtiennent les mêmes résultats.

### Conclusion
L'Afrique du Nord présente généralement les meilleurs indicateurs moyens d'accès à l'électricité, d'Internet et d'espérance de vie. Les écarts entre régions restent importants, mais une comparaison pays par pays reste nécessaire pour comprendre les variations internes.

Résultat détaillé : `comparaison_regions.csv`.
| african_subregion   |   countries |    gdp_mean |   gdp_per_capita_mean |   population_mean |   electricity_access_mean |   internet_users_mean |   life_expectancy_mean |   unemployment_rate_mean |
|:--------------------|------------:|------------:|----------------------:|------------------:|--------------------------:|----------------------:|-----------------------:|-------------------------:|
| Afrique australe    |           5 | 7.2358e+10  |               4113.02 |       1.24341e+07 |                    52.909 |                25.836 |                 56.2   |                   22.044 |
| Afrique centrale    |           9 | 2.17127e+10 |               2916.36 |       1.65754e+07 |                    42.65  |                14.851 |                 57.812 |                   10.149 |
| Afrique de l'Est    |          18 | 1.64075e+10 |               1959.6  |       2.04877e+07 |                    38.071 |                12.355 |                 60.641 |                    7.427 |
| Afrique de l'Ouest  |          16 | 3.41658e+10 |               1141.08 |       2.1387e+07  |                    38.884 |                14.197 |                 59.242 |                    4.6   |
| Afrique du Nord     |           6 | 1.07279e+11 |               3785.59 |       3.68474e+07 |                    85.323 |                29.911 |                 70.622 |                   13.812 |