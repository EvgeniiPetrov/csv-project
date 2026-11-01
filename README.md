🌐 Language: **English** | [Русский](README_RU.md)

# CSV Project — Pump Station Measurement Analysis

A personal Python learning project for reading, validating, and analyzing pump station measurement data from CSV files.

## Features

- Read comma-separated, UTF-8 CSV files using the Python standard library.
- Check for required columns: `timestamp`, `pump_id`, `pressure_mpa`, and `temperature_c`. Additional columns are allowed.
- Validate measurements and separate valid records from rejected records.
- Group valid measurements by pump ID.
- Calculate the record count, minimum and maximum pressure, average pressure, and average temperature for each pump.
- Export a report sorted by pump ID to `report.csv`.
- Display a final processing summary in the console.

## Input format

| Column | Description | Valid values |
| --- | --- | --- |
| `timestamp` | Measurement date and time | `YYYY-MM-DD HH:MM:SS` |
| `pump_id` | Pump identifier | Non-empty string |
| `pressure_mpa` | Pressure in megapascals (MPa) | 0 to 2, inclusive |
| `temperature_c` | Temperature in degrees Celsius (°C) | −40 to 150, inclusive |

## Run

From the repository root:

```bash
python src/csv_project/main.py
```

The input file path is set in [`main.py`](main.py) with `input_csv_file`. The report is written as `report.csv` to the current working directory.

No third-party packages are required.

## Sample datasets

- [Clean measurements](csv_training_tz01/measurements_clean.csv)
- [Measurements with minor errors](csv_training_tz01/measurements_minor_errors.csv)
- [Measurements with more errors](csv_training_tz01/measurements_bad.csv)
- [Expected results](csv_training_tz01/CHECK_AFTER_SOLUTION/expected_results.json)

## Project status

The main requirements of the learning assignment have been implemented: CSV reading, validation, per-pump calculations, sorted report export, and console summary.

This is a learning project, not a production-ready data processing service.

## Author and license

Created by [Evgenii Petrov](https://github.com/EvgeniiPetrov) to practice Python and data processing.

Copyright © 2026 Evgenii Petrov. Licensed under the [MIT License](LICENSE).
