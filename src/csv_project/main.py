import csv
import os
import sys
from datetime import datetime


class ColumnCountError(Exception):
    pass


class ZeroFileSizeError(Exception):
    pass


class FileConsistOnlyFieldnamesError(Exception):
    pass


class PumpIdError(Exception):
    pass


class PressureMpaNotDigitError(Exception):
    pass


class PressureMpaIsNotInRange(Exception):
    pass


def error_print_and_exit_1(err: Exception) -> None:
    print(f"Ошибка: {err}")
    sys.exit(1)


def check_not_zero_file_length(file_for_check: str) -> bool:
    return os.path.getsize(file_for_check) > 0


def is_number(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def check_is_wrong_pressure(pressure_mpa_for_check: str, row_number: int) -> bool:
    ready_for_check = pressure_mpa_for_check.strip()
    if not is_number(ready_for_check):
        raise PressureMpaNotDigitError(
            f"Давление (МПа) в строке {row_number} должно быть числовым значением. ([0..2] МПа)"
        )
    num_pressure_mpa = float(pressure_mpa_for_check)
    result = 0.0 <= num_pressure_mpa <= 2.0
    return not result


def check_is_wrong_timestamp(timestamp_for_check: str | None) -> bool:
    if timestamp_for_check is None:
        return True
    try:
        datetime.strptime(timestamp_for_check, "%Y-%m-%d %H:%M:%S")
        len_timestamp = len(timestamp_for_check)
        return not len_timestamp == 19  # noqa
    except ValueError:
        return True


def check_is_wrong_pump_id(pump_id_for_check: str | None) -> bool:
    if pump_id_for_check is None:
        return True
    if len(pump_id_for_check.strip()) == 0:
        return True
    if (  # noqa
        (pump_id_for_check.lower() == "none")
        or (pump_id_for_check.lower() == "error")
        or (pump_id_for_check.lower() == "nan")
    ):
        return True
    return False


def check_columns(data_for_check: list[dict]) -> bool:
    num_of_columns: int = 4
    column_counter: int = 0
    columns_names = list(data_for_check[0].keys())
    if len(columns_names) != num_of_columns:
        return False
    for column_name in columns_names:
        if column_name in [
            "timestamp",
            "pump_id",
            "pressure_mpa",
            "temperature_c",
        ]:  # timestamp,pump_id,pressure_mpa,temperature_c
            column_counter += 1

    return column_counter == num_of_columns  # Возвращает True или False


def main(file_for_cheking: str) -> None:
    """
    Entry point for the CSV project.
    This function initializes the application and starts the main process.
    """
    print("Starting the CSV project...")
    print(f"Проверяем файл: {file_for_cheking}")

    if check_not_zero_file_length(file_for_cheking):
        print("Файл существует и больше 0 байт.")
    else:
        raise ZeroFileSizeError("Размер файла 0 байт")
    count: int = 0
    with open(
        file_for_cheking,
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        for line in file:
            count += 1
        if count == 1:
            raise FileConsistOnlyFieldnamesError(
                "Файл состоит только из названий колонок"
            )
        file.seek(0)
        print(f"Количество записей в файле: {count - 1}")

        read = csv.DictReader(file)
        rows = list(read)

    checked_columns = check_columns(rows)
    if checked_columns:
        print(f"Назания колонок соответсвуют заявленным требованиям: {checked_columns}")
        print(
            "Заявленные имена столбцов: timestamp, pump_id, pressure_mpa, temperature_c \n"
        )
    else:
        raise ColumnCountError("Число столбцов должно быть 4.")

    #  Предварительная проверка перед преобразованием
    #
    total_wromg_lines: int = 0
    current_row: int = 0
    for current_row, row in enumerate(rows):
        offset_current_row = current_row + 1
        print(f"Проверяем строку №{offset_current_row} {row}")
        error_field_count: int = 0
        if check_is_wrong_timestamp(row.get("timestamp")):
            print(
                f"Значение {row.get('timestamp')} в строке №{offset_current_row} {row} не соответсвует формату YYYY-MM-DD HH:MM:SS"
            )
            error_field_count += 1

        if check_is_wrong_pump_id(row.get("pump_id")):
            print(
                f"Значение {row.get('pump_id')} в строке №{offset_current_row} {row} не должно быть пустым или состоять только из пробелов"
            )
            error_field_count += 1
        if error_field_count:
            total_wromg_lines += 1
        if check_is_wrong_pressure(row.get("pressure_mpa"), current_row):
            raise PressureMpaIsNotInRange(
                f"Давление (МПа) в строке №{offset_current_row} должно быть в диапазоне [0..2] МПа"
            )

    print(f"Общее число не коррестных строк: {total_wromg_lines}")


if __name__ == "__main__":
    try:
        input_csv_file: str = "src/csv_project/csv_training_tz01/measurements_clean.csv"
        main(input_csv_file)
    except FileNotFoundError as err:
        print(f"Файл с данными для проверки не найден.\nОшибка: {err.strerror}")
        print(f"Расположение: {input_csv_file}")
        sys.exit(1)
    except ZeroFileSizeError as err:
        error_print_and_exit_1(err)
    except FileConsistOnlyFieldnamesError as err:
        error_print_and_exit_1(err)
    except PumpIdError as err:
        error_print_and_exit_1(err)
    except PressureMpaNotDigitError as err:
        error_print_and_exit_1(err)
    except PressureMpaIsNotInRange as err:
        error_print_and_exit_1(err)
    except ColumnCountError as err:
        error_print_and_exit_1(err)
    sys.exit(0)
