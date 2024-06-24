from read_transactions_excel import get_data_transactions
from utils import greeting
from utils import get_transactions_by_date
from utils import top_5_trans_by_amount
from utils import get_exchange_rate
from utils import get_stock_prices
from utils import json_result
from utils import read_user_settings
from utils import get_valid_date
import os
from dotenv import load_dotenv


def data_views():

    load_dotenv()
    my_path_to_user_settings_json = "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/user_settings.json"
    MY_API_KEY = os.getenv("API_KEY")
    MY_BASE_URL = os.getenv("BASE_URL")
    my_path_to_operations_xls = "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/data/operations.xls"

    # Вызываем функцию для получения даты и выводим результат
    my_date = get_valid_date()
    # my_date = "02.02.2018 00:00:00"
    my_path_to_operations_xls = "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/data/operations.xls"
    my_greeting = greeting()
    # print(my_greeting)
    my_transactions = get_data_transactions(my_path_to_operations_xls)
    my_data_by_date = get_transactions_by_date(my_transactions, my_date)
    # print(my_data_by_date)
    # print(*my_data_by_date, sep="\n")
    my_top_5_trans_by_amount = top_5_trans_by_amount(my_path_to_operations_xls)
    # print(*my_top_5_trans_by_amount, sep="\n")
    my_user_settings = read_user_settings(my_path_to_user_settings_json)
    my_user_currencies = my_user_settings.get("user_currencies", [])
    my_user_stocks = my_user_settings.get("user_stocks", [])
    my_exchange_rate = get_exchange_rate(MY_API_KEY, MY_BASE_URL, my_user_currencies)
    # print(my_exchange_rate)
    my_stock_prices = get_stock_prices(my_user_stocks)
    my_json_result = json_result(
        my_greeting,
        my_data_by_date,
        my_top_5_trans_by_amount,
        my_exchange_rate,
        my_stock_prices,
    )

    return my_json_result


if __name__ == "__main__":
    print(data_views())
