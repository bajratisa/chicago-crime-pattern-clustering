# Data

The notebook expects these four files in this folder. File names must match exactly.

| File | Contents | Period | Source |
| --- | --- | --- | --- |
| `crime_data.csv` | One row per reported crime | 2020 to 2025 | Chicago Data Portal, "Crimes, 2001 to Present" |
| `weather_data.csv` | One row per day | 2020 to 2025 | NOAA NCEI Daily Summaries, station USW00094846 (Chicago O'Hare) |
| `hardship_index.csv` | One row per community area (77 rows) | 2019 to 2023 | Great Cities Institute, University of Illinois Chicago |
| `chicago_health_data.csv` | Population and coordinates for each community area | 2011 to 2015 extract | Chicago Health Atlas |

## Crime data

Download from the Chicago Data Portal (https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2) and filter before exporting:

- **Date:** from 01/01/2020 to 12/31/2025
- **Primary Type:** Theft, Battery, Criminal Damage, Assault, Burglary, Motor Vehicle Theft, Robbery

Export as CSV and save as `crime_data.csv`. The notebook uses the columns `Date`, `Primary Type`, `Arrest`, `Domestic`, `Community Area`, `Latitude` and `Longitude`, so the column headers must read exactly like this. The project used 1,065,276 reports, and 86 of them had no community area and were dropped. The portal is a live feed, so the count can differ slightly between downloads.

Do not open the raw file in Excel and save it again. Excel cuts files at 1,048,576 rows.

## Weather data

NOAA NCEI Daily Summaries for Chicago O'Hare International Airport (station USW00094846), 1 January 2020 to 31 December 2025, which gives 2,192 daily rows. The average temperature column (`TAVG`) is empty for this station, so the notebook recalculates it as (`TMAX` + `TMIN`) / 2. Columns used: `DATE`, `TMAX`, `TMIN`, `TAVG`, `PRCP`, `SNOW`.

## Hardship Index

Hardship Index scores for the 77 community areas, built from American Community Survey estimates for 2019 to 2023, with one row per community area. The table was copied by hand from the Great Cities Institute story map, because no direct download exists. Per capita income is stored as text with a dollar sign and commas, and the notebook converts it to numbers.

## Population and coordinates

Population, longitude and latitude of each community area from a Chicago Health Atlas download (2011 to 2015 extract). Only these three columns are used. The second row of the file is a description row, which is why the notebook reads it with `skiprows=[1]`. This file is older than the crime data, which is listed as a limitation of the analysis.

## Large files

GitHub rejects any single file over 100 MB and warns above 50 MB. If `crime_data.csv` is too large, either track it with Git LFS (see the main instructions) or leave it out of the repository by removing the `#` in front of `data/crime_data.csv` in `.gitignore`, and keep the download instructions above.
