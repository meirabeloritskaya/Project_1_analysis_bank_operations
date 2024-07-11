import os
import sys
from src.reports import (
    spending_by_category,
    get_unique_categories,
    choose_category,
    get_valid_date,
)


# Добавляем путь к папке src в sys.path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, src_path)


def test_spending_by_category(transactions_data, expected_spending_by_category):

    result = spending_by_category(transactions_data, "Еда", "01.04.2023")
    assert result == expected_spending_by_category, f"Expected {expected_spending_by_category}, but got {result}"


def test_get_unique_categories(transactions_data, expected_unique_categories):
    result = get_unique_categories(transactions_data)
    assert result == expected_unique_categories, f"Expected {expected_unique_categories}, but got {result}"


def test_choose_category(category_choice_input, expected_category_choice):
    categories = ["Еда", "Транспорт"]
    result = choose_category(categories)
    assert result == expected_category_choice, f"Expected {expected_category_choice}, but got {result}"


def test_get_valid_date(valid_date_input, expected_valid_date):
    result = get_valid_date()
    assert result == expected_valid_date, f"Expected {expected_valid_date}, but got {result}"
