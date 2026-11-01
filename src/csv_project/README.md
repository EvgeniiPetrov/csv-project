🌐 Language: **English** | [Русский](README_RU.md)
# CSV Project — Pump Station Measurement Analysis

A Python learning project for reading, validating, and analyzing pump station measurements stored in CSV files.

## Features

- Read comma-separated CSV files using the Python standard library.
- Validate required columns: `timestamp`, `pump_id`, `pressure_mpa`, and `temperature_c` (additional columns are allowed).
- Validate individual measurements and separate valid from invalid records.
- Group valid measurements by pump ID.
- Calculate the measurement count, minimum and maximum pressure, average pressure, and average temperature for each pump.
- Display validation messages and calculated statistics in the console.

## Input format

| Column | Description | Expected value |
| --- | --- | --- |
| `timestamp` | Measurement date and time | `YYYY-MM-DD HH:MM:SS` |
| `pump_id` | Pump identifier | Non-empty string |
| `pressure_mpa` | Pressure in megapascals (MPa) | `0` to `2`, inclusive |
| `temperature_c` | Temperature in degrees Celsius (°C) | `-40` to `150`, inclusive |

Sample datasets: [clean data](src/csv_project/csv_training_tz01/measurements_clean.csv), [minor errors](src/csv_project/csv_training_tz01/measurements_minor_errors.csv), and [more invalid records](src/csv_project/csv_training_tz01/measurements_bad.csv).

## Run

Run the script from the repository root:

```bash
python src/csv_project/main.py
```

The input CSV path is currently configured in [`src/csv_project/main.py`](src/csv_project/main.py) through `input_csv_file`. No third-party Python packages are required for the current implementation.

## Project status

CSV loading, validation, grouping, and per-pump calculations are implemented. Exporting the sorted `report.csv` file and completing the final processing summary are still in progress.

## Author and license

Developed by [Evgenii Petrov](https://github.com/EvgeniiPetrov) as a hands-on Python and data engineering learning project.

Copyright © 2026 Evgenii Petrov. Licensed under the [MIT License](LICENSE). When redistributing the software or substantial parts of it, retain the copyright notice and license text as required by that license. The software is provided **as is**, without warranties; see [LICENSE](LICENSE) for the full terms and liability disclaimer.
