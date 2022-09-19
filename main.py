import pandas as pd
import sys
import json
import requests


def main():

    orders_df = pd.read_csv(sys.argv[1])
    coins_invested = orders_df["product"].unique()

    # finish up following:
    # total invested
    # total fee payed
    # total profit/loss
    # but also show this for each coin
    # coin: invested
    # coin : fee payed
    # coin: total profit/loss

    # TOTAL VARIABLES FOR ALL CURRENCIES
    total_invested_no_fees = 0
    total_fee = 0
    total_invested = 0
    average_buy_prices_dict = {}
    total_invested_per_currency_dict = {}
    current_value_of_holding_dict = {}
    win_loss_of_holding_dict = {}

    # FOR EACH CURRENCY IN YOUR PORTFOLIO
    for coin in coins_invested:

        # 1 COIN VARIABLES
        average_buy_price = 0
        total_invested_in_this_coin_no_fees = 0
        total_fee_for_this_coin = 0
        total_invested_in_this_coin_including_fees = 0

        # filter out transactions for this currency in all transactions
        relevant_records_df = orders_df[orders_df["product"] == coin]
        relevant_records_df = relevant_records_df.reset_index()

        # total size of your currency in your portfolio (e.g. 2.5 ETH)
        total_coin_size = relevant_records_df["size"].sum()

        # For each buy order of this current coin
        for index, row in relevant_records_df.iterrows():

            # Calculate total investment in this coin
            total_invested_in_this_coin_no_fees = total_invested_in_this_coin_no_fees + row["size"] * row["price"]
            total_fee_for_this_coin = total_fee_for_this_coin + row["fee"]
            total_invested_in_this_coin_including_fees = total_invested_in_this_coin_no_fees + total_fee_for_this_coin

            # Calculate average buy price for this coin by adding weight to each buy order and adding it to total
            buy_order_weight = row["size"] / total_coin_size
            transaction_weighted_price = buy_order_weight * row["price"] + row["fee"]  # I calculate the fee within the buy order price. Seems most logical to me.
            average_buy_price = average_buy_price + transaction_weighted_price

            # Add totals for this coin to overall total for all coins
            total_invested_no_fees = total_invested_no_fees + total_invested_in_this_coin_no_fees
            total_fee = total_fee + row["fee"]
            total_invested = total_invested + total_invested_in_this_coin_including_fees

        current_coin_price = get_current_price(coin)

        average_buy_prices_dict[coin] = average_buy_price
        total_invested_per_currency_dict[coin] = total_invested_in_this_coin_including_fees
        current_value_of_holding_dict[coin] = float(total_coin_size) * float(current_coin_price)
        win_loss_of_holding_dict[coin] = current_value_of_holding_dict[coin] - total_invested_per_currency_dict[coin]

    total_invested = round(get_total_of_dict(total_invested_per_currency_dict), 2)
    total_current_value_of_holding = round(get_total_of_dict(current_value_of_holding_dict), 2)
    total_profit = round(get_total_of_dict(win_loss_of_holding_dict), 2)

    print("Overview on your investments")

    print_dict("Your average buy prices: ", average_buy_prices_dict)
    print_dict("Your Total Investment per currency: ", total_invested_per_currency_dict)
    print_dict("Current value of your holdings: ", current_value_of_holding_dict)
    print_dict("Your wins/losses per holding: ", win_loss_of_holding_dict)
    print("Quick Overview:\n\tTotal invested:\t\t€ {}\n\tTotal current value:\t€ {}\n\tTotal profit:\t\t€ {}".format(total_invested, total_current_value_of_holding, total_profit))


def get_total_of_dict(dict):
    total = 0
    for key in dict:
        total = total + dict[key]
    return total


def print_dict(preceeding_text, dict):
    print(preceeding_text + "\n")
    for key in dict:
        print("\t{}: \t€ {}".format(key, round(dict[key], 2)))
    print("\n")


def get_current_price(currency):
    url_part1 = "https://api.coinbase.com/v2/prices/"
    url_part2 = "/spot"
    request_url = url_part1 + currency + url_part2
    request_data = requests.get(request_url).json()
    current_price = request_data["data"]["amount"]
    return current_price


if __name__ == "__main__":
    main()
