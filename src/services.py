from datetime import datetime, timedelta
import math
import logging
from read_transactions_excel import (
    get_data_transactions,
)  # Предположим, что этот модуль импортирует функцию get_data_transactions из файла read_transactions_excel


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(
    "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/logs/services.log",
    encoding="utf-8",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_valid_month():
    """Запрос и валидация ввода месяца и года в формате 'гггг-мм'."""
    while True:
        input_date = input("Введите месяц и год в формате гггг-мм: ").strip()
        try:
            datetime_obj = datetime.strptime(input_date, "%Y-%m")
            return (
                datetime_obj  # Возвращаем объект datetime при успешном преобразовании
            )
        except ValueError:
            print("Некорректный формат даты. Попробуйте еще раз.")


def investment_bank(month_start, transactions, limit):
    """Функция для расчета суммы инвесткопилки по заданному месяцу и лимиту."""
    logger.info("Формирование списка транзакций по заданному месяцу и году")
    total_savings = 0.0

    for transaction in transactions:
        date_str = transaction.get("Дата платежа")

        if not isinstance(date_str, str) or date_str.lower() == "nan":
            logger.info("Отсутствует дата транзакции")
            continue

        try:
            transaction_date = datetime.strptime(date_str, "%d.%m.%Y")
            if (
                transaction_date.year == month_start.year
                and transaction_date.month == month_start.month
            ):
                amount = transaction["Сумма операции"]

                if amount >= 0:
                    logger.info("Положительная транзакция")
                    continue

                rounded_amount = math.ceil(amount / limit) * limit
                difference = rounded_amount - amount
                total_savings += difference
        except ValueError:
            logger.error(f"Неверный формат даты: {date_str}")

    logger.info("Вычисление суммы инвесткопилки по заданному месяцу и лимиту")
    return round(total_savings, 2)


if __name__ == "__main__":
    path = "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/data/operations.xls"
    list_trans = get_data_transactions(path)  # Получаем данные транзакций из Excel

    month_start = get_valid_month()  # Запрашиваем у пользователя месяц и год
    limit = 1000  # Пример лимита для округления

    total_savings = investment_bank(month_start, list_trans, limit)
    print(f"Сумма инвесткопилки за {month_start.strftime('%Y-%m')}: {total_savings}")
