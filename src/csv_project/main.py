import csv


def main() -> None:
    """
    Entry point for the CSV project.
    This function initializes the application and starts the main process.
    """

    print("Starting the CSV project...")

    with open(
        "src/csv_project/csv_training_tz01/measurements_clean.csv",
        "r",
        encoding="utf-8",
    ) as file:
        # csv_reader = list(csv.reader(file))
        read = csv.DictReader(file)
        rows = list(read)
        # for row in csv_reader:cl
        #     print(row)
        # csv_dict.fieldnames()
        # print(csv_reader)

    for row in rows:
        print(row["pump_id"])
    print(rows)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
