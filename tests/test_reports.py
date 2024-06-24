from unittest.mock import patch
from datetime import datetime
import pandas as pd

import os
import sys

# Добавляем путь к папке src в sys.path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, src_path)

from src.reports import (
    spending_by_category,
    get_unique_categories,
    choose_category,
    get_valid_date,
)


def test_spending_by_category():
    transactions = pd.DataFrame(
        [
            {
                "Дата операции": "01.01.2023 12:00:00",
                "Категория": "Еда",
                "Сумма платежа": -150,
            },
            {
                "Дата операции": "05.02.2023 14:00:00",
                "Категория": "Еда",
                "Сумма платежа": -90,
            },
            {
                "Дата операции": "10.03.2023 16:00:00",
                "Категория": "Еда",
                "Сумма платежа": -200,
            },
            {
                "Дата операции": "15.04.2023 18:00:00",
                "Категория": "Еда",
                "Сумма платежа": -250,
            },
            {
                "Дата операции": "01.05.2023 12:00:00",
                "Категория": "Транспорт",
                "Сумма платежа": -100,
            },
        ]
    )

    expected_result = [
        {
            "Дата операции": "01.01.2023 12:00:00",
            "Категория": "Еда",
            "Сумма платежа": -150,
        },
        {
            "Дата операции": "05.02.2023 14:00:00",
            "Категория": "Еда",
            "Сумма платежа": -90,
        },
        {
            "Дата операции": "10.03.2023 16:00:00",
            "Категория": "Еда",
            "Сумма платежа": -200,
        },
    ]

    result = spending_by_category(transactions, "Еда", "01.04.2023")
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_get_unique_categories():
    transactions = pd.DataFrame(
        [
            {
                "Дата операции": "01.01.2023 12:00:00",
                "Категория": "Еда",
                "Сумма платежа": -150,
            },
            {
                "Дата операции": "05.02.2023 14:00:00",
                "Категория": "Еда",
                "Сумма платежа": -90,
            },
            {
                "Дата операции": "01.05.2023 12:00:00",
                "Категория": "Транспорт",
                "Сумма платежа": -100,
            },
        ]
    )

    expected_categories = ["Еда", "Транспорт"]
    result = get_unique_categories(transactions)
    assert (
        result == expected_categories
    ), f"Expected {expected_categories}, but got {result}"


@patch("builtins.input", side_effect=["1"])
def test_choose_category(mock_input):
    categories = ["Еда", "Транспорт"]
    expected_category = "Еда"
    result = choose_category(categories)
    assert (
        result == expected_category
    ), f"Expected {expected_category}, but got {result}"


@patch("builtins.input", side_effect=["01.04.2023"])
def test_get_valid_date(mock_input):
    expected_date = datetime.strptime("01.04.2023", "%d.%m.%Y")
    result = get_valid_date()
    assert result == expected_date, f"Expected {expected_date}, but got {result}"


if __name__ == "__main__":
    test_spending_by_category()
    test_get_unique_categories()
    test_choose_category()
    test_get_valid_date()
    print("All tests passed!")
