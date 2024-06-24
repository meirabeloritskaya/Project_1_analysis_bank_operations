from datetime import datetime
from unittest.mock import patch
import sys
import os

# Добавляем путь к папке src в sys.path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, src_path)

from src.services import get_valid_month, get_limit, investment_bank


def test_get_valid_month():
    with patch("builtins.input", side_effect=["2020-05"]):
        expected_date = datetime(2020, 5, 1)
        assert get_valid_month() == expected_date


def test_get_limit():
    with patch("builtins.input", side_effect=["3"]):
        expected_limit = 100
        assert get_limit() == expected_limit


def test_investment_bank():
    month_start = datetime(2020, 5, 1)
    transactions = [
        {"Дата платежа": "01.05.2020", "Сумма операции": -150},
        {"Дата платежа": "05.05.2020", "Сумма операции": -90},
        {"Дата платежа": "15.05.2020", "Сумма операции": 100},
        {"Дата платежа": "25.05.2020", "Сумма операции": -200},
        {"Дата платежа": "01.06.2020", "Сумма операции": -250},
    ]
    limit = 100
    expected_savings = 60
    assert investment_bank(month_start, transactions, limit) == expected_savings


if __name__ == "__main__":
    test_get_valid_month()
    test_get_limit()
    test_investment_bank()

