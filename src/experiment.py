import math


def investment_bank():

    total_savings = 0.0
    amount = int(input())
    if amount >= 0:
        return 0

    rounded_amount = math.ceil(abs(amount) / 100) * 100
    difference = rounded_amount - abs(amount)
    total_savings += difference
    return round(total_savings, 2)


print(investment_bank())
