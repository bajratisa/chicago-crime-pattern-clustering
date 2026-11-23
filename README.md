# Urban Crime Pattern Clustering in Chicago (2020 to 2025)

Do Chicago's neighborhoods differ in the **kind** of crime they have, and does that connect to hardship and to the weather?

This project groups Chicago's 77 community areas into crime profiles based on the mix of crime types reported in each area, then tests whether those profiles are linked to socioeconomic hardship and to seasonal and temperature patterns. It is a pattern finding project, not a prediction project.

- **Course:** Computer Programming for Data Science and Artificial Intelligence, Asian Institute of Technology (AIT), August 2026 semester
- **Instructor:** Dr. Chantri Polprasert
- **Status:** final stage
- **Team:** NekoLab: Tisa Bajracharya (st126686), Min Thant Win (st127145)
- **Live website:** https://chicago-crime-mix.streamlit.app/
- **Final report and slides:** see the [`docs`](docs/) folder

## Objective

Identify stable neighborhood crime profiles across the 77 community areas, based on the mix of crime types reported in each area, and then examine whether those profiles are associated with socioeconomic hardship and with seasonal and temperature patterns.

## Main findings

- **Crime volume and crime mix give different groups.** The original K-Means clusters mostly measure how much crime an area has: clustering on total crime rate alone gives almost the same groups (adjusted Rand index 0.86).
- **Crime mix gives three profiles:** violence heavy (35 areas), theft heavy (13 areas) and mixed (29 areas), with a silhouette score of 0.40 at the area level. The profiles follow recognizable parts of the city even though no locations were used in the clustering.
- **The kind of crime is tied to hardship far more than the amount.** The crime mix explains 72% of the differences in hardship (R squared 0.72), against 19% for total crime rate. Theft has no link to hardship (Spearman rho 0.02).
- **The core of the profiles holds under a second method.** Hierarchical clustering agrees with K-Means on 46 of the 77 areas under all three linkage methods tested; the other areas sit near a border between two profiles. Hardship separates the groups in the same order under every method (Kruskal Wallis p < 0.001).
- **The profiles mostly survive a log ratio transformation.** On centred log ratio shares, 61 of 77 areas keep their profile, including 34 of the 35 violence heavy areas, and the link to hardship remains strong.
- **Stability depends on the settings.** For the crime mix profiles, 56% of areas keep the same profile in all six years under the main setting, ranging from 30% to 62% depending on how the shares are scaled. Removing Theft drops stability to 12% to 13%, so the stable part of the crime mix is the contrast between Theft and other crime.
- **Temperature is linked to more crime.** A 10°F warmer day has about 3% to 6% more crime citywide after controlling for weekday, month, year and one outlier day (0.57% per °F, 95% CI 0.49 to 0.65, in the main model).
- **Violent crime reacts slightly more to heat.** Violent crime rises about 6.7% per 10°F against 5.3% for property crime, a small but statistically significant difference (p = 0.016).
- **Weather and hardship.** Every area has more crime in summer (average summer to winter ratio 1.23), and this increase has almost no link to hardship. On warmer days within a month, areas with more hardship react slightly more (Spearman rho 0.35).

These are associations between areas. They do not show that hardship or weather causes a particular crime mix.

## Repository structure

```
chicago-crime-pattern-clustering/
├── final_analysis.ipynb      Final analysis notebook (run from top to bottom)
├── progress_analysis.ipynb   Notebook as submitted at the progress stage, kept for the record
├── figures/                  Figures saved by the final notebook
├── website/                  Streamlit website
│   ├── app.py
│   ├── requirements.txt
│   └── app_data/             Small summary tables written by the final notebook
├── .streamlit/config.toml    Website colours and theme
├── data/                     Input data (see data/README.md)
├── requirements.txt          Python packages for the notebooks
├── .gitignore
├── LICENSE
└── README.md
```

The notebooks read their inputs from `data/`. The final notebook also writes `cleaned_crime.csv`, `cleaned_weather.csv` and `cleaned_hardship.csv` to the folder it runs in (not tracked by Git), the figures to `figures/`, and the website's summary tables to `website/app_data/`.

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
   git clone https://github.com/bajratisa/chicago-crime-pattern-clustering.git
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

4. Download `crime_data.csv` and put it in the `data/` folder (see `data/README.md`). The other three data files are already in the repository. The crime file is about 280 MB, which is too big for GitHub.

5. Open `final_analysis.ipynb` in Jupyter or VS Code and choose **Restart and Run All**. Always run the notebook from the top, because later cells depend on variables created earlier.

### Running the website on your own computer

```bash
pip install -r website/requirements.txt
streamlit run website/app.py
```

The website only needs the three files in `website/app_data/`, so it runs without the raw data.

## Notebook guide (`final_analysis.ipynb`)

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
| Part A | K-Means compared with hierarchical clustering (Ward, average, complete and single linkage): agreement, dendrogram, robust core areas and hardship test |
| Part B | Crime mix profiles recomputed on centred log ratio shares |
| Part C | Temperature effect for violent and property crimes, with a direct test of the difference |
| Part D | Stability of the crime mix profiles across scaling, crime type and random start settings |
| Export for the website | Saves the summary tables used by the website |

## Methods in brief

- **Rates and shares.** Crime counts are converted to rates per 1,000 residents. Crime composition is measured as the share of each crime type, with a log ratio of violent crime to Theft for the hardship tests.
- **Clustering.** K-Means on crime shares, with the number of groups judged by the silhouette score. Hierarchical clustering is used as a second method, and groupings are compared with the adjusted Rand index.
- **Compositional check.** The centred log ratio transformation handles the fact that crime shares add up to 100%.
- **Stability.** One model is fitted on all years, each area's group is recorded for each year, and an area counts as stable if it keeps the same group in all six years.
- **Association tests.** Spearman correlation, Kruskal Wallis tests and linear regression with R squared.
- **Daily regression.** Log linear regression of the daily citywide crime count with HAC robust standard errors, a Poisson check, a version with the previous day's crime, and separate models for violent and property crime.

## Limitations

- Associations are not causes, and recorded crime also reflects reporting and policing.
- Population (2011 to 2015), hardship (2019 to 2023) and crime (2020 to 2025) come from different years.
- Rates for areas with a large daytime population, such as the Loop, are inflated because that population is not counted as residents.
- All weather comes from one station at O'Hare Airport.
- The borders between profiles depend on the clustering method and on how the shares are transformed; only the core areas are stable across methods.
- Stability results are a sensitivity analysis and not a formal test. They depend on the number of groups, the scaling and the crime types used.

## Future work

- A formal stability test by resampling months, giving a confidence level for each area's profile.
- Exposure adjusted rates that account for daytime population, for example near transit stations, shopping areas and universities.
- Separate violent and property temperature effects for each community area.
- A formal spatial test of whether neighboring areas share the same profile.

## Data sources and credits

- City of Chicago. Chicago Data Portal, Crimes, 2001 to Present. https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2
- National Oceanic and Atmospheric Administration, National Centers for Environmental Information. Daily Summaries, station USW00094846.
- Great Cities Institute, University of Illinois Chicago. Chicago community area hardship index, 2019 to 2023.
- Chicago Health Atlas.
- Website map tiles © OpenStreetMap contributors.

## License

The code is released under the MIT License (see `LICENSE`). The datasets belong to their original publishers and are subject to their terms of use.
