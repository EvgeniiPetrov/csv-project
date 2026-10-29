import csv
import math
import os
import sys
from datetime import datetime


class MissingCorrectDataError(Exception):
    pass


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


class TemperatureCIsNotInRange(Exception):
    pass


def error_print_and_exit_1(err: Exception) -> None:
    print(f"Ошибка: {err}")
    sys.exit(1)


def check_not_zero_file_length(file_for_check: str) -> bool:
    return os.path.getsize(file_for_check) > 0


def is_number(value: str) -> bool:
    try:
        if (float(value) == math.inf) or (float(value) == -math.inf):
            return False
        if math.isnan(float(value)):  # noqa
            return False
        return True
    except ValueError:
        return False


def check_rows(rows_for_check: list[dict]) -> set:
    #  Предварительная проверка перед преобразованием
    total_wrong_lines: int = 0
    current_row: int = 0
    wrong_lines = set()
    for current_row, row in enumerate(rows_for_check):
        offset_current_row = (
            current_row + 2
        )  # +1 для смещения на заголовок и +1 для смещения на 0 индекс
        # print(f"Проверяем строку №{offset_current_row} {row}")
        error_field_count: int = 0

        timestamp = row.get("timestamp")
        if check_is_wrong_timestamp(timestamp):
            print(
                f"Значение {row.get('timestamp')} в строке №{offset_current_row} {row} не соответсвует формату YYYY-MM-DD HH:MM:SS"
            )
            error_field_count += 1
        pump_id = row.get("pump_id")
        if check_is_wrong_pump_id(pump_id):
            print(
                f"Значение {row.get('pump_id')} в строке №{offset_current_row} {row} не должно быть пустым или состоять только из пробелов"
            )
            error_field_count += 1
        pressure_mpa = row.get("pressure_mpa")
        if check_is_wrong_pressure(pressure_mpa, current_row):
            print(
                f"Давление {pressure_mpa}(МПа) в строке {offset_current_row} должно быть в диапазоне [0..2] МПа"
            )
            error_field_count += 1
        temperature_c: str = row.get("temperature_c")
        if check_is_wrong_temperature(temperature_c, current_row):
            print(
                f"Температура (\u2103) в строке {offset_current_row} должно быть в диапазоне [-40..150] \u2103)"
            )
            error_field_count += 1

        if error_field_count:
            total_wrong_lines += 1
            wrong_lines.add(current_row)

    print(f"Общее число не коррестных строк: {total_wrong_lines}")
    print(f"Номера не корректных строк: {wrong_lines}")
    return wrong_lines


def check_is_wrong_temperature(temperature_c_for_check: str, row_number: int) -> bool:
    if temperature_c_for_check is not None:
        ready_for_check = temperature_c_for_check.strip()
    else:
        return True
    if not is_number(ready_for_check):
        return True
    num_temperature = float(temperature_c_for_check)
    result = -40.0 <= num_temperature <= 150.0
    return not result


def check_is_wrong_pressure(pressure_mpa_for_check: str, row_number: int) -> bool:
    if pressure_mpa_for_check is not None:
        ready_for_check = pressure_mpa_for_check.strip()
    else:
        return True
    if not is_number(ready_for_check):
        return True
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
    if len(pump_id_for_check.strip()) == 0:  # noqa
        return True
    # мои добавления
    # if (  # noqa
    #     (pump_id_for_check.lower() == "none")
    #     # or (pump_id_for_check.lower() == "error")
    #     or (pump_id_for_check.lower() == "nan")
    # ):
    #     return True
    return False


# def check_columns(data_for_check: list[dict]) -> bool:
#     num_of_columns: int = 4
#     column_counter: int = 0
#     columns_names = list(data_for_check[0].keys())
#     if len(columns_names) != num_of_columns:
#         return False
#     for column_name in columns_names:
#         if column_name in [
#             "timestamp",
#             "pump_id",
#             "pressure_mpa",
#             "temperature_c",
#         ]:  # timestamp,pump_id,pressure_mpa,temperature_c
#             column_counter += 1

#     return column_counter == num_of_columns  # Возвращает True или False


def check_columns(data_for_check) -> bool:
    if data_for_check is None:
        return False
    num_of_columns: int = 4
    column_counter: int = 0
    # columns_names = list(data_for_check[0].keys())
    columns_names = data_for_check
    # print("***")
    # print(columns_names)
    # print(f"Количество столбцов: {len(columns_names)}")
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
                f"В принятом файле {file_for_cheking} только одна строка."
            )
        file.seek(0)
        print(f"Количество записей в файле: {count - 1}")

        read = csv.DictReader(file)
        field_names = read.fieldnames
        print(f"Названия колонок в файле: {field_names}")
        checked_columns = check_columns(field_names)
        rows: list[dict] = list(read)

    # checked_columns = check_columns(rows)
    if checked_columns:
        print(f"Назания колонок соответсвуют заявленным требованиям: {checked_columns}")
        print(
            "Заявленные имена столбцов: timestamp, pump_id, pressure_mpa, temperature_c \n"
        )
    else:
        raise ColumnCountError("Число столбцов должно быть 4.")
    position_of_wrong_rows: set = check_rows(rows)
    print(f"Повторно: Номера не корректных строк: {position_of_wrong_rows}")
    print("***")

    clear_rows: list[dict] = []
    bad_rows: list[dict] = []
    for row_position, row in enumerate(rows):
        if row_position in position_of_wrong_rows:
            print(f"Wrong string number is {row_position}")
            bad_rows.append(row)
        else:
            clear_rows.append(row)
    if len(clear_rows) == 0:
        raise MissingCorrectDataError(
            f"Отсутствуют корректные данные для обработки. \n Количество корректных данных равно {len(clear_rows)}. \n Количество не корректных данных: {len(bad_rows)}"
        )
    print("*** The next step is checking the filtered  clear data. *** ")
    check_rows(clear_rows)
    print("*** The next step is checking the incorrect data. *** ")
    check_rows(bad_rows)
    for row in bad_rows:
        print(row)
    print("***")
    sorted_rows = sorted(clear_rows, key=lambda x: (x["pump_id"], x["timestamp"]))
    uniq_pump_id = list(
        {row["pump_id"] for row in clear_rows}
    )  # this is Set (It cintains unique values)
    print(uniq_pump_id)

    for pump_id in uniq_pump_id:
        print("***")
        pump_id_records: list[dict] = list(
            filter(lambda x: x["pump_id"] == pump_id, sorted_rows)
        )
        number_of_dimensions: int = len(pump_id_records)
        if number_of_dimensions == 0:
            print(f"Корректные данные по насосному агрегату {pump_id} отсутсвуют.")
            continue
        print(f"Данные по НА: {pump_id}")
        print(f"Количество корректных измерений: {number_of_dimensions} шт.")
        min_pressure = min(pump_id_records, key=lambda x: float(x["pressure_mpa"]))
        print(
            f"Минимальное давление: {min_pressure['pressure_mpa']} МПа в {min_pressure['timestamp']}"
        )
        max_pressure = max(pump_id_records, key=lambda x: float(x["pressure_mpa"]))
        print(
            f"Максимальное давление: {max_pressure['pressure_mpa']} Мпа в {max_pressure['timestamp']}"
        )
        sum_pumps_pressuries = [float(d["pressure_mpa"]) for d in pump_id_records]
        average_pressure = round(
            sum(sum_pumps_pressuries) / len(sum_pumps_pressuries), 3
        )
        print(f"Среднее давление: {average_pressure} МПа")

        sum_pumps_temperatures = [float(d["temperature_c"]) for d in pump_id_records]
        average_temperature = round(
            sum(sum_pumps_temperatures) / len(sum_pumps_temperatures), 3
        )
        print(f"Средняя температура: {average_temperature} \u2103")


if __name__ == "__main__":
    try:
        # measurements_clean.csv
        # measurements_minor_errors.csv
        # measurements_bad.csv
        input_csv_file: str = (
            "src/csv_project/csv_training_tz01/measurements_minor_errors.csv"
        )
        main(input_csv_file)
    except FileNotFoundError as err:
        print(f"Файл с данными для проверки не найден.\nОшибка: {err.strerror}")
        print(f"Расположение: {input_csv_file}")
        sys.exit(1)
    except ZeroFileSizeError as err:
        error_print_and_exit_1(err)
    except MissingCorrectDataError as err:
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
    except TemperatureCIsNotInRange as err:
        error_print_and_exit_1(err)
    sys.exit(0)
