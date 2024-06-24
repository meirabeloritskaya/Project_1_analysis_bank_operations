import logging
import pandas as pd
from datetime import datetime
import functools
from read_transactions_excel import get_data_transactions
import json

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(
    "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/logs/reports.log",
    encoding="utf-8",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def report_to_file(filename="file_report.json"):
    """Декоратор записывает данные по отчету в файл"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for entry in result:
                entry["Дата операции"] = entry["Дата операции"].strftime(
                    "%d.%m.%Y %H:%M:%S"
                )
            with open(filename, "w+", encoding="utf-8") as f:
                # f.write(str(result))
                json.dump(result, f, ensure_ascii=False, indent=4)
                logger.info("Результат отчета записан в файл в формате JSON")
            return result

        return wrapper

    return decorator


@report_to_file("report.json")
def spending_by_category(transactions, category, date=None):
    """Функция возвращает траты по категориям за указанный месяц"""
    try:
        # Преобразование столбца 'Дата операции' в формат datetime
        transactions["Дата операции"] = pd.to_datetime(
            transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S"
        )

        if date is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date, "%d.%m.%Y")

        # Начало и конец месяца для фильтрации
        end_date_month = end_date.month
        start_month = end_date_month - 3
        start_date = end_date.replace(month=start_month)

        # Фильтрация транзакций по дате и категории
        filtered_transactions = transactions[
            (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= end_date)
            & (transactions["Категория"] == category)
            & (transactions["Сумма платежа"] < 0)
        ]

        # Проверка, есть ли отфильтрованные данные
        if filtered_transactions.empty:
            logger.info("Нет данных для указанного периода и категории")
            return []

        logger.info(f"Траты за указанный месяц по категории {category}")

        # print("Данные после фильтрации:")
        # print(filtered_transactions)

        return filtered_transactions.to_dict(orient="records")

    except Exception as e:
        print(f"ошибка {e}")
        logger.error(f"ошибка {e}")
        return []


if __name__ == "__main__":
    path = "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/data/operations.xls"
    list_trans = get_data_transactions(path)

    transactions = pd.DataFrame(list_trans)

    category = "Супермаркеты"
    date = "30.12.2021"

    result = spending_by_category(transactions, category, date)
    print(*result, sep="\n")
