from unittest.mock import patch
import sys
import os
from src.services import get_valid_month, get_limit, investment_bank

# Добавляем путь к папке src в sys.path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, src_path)


def test_get_valid_month(valid_month_input, expected_valid_month):
    with patch("builtins.input", side_effect=["2020-05"]):
        with patch("builtins.input", side_effect=[valid_month_input]):
            assert get_valid_month() == expected_valid_month


def test_get_limit(limit_input, expected_limit):
    with patch("builtins.input", side_effect=[limit_input]):
        assert get_limit() == expected_limit


def test_investment_bank(investment_data, expected_savings):
    month_start, transactions, limit = investment_data
    assert investment_bank(month_start, transactions, limit) == expected_savings
