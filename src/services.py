from datetime import datetime
import math
import logging
from read_transactions_excel import get_data_transactions


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


def investment_bank(month, transactions, limit):
    """вывод суммы инвесткопилки, заданной лимитом и месяцем"""
    logger.info("формирование списка транзакций, по заданному месяцу ")
    total_savings = 0.0
    month_start = datetime.strptime(month, "%Y-%m")

    for transaction in transactions:
        date_str = transaction.get("Дата платежа")

        if not isinstance(date_str, str) or date_str.lower() == "nan":
            logger.info("отсутсвует дата транзакции")
            continue

        try:
            transaction_date = datetime.strptime(date_str, "%d.%m.%Y")
            if (
                transaction_date.year == month_start.year
                and transaction_date.month == month_start.month
            ):
                amount = transaction["Сумма операции"]
                # print(transaction)

                if amount >= 0:
                    logger.info("положительная транзакция")
                    continue
                rounded_amount = math.ceil(amount / limit) * limit
                difference = rounded_amount - amount
                total_savings += difference
        except ValueError:
            print(f"Invalid date format: {date_str}")
    logger.info("вывод суммы инвесткопилки, заданной лимитом и месяцем")
    return round(total_savings, 2)


if __name__ == "__main__":
    path = "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/data/operations.xls"
    list_trans = get_data_transactions(path)

    month = "2021-08"
    limit = 50
    total_savings = investment_bank(month, list_trans, limit)
    print(f"Total savings for month {month}: {total_savings}")
