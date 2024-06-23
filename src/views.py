from read_transactions_excel import get_data_transactions
from utils import greeting
from utils import get_transactions_by_date
from utils import top_5_trans_by_amount
from utils import get_exchange_rate
from utils import get_stock_prices
from utils import json_result
import os
from dotenv import load_dotenv

load_dotenv()
MY_API_KEY = os.getenv("API_KEY")
MY_BASE_URL = os.getenv("BASE_URL")


if __name__ == "__main__":
    my_date = "02.02.2018 00:00:00"
    my_path = "C:/Users/Meira/PycharmProjects/Project_1_analis_bank_operations/data/operations.xls"
    my_greeting = greeting()
    # print(my_greeting)
    my_transactions = get_data_transactions(my_path)
    my_data_by_date = get_transactions_by_date(my_transactions, my_date)
    # print(my_data_by_date)
    # print(*my_data_by_date, sep="\n")
    my_top_5_trans_by_amount = top_5_trans_by_amount(my_path)
    # print(*my_top_5_trans_by_amount, sep="\n")
    my_exchange_rate = get_exchange_rate(MY_API_KEY, MY_BASE_URL)
    # print(my_exchange_rate)
    my_stock_prices = get_stock_prices()
    my_json_result = json_result(
        my_greeting,
        my_data_by_date,
        my_top_5_trans_by_amount,
        my_exchange_rate,
        my_stock_prices,
    )

    print(my_json_result)
