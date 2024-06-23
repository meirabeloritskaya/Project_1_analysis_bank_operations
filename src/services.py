from datetime import datetime
import math
from typing import List, Dict, Any
from read_transactions_excel import get_data_transactions


def investment_bank(
    month: str, transactions: List[Dict[str, Any]], limit: int
) -> float:
    total_savings = 0.0
    month_start = datetime.strptime(month, "%Y-%m")

    for transaction in transactions:
        date_str = transaction.get("Дата платежа")

        # Пропускаем транзакцию, если дата не является строкой или содержит "nan"
        if not isinstance(date_str, str) or date_str.lower() == "nan":

            continue

        try:
            transaction_date = datetime.strptime(date_str, "%d.%m.%Y")
            if (
                transaction_date.year == month_start.year
                and transaction_date.month == month_start.month
            ):
                amount = transaction["Сумма операции"]
                # print(transaction)
                rounded_amount = math.ceil(amount / limit) * limit
                difference = rounded_amount - amount
                total_savings += difference
        except ValueError:
            print(f"Invalid date format: {date_str}")

    return round(total_savings, 2)


if __name__ == "__main__":
    path = "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/data/operations.xls"
    list_trans = get_data_transactions(path)

    month = "2021-08"
    limit = 50
    total_savings = investment_bank(month, list_trans, limit)
    print(f"Total savings for month {month}: {total_savings}")
