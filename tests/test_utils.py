import pytest
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import json
import pandas as pd

from src.utils import (
    greeting,
    calculate_cashback,
    get_valid_date,
    get_transactions_by_date,
    top_5_trans_by_amount,
    read_user_settings,
    get_exchange_rate,
    get_stock_prices,
    json_result,
)


def test_greeting(greeting_expected):
    assert greeting() == greeting_expected


@pytest.mark.parametrize("input_amount, expected_cashback", [(-100, 1), (-50, 0), (100, 0), (0, 0)])
def test_calculate_cashback(input_amount, expected_cashback):
    assert calculate_cashback(input_amount) == expected_cashback


@patch("builtins.input", side_effect=["25.12.2020"])
def test_get_valid_date(mock_input):
    expected_date = "25.12.2020 00:00:00"
    assert get_valid_date() == expected_date


def test_get_transactions_by_date(transactions, expected_transactions):
    date = "31.12.2020 00:00:00"
    assert get_transactions_by_date(transactions, date) == expected_transactions


@patch("pandas.read_excel")
def test_top_5_trans_by_amount(mock_read_excel, expected_top_5):
    mock_df = pd.DataFrame(
        {
            "Дата платежа": [
                "01.12.2020",
                "02.12.2020",
                "03.12.2020",
                "04.12.2020",
                "05.12.2020",
            ],
            "Сумма платежа": [500, 400, 300, 200, 100],
            "Категория": [
                "Категория1",
                "Категория2",
                "Категория3",
                "Категория4",
                "Категория5",
            ],
            "Описание": [
                "Описание1",
                "Описание2",
                "Описание3",
                "Описание4",
                "Описание5",
            ],
        }
    )
    mock_read_excel.return_value = mock_df
    path = "dummy_path"
    assert top_5_trans_by_amount(path) == expected_top_5


def test_read_user_settings(user_settings):
    file_path = "dummy_settings.json"

    with patch("builtins.open", unittest.mock.mock_open(read_data=json.dumps(user_settings))):
        assert read_user_settings(file_path) == user_settings

    with patch("builtins.open", side_effect=FileNotFoundError):
        assert read_user_settings(file_path) is None

    with patch("builtins.open", unittest.mock.mock_open(read_data="invalid json")):
        assert read_user_settings(file_path) is None


@patch("requests.get")
def test_get_exchange_rate(mock_get, mock_exchange_rate_response, user_currencies, expected_exchange_rates):
    api_key = "dummy_key"
    BASE_URL = "https://dummy_url/"

    mock_response = MagicMock()
    mock_response.json.return_value = mock_exchange_rate_response
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    assert get_exchange_rate(api_key, BASE_URL, user_currencies) == expected_exchange_rates


@patch("yfinance.Ticker")
def test_get_stock_prices(mock_ticker, mock_stock_info, user_stocks, expected_stock_prices):

    mock_stock = MagicMock()
    mock_stock.info = mock_stock_info
    mock_ticker.return_value = mock_stock

    assert get_stock_prices(user_stocks) == expected_stock_prices


def test_json_result(
    expected_json_result, greeting_msg, transactions_for_json, top_transactions, exchange_rate, stock_prices
):

    assert (
        json_result(greeting_msg, transactions_for_json, top_transactions, exchange_rate, stock_prices)
        == expected_json_result
    )
