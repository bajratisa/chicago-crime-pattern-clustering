# Chicago Crime Pattern Clustering (2020 to 2025)

Do Chicago's neighborhoods differ in the **kind** of crime they have, and does that connect to hardship and to the weather?

This project groups Chicago's 77 community areas into crime profiles based on the mix of crime types reported in each area, then tests whether those profiles are linked to socioeconomic hardship and to seasonal and temperature patterns. It is a pattern finding project, not a prediction project.

**Course:** Computer Programming for Data Science and Artificial Intelligence, Asian Institute of Technology (AIT), August 2026 semester

**Instructor:** Dr. Chantri Polprasert

**Status:** progress stage

## Objective

Identify stable neighborhood crime profiles across the 77 community areas, based on the mix of crime types reported in each area, and then examine whether those profiles are associated with socioeconomic hardship and with seasonal and temperature patterns.

## Main findings so far

- **The original K-Means clusters mostly measure crime volume.** Clustering on total crime rate alone gives almost the same groups (adjusted Rand index 0.86).
- **Crime mix gives three clear profiles:** violence heavy (35 areas), theft heavy (13 areas) and mixed (29 areas), with a silhouette score of 0.40 at the area level. The profiles follow recognizable parts of the city even though no locations were used in the clustering.
- **The kind of crime is tied to hardship far more than the amount.** The crime mix explains 72% of the differences in hardship (R squared 0.72), against 19% for total crime rate. Theft has no link to hardship (Spearman rho 0.02).
- **Stability depends on the settings.** The share of areas that stay in one group for all six years ranges from 45% to 83% for the original groups. The crime mix profiles are stable for 56% of areas with three profiles.
- **Temperature is linked to more crime.** A 10°F warmer day has about 3% to 6% more crime citywide (0.57% per °F, 95% CI 0.49 to 0.65, in the main model) after controlling for weekday, month, year and one outlier day.
- **Weather and hardship.** Every area has more crime in summer (average summer to winter ratio 1.23), and this increase has almost no link to hardship. On warmer days within a month, areas with more hardship react slightly more (Spearman rho 0.35).

These are associations between areas. They do not show that hardship or weather causes a particular crime mix.

## Repository structure

```
chicago-crime-pattern-clustering/
├── progress_analysis.ipynb   Main analysis notebook (run from top to bottom)
├── data/                     Input data (see data/README.md)
├── requirements.txt          Python packages
├── .gitignore
├── LICENSE
└── README.md
```

The notebook reads its inputs from `data/` and writes `cleaned_crime.csv`, `cleaned_weather.csv` and `cleaned_hardship.csv` to the folder it runs in. These files can be regenerated and are not tracked by Git.

## Data

| File in `data/` | What it is | Source |
| --- | --- | --- |
| `crime_data.csv` | Crime reports, 2020 to 2025, seven crime types | Chicago Data Portal, "Crimes, 2001 to Present" |
| `weather_data.csv` | Daily weather, Chicago O'Hare station | NOAA National Centers for Environmental Information |
| `hardship_index.csv` | Hardship Index for the 77 community areas, 2019 to 2023 | Great Cities Institute, University of Illinois Chicago |
| `chicago_health_data.csv` | Population and coordinates of each community area | Chicago Health Atlas |

Full details, column names and download instructions are in [`data/README.md`](data/README.md).

## Getting started

1. Clone the repository.

   ```bash
   git clone https://github.com/<your-username>/chicago-crime-pattern-clustering.git
   cd chicago-crime-pattern-clustering
   ```

2. Create and activate a virtual environment (Python 3.10 or newer).

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS or Linux
   source .venv/bin/activate
   ```

3. Install the packages.

   ```bash
   pip install -r requirements.txt
   ```

4. Put the four data files in the `data/` folder (see `data/README.md`).

5. Open `progress_analysis.ipynb` in Jupyter or VS Code and choose **Restart and Run All**. Always run the notebook from the top, because later cells depend on variables created earlier.

## Notebook guide

| Part of the notebook | What it does |
| --- | --- |
| Load datasets, exploratory analysis | Loads and cleans the data, and shows the main patterns over time and across areas |
| Clustering with K-Means | First clustering of the 77 areas, then the month by area table (5,544 rows), silhouette scores and cluster stability across years |
| Hypothesis tests | First look at weekday, temperature and season effects on daily crime |
| Comment 2 | Crime volume versus crime mix: clustering on total rate and on crime shares, adjusted Rand index, area level crime mix profiles |
| Comment 3 | Hardship as an outside variable: Spearman correlations, Kruskal Wallis tests, R squared for intensity and composition |
| Comment 4 | Stability checks across the number of clusters, scaling, crime types, the Loop and random starts |
| Comment 5 | Regression of daily crime on temperature with weekday, month, year and event controls, robust errors and residual checks |
| Comment 6 | Seasonal swing, temperature by profile regression and a temperature effect for each area |

## Methods in brief

- **Rates and shares.** Crime counts are converted to rates per 1,000 residents. Crime composition is measured as the share of each crime type, with a log ratio of violent crime to Theft for the hardship tests.
- **Clustering.** K-Means on standardized crime numbers, with the number of groups judged by the silhouette score. Two groupings are compared with the adjusted Rand index.
- **Stability.** One model is fitted on all months, each area's most common group is recorded for each year, and an area counts as stable if it keeps the same group in all six years.
- **Association tests.** Spearman correlation, Kruskal Wallis tests and linear regression with R squared.
- **Daily regression.** Log linear regression of the daily citywide crime count with HAC robust standard errors, a Poisson check, and a version with the previous day's crime.

## Limitations

- Associations are not causes, and recorded crime also reflects reporting and policing.
- Population (2011 to 2015), hardship (2019 to 2023) and crime (2020 to 2025) come from different years.
- Rates for areas with a large daytime population, such as the Loop, are inflated because that population is not counted as residents.
- All weather comes from one station at O'Hare Airport.
- Stability results are a sensitivity analysis and not a formal test. They depend on the number of groups, the scaling and the crime types used.

## Planned work

- Compare K-Means with hierarchical clustering on the area level crime shares.
- Recompute the profiles on log ratio transformed shares.
- Estimate the temperature effect separately for violent and property crimes.
- Link the results to Routine Activity Theory, Social Disorganization Theory and earlier weather and crime studies.

## Data sources and credits

- City of Chicago. Chicago Data Portal, Crimes, 2001 to Present. https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2
- National Oceanic and Atmospheric Administration, National Centers for Environmental Information. Daily Summaries, station USW00094846.
- Great Cities Institute, University of Illinois Chicago. Chicago community area hardship index, 2019 to 2023.
- Chicago Health Atlas.

## License

The code is released under the MIT License (see `LICENSE`). The datasets belong to their original publishers and are subject to their terms of use.
